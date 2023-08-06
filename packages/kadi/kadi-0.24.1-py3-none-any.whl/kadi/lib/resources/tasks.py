# Copyright 2022 Karlsruhe Institute of Technology
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
from datetime import timedelta

from flask import current_app
from flask_babel import force_locale
from flask_login import current_user

import kadi.lib.constants as const
from kadi.ext.celery import celery
from kadi.ext.db import db
from kadi.lib.db import get_class_by_tablename
from kadi.lib.publication import publish_resource
from kadi.lib.tasks.core import launch_task
from kadi.lib.tasks.models import Task
from kadi.lib.utils import utcnow
from kadi.lib.web import get_locale
from kadi.modules.accounts.core import purge_user
from kadi.modules.accounts.models import User
from kadi.modules.collections.core import purge_collection
from kadi.modules.collections.models import Collection
from kadi.modules.groups.core import purge_group
from kadi.modules.groups.models import Group
from kadi.modules.records.core import purge_record
from kadi.modules.records.models import Record
from kadi.modules.records.utils import clean_files


def clean_resources(inside_task=False):
    """Clean all deleted users and expired, deleted resources.

    Note that this function issues one or more database commits.

    :param inside_task: (optional) A flag indicating whether the function is executed in
        a task. In that case, additional information will be logged.
    """
    expiration_date = utcnow() - timedelta(
        seconds=current_app.config["RESOURCES_MAX_AGE"]
    )

    # Purge deleted users.
    users = User.query.filter(User.state == "deleted")

    if inside_task and users.count() > 0:
        current_app.logger.info(f"Purging {users.count()} deleted user(s).")

    for user in users:
        purge_user(user)

    db.session.commit()

    # Purge expired records.
    records = Record.query.filter(
        Record.state == "deleted", Record.last_modified < expiration_date
    )

    if inside_task and records.count() > 0:
        current_app.logger.info(f"Purging {records.count()} expired record(s).")

    for record in records:
        purge_record(record)

    # Purge expired collections.
    collections = Collection.query.filter(
        Collection.state == "deleted", Collection.last_modified < expiration_date
    )

    if inside_task and collections.count() > 0:
        current_app.logger.info(f"Purging {collections.count()} expired collection(s).")

    for collection in collections:
        purge_collection(collection)

    # Purge expired groups.
    groups = Group.query.filter(
        Group.state == "deleted", Group.last_modified < expiration_date
    )

    if inside_task and groups.count() > 0:
        current_app.logger.info(f"Purging {groups.count()} expired group(s).")

    for group in groups:
        purge_group(group)

    db.session.commit()


@celery.task(name="kadi.resources.clean_resources")
def _clean_resources_task(**kwargs):
    clean_resources(inside_task=True)
    clean_files(inside_task=True)


@celery.task(
    name="kadi.resources.publish_resource", soft_time_limit=const.ONE_HOUR, bind=True
)
def _publish_resource_task(
    self, provider, resource_type, resource_id, form_data, locale, **kwargs
):
    task = Task.query.get(self.request.id)

    if task.is_revoked:
        return None

    model = get_class_by_tablename(resource_type)
    resource = model.query.get(resource_id)
    user = User.query.get(kwargs["_meta"]["user"])

    success = False

    try:
        # Since the result template may contain translatable strings and we cannot get
        # the user's locale the usual way, we instead force the locale that was given to
        # us.
        with force_locale(locale):
            success, template = publish_resource(
                provider, resource, form_data=form_data, user=user, task=task
            )

        if not success:
            task.state = "failure"

        task.result = {"template": template}

    # Catches time limit exceeded exceptions as well.
    except Exception as e:
        current_app.logger.exception(e)

        db.session.rollback()
        task.state = "failure"

    db.session.commit()
    return success


def start_publish_resource_task(
    provider, resource, form_data=None, user=None, force_locale=True
):
    """Publish a resource using a given provider in a background task.

    The created task will be kept in the database and the user that started the task
    will get notified about its current status as well.

    Note that this function issues one or more database commits.

    :param provider: The unique name of the publication provider.
    :param resource: The :class:`.Record` or :class:`.Collection` to publish.
    :param form_data: (optional) Form data as dictionary to customize the publication
        process.
    :param user: (optional) The user that started the task. Defaults to the current
        user.
    :param force_locale: (optional) Flag indicating whether the current locale as
        returned by :func:`kadi.lib.web.get_locale` should be used inside the task. If
        ``False``, the default locale will be used instead given by ``LOCALE_DEFAULT``
        as configured in the application's configuration.
    :return: A tuple containing a flag whether a previous publishing task was already
        started by the given user (in which case no new task will be started) and either
        the new task object or ``None``, depending on whether the task was started
        successfully.
    """
    form_data = form_data if form_data is not None else {}
    user = user if user is not None else current_user

    task = Task.query.filter(
        Task.name == "kadi.resources.publish_resource",
        Task.state.in_(["pending", "running"]),
        Task.user_id == user.id,
    ).first()

    if task is not None:
        return False, None

    if force_locale:
        locale = get_locale()
    else:
        locale = current_app.config["LOCALE_DEFAULT"]

    return True, launch_task(
        "kadi.resources.publish_resource",
        args=(
            provider,
            resource.__class__.__tablename__,
            resource.id,
            form_data,
            locale,
        ),
        user=user,
        keep=True,
        notify=True,
    )
