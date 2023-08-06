# Copyright 2021 Karlsruhe Institute of Technology
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
import os

import requests
from flask import current_app
from flask import send_file

from kadi.lib.api.blueprint import bp
from kadi.lib.api.core import internal
from kadi.lib.api.core import json_error_response
from kadi.lib.api.core import json_response
from kadi.lib.config.core import get_sys_config
from kadi.lib.storage.misc import create_misc_storage


@bp.get("/sysadmin/config/index-image", v=None)
@internal
def preview_index_image():
    """Preview the configured index image directly in the browser."""
    image_identifier = get_sys_config("INDEX_IMAGE", use_fallback=False)
    filepath = None

    # Check whether an image that was uploaded via the GUI should be used or try to use
    # the path specified directly in the config file as fallback, if applicable.
    if image_identifier is not None:
        storage = create_misc_storage()
        filepath = storage.create_filepath(image_identifier)

        if not storage.exists(filepath):
            filepath = None
    else:
        filepath = current_app.config["INDEX_IMAGE"]

        if filepath is not None and not os.path.isfile(filepath):
            filepath = None

    if filepath is not None:
        return send_file(filepath, mimetype="image/jpeg", download_name="index.jpg")

    return json_error_response(404)


@bp.get("/sysadmin/latest-version", v=None)
@internal
def get_latest_version():
    """Get the latest released Kadi version via PyPI."""
    latest_version = None

    try:
        response = requests.get(current_app.config["RELEASE_URL"], timeout=5)
        latest_version = response.json()["info"]["version"]
    except Exception as e:
        current_app.logger.exception(e)

    return json_response(200, {"latest_version": latest_version})
