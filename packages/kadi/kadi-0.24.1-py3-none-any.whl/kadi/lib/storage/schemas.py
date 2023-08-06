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
from flask_babel import gettext as _
from marshmallow import fields
from marshmallow import ValidationError

from .core import get_storage
from kadi.lib.schemas import KadiSchema
from kadi.lib.storage.local import LocalStorage


def _validate_storage(value):
    if not get_storage(value):
        raise ValidationError(_("Not a valid storage type."))


class StorageSchema(KadiSchema):
    """Schema to represent storages.

    See :class:`.BaseStorage`.
    """

    storage_type = fields.String(
        load_default=LocalStorage.storage_type, validate=_validate_storage
    )

    storage_name = fields.String(dump_only=True)
