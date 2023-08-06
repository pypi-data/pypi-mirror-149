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
from flask import send_file
from flask_login import current_user
from flask_login import login_required

from kadi.lib.api.blueprint import bp
from kadi.lib.api.core import internal
from kadi.lib.api.core import json_error_response
from kadi.lib.api.core import json_response
from kadi.lib.api.utils import create_pagination_data
from kadi.lib.conversion import normalize
from kadi.lib.db import get_class_by_tablename
from kadi.lib.permissions.core import has_permission
from kadi.lib.permissions.models import RoleRule
from kadi.lib.permissions.schemas import RoleRuleSchema
from kadi.lib.permissions.utils import get_group_roles
from kadi.lib.permissions.utils import get_role_rules
from kadi.lib.permissions.utils import permission_required
from kadi.lib.resources.api import get_selected_resources
from kadi.lib.storage.misc import create_misc_storage
from kadi.lib.web import paginated
from kadi.lib.web import qparam
from kadi.modules.groups.models import Group


@bp.get("/groups/<int:id>/image", v=None)
@permission_required("read", "group", "id")
@internal
def preview_group_image(id):
    """Preview a group's image thumbnail directly in the browser."""
    group = Group.query.get_active_or_404(id)

    if group.image_name:
        storage = create_misc_storage()
        filepath = storage.create_filepath(str(group.image_name))

        if storage.exists(filepath):
            return send_file(
                filepath,
                mimetype="image/jpeg",
                download_name=f"{group.identifier}.jpg",
            )

    return json_error_response(404)


@bp.get("/groups/<int:id>/rules", v=None)
@permission_required("members", "group", "id")
@internal
@paginated
def get_group_role_rules(id, page, per_page):
    """Get all role rules of a group."""
    group = Group.query.get_active_or_404(id)
    role_rules = (
        get_role_rules("group", group.id)
        .order_by(RoleRule.created_at.desc())
        .paginate(page, per_page, False)
    )

    data = {
        "items": RoleRuleSchema(many=True).dump(role_rules.items),
        **create_pagination_data(
            role_rules.total, page, per_page, "api.get_group_role_rules", id=group.id
        ),
    }
    return json_response(200, data)


@bp.get("/groups/select", v=None)
@login_required
@internal
@qparam("page", default=1, parse=int)
@qparam("term", parse=normalize)
@qparam("exclude", multiple=True, parse=int)
@qparam("action", multiple=True)
@qparam("resource_type")
@qparam("resource_id", default=None, parse=int)
def select_groups(qparams):
    """Search groups in dynamic selections.

    Uses :func:`kadi.lib.resources.api.get_selected_resources`.
    """
    exclude = qparams["exclude"]
    object_name = qparams["resource_type"]
    object_id = qparams["resource_id"]

    # If applicable, exclude groups that already have any role in the specified
    # resource.
    if object_name in ["record", "collection", "template"] and object_id is not None:
        model = get_class_by_tablename(object_name)
        resource = model.query.get(object_id)

        if (
            resource is not None
            and getattr(resource, "state", "active") == "active"
            and has_permission(current_user, "read", object_name, object_id)
        ):
            group_ids_query = get_group_roles(
                object_name, object_id=object_id
            ).with_entities(Group.id)
            exclude += [g.id for g in group_ids_query]

    return get_selected_resources(
        Group,
        page=qparams["page"],
        filter_term=qparams["term"],
        exclude=exclude,
        actions=qparams["action"],
    )
