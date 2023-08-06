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
from elasticsearch_dsl import Q
from flask_login import current_user
from sqlalchemy.exc import IntegrityError

from .models import Collection
from kadi.ext.db import db
from kadi.lib.conversion import strip_markdown
from kadi.lib.db import acquire_lock
from kadi.lib.db import update_object
from kadi.lib.exceptions import KadiPermissionError
from kadi.lib.permissions.core import add_role
from kadi.lib.permissions.core import delete_permissions
from kadi.lib.permissions.core import get_permitted_objects
from kadi.lib.permissions.core import has_permission
from kadi.lib.permissions.core import setup_permissions
from kadi.lib.resources.utils import search_resources
from kadi.lib.revisions.core import create_revision
from kadi.lib.revisions.core import delete_revisions
from kadi.lib.tags.models import Tag
from kadi.lib.utils import signal_resource_change


def create_collection(
    *,
    identifier,
    title,
    creator=None,
    description="",
    visibility="private",
    state="active",
    tags=None,
):
    """Create a new collection.

    This will also create all default permissions of the collection.

    Note that this function issues a database commit or rollback.

    :param identifier: See :attr:`.Collection.identifier`.
    :param title: See :attr:`.Collection.title`.
    :param creator: (optional) The user that created the collection. Defaults to the
        current user.
    :param description: (optional) See :attr:`.Collection.description`.
    :param visibility: (optional) See :attr:`.Collection.visibility`.
    :param state: (optional) See :attr:`.Collection.state`.
    :param tags: (optional) A list of tag names to tag the collection with. See also
        :class:`.Tag`.
    :return: The created collection or ``None`` if the collection could not be created.
    """
    creator = creator if creator is not None else current_user

    collection = Collection.create(
        identifier=identifier,
        title=title,
        creator=creator,
        description=description,
        plain_description=strip_markdown(description),
        visibility=visibility,
        state=state,
    )

    try:
        db.session.flush()
    except IntegrityError:
        db.session.rollback()
        return None

    if tags is not None and not collection.set_tags(tags):
        db.session.rollback()
        return None

    setup_permissions("collection", collection.id)
    add_role(creator, "collection", collection.id, "admin")

    revision_created = create_revision(collection, user=creator)
    db.session.commit()

    if revision_created:
        signal_resource_change(collection, user=creator, created=True)

    return collection


def update_collection(collection, tags=None, **kwargs):
    r"""Update an existing collection.

    Note that this function issues a database commit or rollback.

    :param collection: The collection to update.
    :param tags: (optional) A list of tag names to tag the collection with. See also
        :class:`.Tag`.
    :param \**kwargs: Keyword arguments that will be passed to
        :func:`kadi.lib.db.update_object`.
    :return: ``True`` if the collection was updated successfully, ``False`` otherwise.
    """
    if collection.state != "active":
        return False

    if "description" in kwargs:
        kwargs["plain_description"] = strip_markdown(kwargs["description"])

    update_object(collection, **kwargs)

    try:
        db.session.flush()
    except IntegrityError:
        db.session.rollback()
        return False

    if tags is not None and not collection.set_tags(tags):
        db.session.rollback()
        return False

    revision_created = create_revision(collection)
    db.session.commit()

    if revision_created:
        signal_resource_change(collection)

    return True


def delete_collection(collection):
    """Delete an existing collection.

    This will perform a soft deletion, i.e. the collection's state will be set to
    ``"deleted"``.

    Note that this function issues a database commit.

    :param collection: The collection to delete.
    """
    revision_created = False

    if collection.state == "active":
        collection.state = "deleted"
        revision_created = create_revision(collection)

    db.session.commit()

    if revision_created:
        signal_resource_change(collection)


def restore_collection(collection):
    """Restore a deleted collection.

    Note that this function issues a database commit.

    :param collection: The collection to restore.
    """
    revision_created = False

    if collection.state == "deleted":
        collection.state = "active"
        revision_created = create_revision(collection)

    db.session.commit()

    if revision_created:
        signal_resource_change(collection)


def purge_collection(collection):
    """Purge an existing collection.

    This will completely delete the collection from the database.

    :param collection: The collection to purge.
    """
    delete_revisions(collection)
    delete_permissions("collection", collection.id)

    db.session.delete(collection)


def link_collections(parent_collection, child_collection, user=None):
    """Link two collections together.

    Note that this function acquires a lock on the given collections.

    :param parent_collection: The parent collection.
    :param child_collection: The child collection.
    :param user: (optional) The user performing the link operation. Defaults to the
        current user.
    :return: ``True`` if the collections were linked successfully, ``False`` if both
        given collections refer to the same object, if the given child collection
        already has a parent or if the given child collection is already a parent of the
        parent collection.
    :raises KadiPermissionError: If the user performing the operation does not have the
        necessary permissions.
    """
    user = user if user is not None else current_user

    if not has_permission(
        user, "link", "collection", parent_collection.id
    ) or not has_permission(user, "link", "collection", child_collection.id):
        raise KadiPermissionError("No permission to link collections.")

    # Acquire a lock on the given collections to ensure that all cycle checks use up to
    # date values.
    parent_collection = acquire_lock(parent_collection)
    child_collection = acquire_lock(child_collection)

    if child_collection == parent_collection:
        return False

    if child_collection.parent_id:
        return False

    # Check that the child collection is not already a parent of the parent collection
    # to prevent cycles.
    current_parent = parent_collection.parent

    while current_parent is not None:
        if current_parent == child_collection:
            return False

        current_parent = current_parent.parent

    # No need for further checks, since we already know the collection does not have any
    # parent.
    parent_collection.children.append(child_collection)
    return True


def search_collections(
    query,
    sort="_score",
    visibility=None,
    tags=None,
    tag_operator="or",
    page=1,
    per_page=10,
):
    """Search for and filter all collections that the current user can read.

    Uses :func:`kadi.lib.resources.utils.search_resources`.

    :param query: The search query as string to search for the title, identifier and
        plain description of the collection.
    :param sort: (optional) See :func:`kadi.lib.resources.utils.search_resources`.
    :param visibility: (optional) A value to filter the visibility of the searched
        collections with. One of ``"private"`` or ``"public"``.
    :param tags: (optional) A list of tag names to filter the collections with before
        searching. All given tags are filtered using the operator specified via
        ``tag_operator``.
    :param tag_operator: (optional) The operator to filter the tags with. One of
        ``"or"`` or ``"and"``.
    :param page: (optional) See :func:`kadi.lib.resources.utils.search_resources`.
    :param per_page: (optional) See :func:`kadi.lib.resources.utils.search_resources`.
    :return: The search results as returned by
        :func:`kadi.lib.resources.utils.search_resources`.
    """
    collections_query = get_permitted_objects(
        current_user, "read", "collection"
    ).filter(Collection.state == "active")

    if visibility in ["private", "public"]:
        collections_query = collections_query.filter(
            Collection.visibility == visibility
        )

    if tags:
        if tag_operator == "and":
            for tag in tags:
                collections_query = collections_query.filter(
                    Collection.tags.any(Tag.name == tag)
                )
        else:
            collections_query = collections_query.join(Collection.tags).filter(
                Tag.name.in_(tags)
            )

    collection_ids = [c.id for c in collections_query.with_entities(Collection.id)]

    if query:
        base_query_params = {
            "query": query,
            "fields": [
                "identifier",
                "identifier.text",
                "title",
                "title.text",
                "plain_description",
            ],
        }

        exact_query = Q("multi_match", boost=5, **base_query_params)
        fuzzy_query = Q("multi_match", fuzziness="AUTO:2,6", **base_query_params)

        query = Q("bool", should=[exact_query, fuzzy_query])

    return search_resources(
        Collection,
        query=query,
        sort=sort,
        filter_ids=collection_ids,
        page=page,
        per_page=per_page,
    )
