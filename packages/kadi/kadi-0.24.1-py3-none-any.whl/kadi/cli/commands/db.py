# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import sys

import click
from flask import current_app
from flask_migrate import downgrade as downgrade_db
from flask_migrate import upgrade as upgrade_db

from kadi.cli.main import kadi
from kadi.cli.utils import check_env
from kadi.cli.utils import danger
from kadi.cli.utils import echo
from kadi.cli.utils import success
from kadi.cli.utils import warning
from kadi.ext.db import db as database
from kadi.lib.db import update_object
from kadi.lib.licenses.models import License
from kadi.lib.licenses.utils import get_builtin_licenses
from kadi.lib.licenses.utils import get_plugin_licenses
from kadi.lib.permissions.utils import initialize_system_role
from kadi.modules.accounts.providers import LocalProvider
from kadi.modules.collections.core import create_collection
from kadi.modules.groups.core import create_group
from kadi.modules.records.core import create_record


@kadi.group()
def db():
    """Utility commands for database management."""


def _initialize_db():
    for role_name in current_app.config["SYSTEM_ROLES"]:
        role = initialize_system_role(role_name)

        if role is not None:
            echo(f"Initialized system role '{role_name}'.")

    if License.query.count() == 0:
        licenses = get_builtin_licenses()

        for name, license_meta in licenses.items():
            License.create(
                name=name, title=license_meta["title"], url=license_meta["url"]
            )

        echo("Initialized licenses.")


@db.command()
@click.argument("revision", default="head")
def upgrade(revision):
    """Upgrade the database schema to a specified revision.

    The default behaviour is to upgrade to the latest revision.
    """
    upgrade_db(directory=current_app.config["MIGRATIONS_PATH"], revision=revision)

    database.session.commit()
    success("Upgrade completed successfully.")


@db.command()
@click.argument("revision", default="-1")
@click.option("--i-am-sure", is_flag=True)
@check_env
def downgrade(revision, i_am_sure):
    """Downgrade the database schema to a specified revision.

    The default behaviour is to downgrade a single revision.
    """
    if not i_am_sure:
        warning(
            "This can potentially erase some data of database"
            f" '{current_app.config['SQLALCHEMY_DATABASE_URI']}'. If you are sure you"
            " want to do this, use the flag --i-am-sure."
        )
        sys.exit(1)

    downgrade_db(directory=current_app.config["MIGRATIONS_PATH"], revision=revision)

    database.session.commit()
    success("Downgrade completed successfully.")


@db.command()
def init():
    """Initialize the database."""
    upgrade_db(directory=current_app.config["MIGRATIONS_PATH"], revision="head")
    _initialize_db()

    database.session.commit()
    success("Initialization completed successfully.")


@db.command()
@click.option("--i-am-sure", is_flag=True)
@check_env
def reset(i_am_sure):
    """Reset and reinitialize the database."""
    if not i_am_sure:
        warning(
            "This will erase all data of database"
            f" '{current_app.config['SQLALCHEMY_DATABASE_URI']}'. If you are sure you"
            " want to do this, use the flag --i-am-sure."
        )
        sys.exit(1)

    downgrade_db(directory=current_app.config["MIGRATIONS_PATH"], revision="base")
    upgrade_db(directory=current_app.config["MIGRATIONS_PATH"], revision="head")
    _initialize_db()

    database.session.commit()
    success("Reset completed successfully.")


@db.command()
def licenses():
    """Update the plugin licenses stored in the database.

    Note that plugin licenses that have previously been added to the database, but are
    not included in the current plugin licenses anymore, will only be deleted if they
    are not in use by any record.
    """
    builtin_licenses = get_builtin_licenses()
    plugin_licenses = get_plugin_licenses()

    for license in License.query.order_by(License.name):
        # Check if the current license is a deprecated plugin license.
        if license.name not in builtin_licenses and license.name not in plugin_licenses:
            current_records = license.records.count()

            warning(
                f"Found deprecated license '{license.name}' in database, which is"
                f" currently used by {current_records} record(s)."
            )

            # Keep licenses that are still in use.
            if current_records == 0:
                database.session.delete(license)
                echo(f"Deleted license '{license.name}'.")

    # Update the current plugin licenses.
    for name, license_meta in plugin_licenses.items():
        license = License.query.filter_by(name=name).first()

        title = license_meta["title"]
        url = license_meta["url"]

        if license is None:
            License.create(name=name, title=title, url=url)
            echo(f"Added new license '{name}'.")
        else:
            if name in builtin_licenses:
                warning(f"License '{name}' is built-in and cannot be changed.")
            else:
                update_object(license, title=title, url=url)
                echo(f"Updated license '{name}'.")

    database.session.commit()
    success("Licenses updated successfully.")


@db.command()
@click.option("--i-am-sure", is_flag=True)
@check_env
def test_data(i_am_sure):
    """Reset the database and setup sample data."""
    if not i_am_sure:
        warning(
            "This will erase all data of database"
            f" '{current_app.config['SQLALCHEMY_DATABASE_URI']}' and replace it with"
            " sample data. If you are sure you want to do this, use the flag"
            " --i-am-sure."
        )
        sys.exit(1)

    downgrade_db(directory=current_app.config["MIGRATIONS_PATH"], revision="base")
    upgrade_db(directory=current_app.config["MIGRATIONS_PATH"], revision="head")
    _initialize_db()

    if not LocalProvider.is_registered():
        danger("The local provider is not registered in the application.")
        sys.exit(1)

    # Set up an admin that can do anything.
    LocalProvider.register(
        username="admin",
        email="admin@example.com",
        displayname="Admin",
        password="admin123",
        system_role="admin",
        apply_role_rules=False,
    )

    # Setup a guest user with read-only access.
    LocalProvider.register(
        username="guest",
        email="guest@example.com",
        displayname="Guest",
        password="guest123",
        system_role="guest",
        apply_role_rules=False,
    )

    # Set up a normal user that can create new resources.
    member = LocalProvider.register(
        username="member",
        email="member@example.com",
        displayname="Member",
        password="member123",
        system_role="member",
        apply_role_rules=False,
    )

    # Setup additional local sample users and resources, the latter belonging to the
    # "member" user.
    echo("Setting up sample data...")

    for i in range(1, 31):
        LocalProvider.register(
            username=f"user-{i}",
            email=f"user-{i}@example.com",
            displayname=f"User {i}",
            password=f"user{i}123",
            apply_role_rules=False,
        )

        create_record(
            creator=member.user,
            identifier=f"sample-record-{i}",
            title=f"Sample record {i}",
            type="sample",
            description="This is a sample record.",
            extras=[
                {"type": "str", "key": "sample 1", "value": "test"},
                {"type": "float", "key": "sample 2", "value": 3.141, "unit": "cm"},
            ],
            tags=["sample tag", "sample record tag"],
            visibility="private" if i <= 15 else "public",
        )

        create_collection(
            creator=member.user,
            identifier=f"sample-collection-{i}",
            title=f"Sample collection {i}",
            description="This is a sample collection.",
            tags=["sample tag", "sample collection tag"],
            visibility="private" if i <= 15 else "public",
        )

        create_group(
            creator=member.user,
            identifier=f"sample-group-{i}",
            title=f"Sample group {i}",
            description="This is a sample group.",
            visibility="private" if i <= 15 else "public",
        )

    database.session.commit()
    success("Setup completed successfully.")
