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
from flask import current_app
from flask import render_template
from flask_login import current_user
from flask_login import login_required

from kadi.lib.api.blueprint import bp
from kadi.lib.api.core import internal
from kadi.lib.api.core import json_error_response
from kadi.lib.api.core import json_response
from kadi.lib.conversion import clamp
from kadi.lib.conversion import normalize
from kadi.lib.conversion import parse_json_object
from kadi.lib.conversion import strip
from kadi.lib.db import escape_like
from kadi.lib.permissions.core import get_permitted_objects
from kadi.lib.permissions.core import has_permission
from kadi.lib.permissions.utils import permission_required
from kadi.lib.resources.api import get_selected_resources
from kadi.lib.utils import compact_json
from kadi.lib.web import download_bytes
from kadi.lib.web import qparam
from kadi.lib.web import url_for
from kadi.modules.collections.models import Collection
from kadi.modules.records.export import get_export_data
from kadi.modules.records.files import (
    download_temporary_file as _download_temporary_file,
)
from kadi.modules.records.files import get_permitted_files
from kadi.modules.records.links import get_record_links_graph as _get_record_links_graph
from kadi.modules.records.models import File
from kadi.modules.records.models import Record
from kadi.modules.records.models import RecordLink
from kadi.modules.records.models import TemporaryFile
from kadi.modules.records.previews import get_preview_data
from kadi.modules.records.previews import preview_file as _preview_file


@bp.get("/records/<int:id>/export/internal/<export_type>", v=None)
@permission_required("read", "record", "id")
@internal
@qparam("preview", default=False, parse=bool)
@qparam("download", default=False, parse=bool)
@qparam("filter", default=lambda: {}, parse=parse_json_object)
def get_record_export_internal(id, export_type, qparams):
    """Export a record in a specific format."""
    record = Record.query.get_active_or_404(id)
    export_types = current_app.config["EXPORT_TYPES"]["record"]

    if export_type not in export_types:
        return json_error_response(404)

    if export_type == "json" or qparams["preview"] or qparams["download"]:
        file_ext = "png" if export_type == "qr" else export_type
        return download_bytes(
            get_export_data(record, export_type, export_filter=qparams["filter"]),
            f"{record.identifier}.{file_ext}",
            as_attachment=qparams["download"],
        )

    return json_response(
        200,
        body=url_for(
            "api.get_record_export_internal",
            id=record.id,
            export_type=export_type,
            preview=True,
            filter=compact_json(qparams["filter"]),
        ),
    )


@bp.get("/records/<int:id>/records/graph", v=None)
@permission_required("read", "record", "id")
@internal
@qparam("depth", default=1, parse=[int, lambda x: clamp(x, 1, 3)])
@qparam("direction")
def get_record_links_graph(id, qparams):
    """Get all links of a record for visualizing them in a graph."""
    record = Record.query.get_active_or_404(id)

    data = _get_record_links_graph(record, qparams["depth"], qparams["direction"])
    return json_response(200, data)


@bp.get("/records/<int:record_id>/files/<uuid:file_id>/preview", v=None)
@permission_required("read", "record", "record_id")
@internal
def get_file_preview(record_id, file_id):
    """Get the preview data of a file.

    The actual preview data may either consist of a URL or the preview data itself,
    depending on the preview type. In the first case, a browser may be able to directly
    preview the file using the returned URL.
    """
    record = Record.query.get_active_or_404(record_id)
    file = record.active_files.filter(File.id == file_id).first_or_404()

    preview_data = get_preview_data(file)

    if preview_data is None:
        return json_error_response(404)

    return json_response(200, {"type": preview_data[0], "data": preview_data[1]})


@bp.get("/records/<int:record_id>/files/<uuid:file_id>/preview/file", v=None)
@permission_required("read", "record", "record_id")
@internal
def preview_file(record_id, file_id):
    """Preview a file directly in the browser."""
    record = Record.query.get_active_or_404(record_id)
    file = record.active_files.filter(File.id == file_id).first_or_404()

    if file.magic_mimetype in [
        *current_app.config["IMAGE_MIMETYPES"],
        "application/pdf",
    ]:
        return _preview_file(file)

    return json_error_response(404)


@bp.get("/records/<int:record_id>/temporary-files/<uuid:temporary_file_id>", v=None)
@permission_required("read", "record", "record_id")
@internal
def download_temporary_file(record_id, temporary_file_id):
    """Download a temporary file."""
    record = Record.query.get_active_or_404(record_id)
    temporary_file = record.temporary_files.filter(
        TemporaryFile.id == temporary_file_id, TemporaryFile.state == "active"
    ).first_or_404()

    return _download_temporary_file(temporary_file)


@bp.get("/records/select", v=None)
@login_required
@internal
@qparam("page", default=1, parse=int)
@qparam("term", parse=normalize)
@qparam("exclude", multiple=True, parse=int)
@qparam("action", multiple=True)
@qparam("collection", default=None, parse=int)
def select_records(qparams):
    """Search records in dynamic selections.

    Uses :func:`kadi.lib.resources.api.get_selected_resources`.
    """
    exclude = qparams["exclude"]
    collection_id = qparams["collection"]

    # If applicable, exclude records that are already linked to the collection with the
    # given ID.
    if collection_id is not None:
        collection = Collection.query.get_active(collection_id)

        if collection is not None and has_permission(
            current_user, "read", "collection", collection.id
        ):
            record_ids_query = collection.records.filter(
                Record.state == "active"
            ).with_entities(Record.id)
            exclude += [r.id for r in record_ids_query]

    return get_selected_resources(
        Record,
        page=qparams["page"],
        filter_term=qparams["term"],
        exclude=exclude,
        actions=qparams["action"],
    )


@bp.get("/records/types/select", v=None)
@login_required
@internal
@qparam("page", default=1, parse=int)
@qparam("term", parse=normalize)
def select_record_types(qparams):
    """Search record types in dynamic selections.

    Similar to :func:`kadi.lib.resources.api.get_selected_resources`. Only the types of
    records the current user has read permission for are returned.
    """
    paginated_record_types = (
        get_permitted_objects(current_user, "read", "record")
        .filter(
            Record.state == "active",
            Record.type.is_not(None),
            Record.type.ilike(f"%{escape_like(qparams['term'])}%"),
        )
        .distinct()
        .order_by(Record.type)
        .with_entities(Record.type)
        .paginate(qparams["page"], 10, False)
    )

    data = {"results": [], "pagination": {"more": paginated_record_types.has_next}}
    for record_type in paginated_record_types.items:
        data["results"].append({"id": record_type[0], "text": record_type[0]})

    return json_response(200, data)


@bp.get("/records/mimetypes/select", v=None)
@login_required
@internal
@qparam("page", default=1, parse=int)
@qparam("term", parse=strip)
def select_mimetypes(qparams):
    """Search MIME types of record files in dynamic selections.

    Similar to :func:`kadi.lib.resources.api.get_selected_resources`. Only the MIME
    types of records the current user has read permission for are returned.
    """
    paginated_mimetypes = (
        get_permitted_objects(current_user, "read", "record")
        .join(Record.files)
        .filter(
            Record.state == "active",
            File.state == "active",
            File.mimetype.ilike(f"%{escape_like(qparams['term'])}%"),
        )
        .distinct()
        .order_by(File.mimetype)
        .with_entities(File.mimetype)
        .paginate(qparams["page"], 10, False)
    )

    data = {"results": [], "pagination": {"more": paginated_mimetypes.has_next}}
    for mimetype in paginated_mimetypes.items:
        data["results"].append({"id": mimetype[0], "text": mimetype[0]})

    return json_response(200, data)


@bp.get("/records/files/select", v=None)
@login_required
@internal
@qparam("page", default=1, parse=int)
@qparam("term", parse=strip)
@qparam("current_record", default=None, parse=int)
@qparam("images", default=False, parse=bool)
def select_files(qparams):
    """Search record files in dynamic selections.

    Similar to :func:`kadi.lib.resources.api.get_selected_resources`. Only the files of
    records the current user has read permission for are returned.
    """
    files_query = get_permitted_files(filter_term=qparams["term"])

    if qparams["images"]:
        files_query = files_query.filter(
            File.magic_mimetype.in_(current_app.config["IMAGE_MIMETYPES"])
        )

    order = [File.name]

    if qparams["current_record"] is not None:
        order.insert(0, Record.id != qparams["current_record"])

    paginated_files = files_query.order_by(*order).paginate(qparams["page"], 10, False)

    data = {"results": [], "pagination": {"more": paginated_files.has_next}}
    for file in paginated_files.items:
        data["results"].append(
            {
                "id": file.id,
                "text": file.name,
                "body": render_template(
                    "records/snippets/select_file.html",
                    file=file,
                    current_record=qparams["current_record"],
                ),
                "view_endpoint": url_for(
                    "records.view_file", record_id=file.record_id, file_id=file.id
                ),
                "preview_endpoint": url_for(
                    "api.preview_file", record_id=file.record_id, file_id=file.id
                ),
            }
        )

    return json_response(200, data)


@bp.get("/records/links/select", v=None)
@login_required
@internal
@qparam("page", default=1, parse=int)
@qparam("term", parse=strip)
def select_link_names(qparams):
    """Search the names of record links in dynamic selections.

    Similar to :func:`kadi.lib.resources.api.get_selected_resources`. Only the links of
    records the current user has read permission for are considered.
    """
    record_ids_query = (
        get_permitted_objects(current_user, "read", "record")
        .filter(Record.state == "active")
        .with_entities(Record.id)
    )

    paginated_record_links = (
        RecordLink.query.filter(
            RecordLink.record_from_id.in_(record_ids_query),
            RecordLink.record_to_id.in_(record_ids_query),
            RecordLink.name.ilike(f"%{escape_like(qparams['term'])}%"),
        )
        .distinct()
        .order_by(RecordLink.name)
        .with_entities(RecordLink.name)
        .paginate(qparams["page"], 10, False)
    )

    data = {"results": [], "pagination": {"more": paginated_record_links.has_next}}
    for record_link in paginated_record_links.items:
        data["results"].append({"id": record_link.name, "text": record_link.name})

    return json_response(200, data)
