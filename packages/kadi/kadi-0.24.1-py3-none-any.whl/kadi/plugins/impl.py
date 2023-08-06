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
# pylint: disable=missing-function-docstring
from flask import current_app
from flask import render_template

from kadi.lib.api.blueprint import bp as api_bp
from kadi.lib.db import has_extension
from kadi.lib.storage.local import LocalStorage
from kadi.modules.accounts.blueprint import bp as accounts_bp
from kadi.modules.collections.blueprint import bp as collections_bp
from kadi.modules.groups.blueprint import bp as groups_bp
from kadi.modules.main.blueprint import bp as main_bp
from kadi.modules.notifications.blueprint import bp as notifications_bp
from kadi.modules.records.blueprint import bp as records_bp
from kadi.modules.records.previews import get_builtin_preview_data
from kadi.modules.settings.blueprint import bp as settings_bp
from kadi.modules.sysadmin.blueprint import bp as sysadmin_bp
from kadi.modules.templates.blueprint import bp as templates_bp
from kadi.modules.workflows.blueprint import bp as workflows_bp
from kadi.modules.workflows.core import get_custom_mimetype
from kadi.plugins import hookimpl


@hookimpl(tryfirst=True)
def kadi_register_blueprints(app):
    if app.config["EXPERIMENTAL_FEATURES"]:
        import kadi.modules.workflows.api  # pylint: disable=unused-import

        app.register_blueprint(workflows_bp, url_prefix="/workflows")

    for bp, prefix in [
        (api_bp, "/api"),
        (accounts_bp, None),
        (collections_bp, "/collections"),
        (groups_bp, "/groups"),
        (main_bp, None),
        (notifications_bp, None),
        (records_bp, "/records"),
        (settings_bp, "/settings"),
        (sysadmin_bp, "/sysadmin"),
        (templates_bp, "/templates"),
    ]:
        app.register_blueprint(bp, url_prefix=prefix)


@hookimpl(tryfirst=True)
def kadi_register_capabilities():
    return "timescaledb" if has_extension("timescaledb") else None


@hookimpl(tryfirst=True)
def kadi_get_storages():
    return LocalStorage(root_directory=current_app.config["STORAGE_PATH"])


@hookimpl(tryfirst=True)
def kadi_get_custom_mimetype(file, base_mimetype):
    return get_custom_mimetype(file, base_mimetype)


@hookimpl(tryfirst=True)
def kadi_get_preview_data(file):
    return get_builtin_preview_data(file)


@hookimpl(tryfirst=True)
def kadi_get_preview_templates(file):
    return render_template("records/snippets/preview_file.html", file=file)
