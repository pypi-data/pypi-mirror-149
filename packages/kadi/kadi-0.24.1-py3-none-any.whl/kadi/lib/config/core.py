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
from flask import current_app

from .models import ConfigItem
from kadi.config import configs
from kadi.ext.db import db
from kadi.lib.cache import memoize_request


@memoize_request
def get_sys_config(key, use_fallback=True):
    """Get the value of a global config item from the database.

    This function can be used as an alternative to directly accessing the application's
    configuration if a certain config item can be stored in the database as well.

    :param key: The key of the config item.
    :param use_fallback: (optional) Whether the application's configuration should be
        used as a fallback if no matching key could be found in the database.
    :return: The value of the config item or ``None`` if no matching item could be found
        and ``use_fallback`` is ``False``.
    :raises KeyError: If no config item could be found and ``use_fallback`` is ``True``.
    """
    config_item = ConfigItem.query.filter(
        ConfigItem.key == key, ConfigItem.user_id.is_(None)
    ).first()

    if config_item is None:
        if use_fallback:
            return current_app.config[key]

        return None

    return config_item.value


def set_sys_config(key, value):
    """Set a global config item in the database.

    Note that trying to set an existing config item to its default value, as specified
    in the application's configuration, will instead remove this config item from the
    database.

    :param key: The key of the config item.
    :param value: The value of the config item, which needs to be JSON serializable.
    :return: The created or updated config item or ``None`` if either the given key or
        value are invalid.
    """
    config_cls = configs[current_app.env]

    for config_key in dir(config_cls):
        # Check if the given key exists at all in the current config class.
        if config_key.isupper() and config_key == key:
            # Check if the given value matches the default value specified in the config
            # class. If so, remove the corresponding config item in the database if it
            # exists, otherwise update or create it.
            if getattr(config_cls, key) == value:
                remove_sys_config(key)
            else:
                return ConfigItem.update_or_create(key=key, value=value)

    return None


def remove_sys_config(key):
    """Remove a global config item from the database.

    :param key: The key of the config item.
    :return: ``True`` if the config item was deleted successfully, ``False`` if no such
        item exists.
    """
    config_item = ConfigItem.query.filter(
        ConfigItem.key == key, ConfigItem.user_id.is_(None)
    ).first()

    if config_item is not None:
        db.session.delete(config_item)
        return True

    return False
