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
from flask import render_template
from flask_babel import gettext as _

from kadi.ext.db import db
from kadi.lib.tasks.models import Task


def create_notification_data(notification):
    """Create a notification suitable for presenting it to a client.

    :param notification: A :class:`.Notification` object.
    :return: A tuple containing the title and the HTML body of the notification.
    """
    title = body = notification.name

    # Task status notifications.
    if notification.name == "task_status":
        task = Task.query.get(notification.data["task_id"])
        task_meta = notification.data.get("task_meta")

        # Default task status notifications.
        title = _("Task")

        if task.state == "pending":
            body = _("Waiting for available resources...")
        elif task.state == "running":
            body = _("Task running...")
        elif task.state == "success":
            body = _("Task succeeded.")
        elif task.state == "failure":
            body = _("Task failed.")
        elif task.state == "revoked":
            body = _("Task revoked.")

        # Publish resource task.
        if task.name == "kadi.resources.publish_resource":
            title = _("Publish resource")

            if task.state == "running":
                body = render_template(
                    "notifications/snippets/publish_resource_running.html",
                    progress=task.progress,
                )
            elif task.state in ["success", "failure"]:
                template = (
                    task.result.get("template") if task.result is not None else None
                )
                body = template if template is not None else _("Unexpected error.")

        # Check if the additional task notification metadata contains a custom title,
        # which overwrites previous values.
        if isinstance(task_meta, dict) and "task_title" in task_meta:
            title = task_meta["task_title"]

        title = f"{title} ({task.pretty_state})"

    return title, body


def dismiss_notification(notification):
    """Dismiss a notification.

    If the notification is of type ``"task_status"``, the referenced task will be
    revoked as well.

    :param notification: The :class:`.Notification` to dismiss.
    """
    if notification.name == "task_status":
        task = Task.query.get(notification.data["task_id"])
        task.revoke()

    db.session.delete(notification)
