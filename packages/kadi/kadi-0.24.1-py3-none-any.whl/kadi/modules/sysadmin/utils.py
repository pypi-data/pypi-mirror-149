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
from functools import wraps
from uuid import uuid4

from flask import abort
from flask_login import current_user
from flask_login import login_required

from kadi.lib.config.core import get_sys_config
from kadi.lib.config.core import remove_sys_config
from kadi.lib.config.core import set_sys_config
from kadi.lib.storage.misc import delete_thumbnail
from kadi.lib.storage.misc import save_as_thumbnail


def sysadmin_required(func):
    """Decorator to add access restrictions based on sysadmin status to an endpoint.

    If the current user is not authenticated, the decorator will behave the same as
    Flask-Login's ``login_required`` decorator.
    """

    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_sysadmin:
            abort(404)

        return func(*args, **kwargs)

    return login_required(decorated_view)


def save_index_image(file_object):
    """Set an image file used on the index page as a global config item.

    Uses :func:`kadi.lib.storage.local.save_as_thumbnail` to create and save a thumbnail
    of the given image. If the image cannot be saved, :func:`delete_index_image` will be
    called.

    :param file_object: The image file object.
    """
    config_item = set_sys_config("INDEX_IMAGE", str(uuid4()))

    if not save_as_thumbnail(
        config_item.value, file_object, max_image_size=(1024, 1024)
    ):
        delete_index_image()


def delete_index_image(keep_config=False):
    """Delete the image file used on the index page, including the global config item.

    Uses :func:`kadi.lib.storage.local.delete_thumbnail` to delete the actual thumbnail
    file.

    :param keep_config: (optional) A flag indicating whether the config item in the
        database should be kept, in which case only the actual image in the storage will
        be deleted.
    """
    image_identifier = get_sys_config("INDEX_IMAGE", use_fallback=False)

    if image_identifier is not None:
        delete_thumbnail(image_identifier)

    if not keep_config:
        remove_sys_config("INDEX_IMAGE")


def legals_acceptance_required():
    """Check whether users need to accept the configured legal notices.

    :return: ``True`` if any of the legal notices are configured and accepting them is
        enforced, ``False`` otherwise.
    """
    if not get_sys_config("ENFORCE_LEGALS"):
        return False

    for config_item in ["TERMS_OF_USE", "PRIVACY_POLICY"]:
        if get_sys_config(config_item):
            return True

    return False
