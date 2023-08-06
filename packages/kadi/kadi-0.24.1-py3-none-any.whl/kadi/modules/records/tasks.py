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
from flask_login import current_user
from sqlalchemy.exc import IntegrityError

import kadi.lib.constants as const
from .core import purge_record
from .models import Record
from .models import Upload
from .uploads import merge_chunks
from kadi.ext.celery import celery
from kadi.ext.db import db
from kadi.lib.exceptions import KadiChecksumMismatchError
from kadi.lib.exceptions import KadiFilesizeExceededError
from kadi.lib.exceptions import KadiFilesizeMismatchError
from kadi.lib.tasks.core import launch_task
from kadi.lib.tasks.models import Task


@celery.task(
    name="kadi.records.merge_chunks", soft_time_limit=const.ONE_HOUR, bind=True
)
def _merge_chunks_task(self, upload_id, **kwargs):
    task = Task.query.get(self.request.id)
    upload = Upload.query.get(upload_id)

    # Check if the upload was not deleted before the task actually started, which will
    # also be the case if a file to be replaced by the upload was deleted.
    if task.is_revoked or upload is None or upload.state != "processing":
        return None

    file = None

    try:
        file = merge_chunks(upload, task=task)

        if file is not None:
            task.result = {"file": str(file.id)}
        else:
            task.state = "failure"
            task.result = {"error": "File has already been deleted."}

    # Catches time limit exceeded exceptions as well.
    except Exception as e:
        db.session.rollback()
        task.state = "failure"

        if isinstance(
            e,
            (
                KadiFilesizeExceededError,
                KadiFilesizeMismatchError,
                KadiChecksumMismatchError,
            ),
        ):
            task.result = {"error": str(e)}
        elif isinstance(e, IntegrityError):
            task.result = {"error": "A file with that name already exists."}
        else:
            current_app.logger.exception(e)
            task.result = {"error": "Internal server error."}

    db.session.commit()
    return str(file.id) if file is not None else None


def start_merge_chunks_task(upload, user=None):
    """Merge the chunks of a local file upload in a background task.

    Uses :func:`kadi.modules.records.files.merge_chunks`. The created task will be kept
    in the database.

    Note that this function issues one or more database commits.

    :param upload: The upload that the chunks belong to.
    :param user: (optional) The user that started the task. Defaults to the current
        user.
    :return: The new task object if the task was started successfully, ``None``
        otherwise.
    """
    user = user if user is not None else current_user

    return launch_task(
        "kadi.records.merge_chunks", args=(str(upload.id),), user=user, keep=True
    )


@celery.task(name="kadi.records.purge_record")
def _purge_record_task(record_id, **kwargs):
    record = Record.query.get(record_id)

    try:
        purge_record(record)
    except Exception as e:
        current_app.logger.exception(e)

        db.session.rollback()
        # In case the state of the record was set to "purged" before, make sure to reset
        # it so another attempt can be made to delete it as part of the periodic task.
        record.state = "deleted"

    db.session.commit()


def start_purge_record_task(record):
    """Purge an existing record in a background task.

    Uses :func:`kadi.modules.records.core.purge_record`.

    :param record: The record to purge.
    """
    return launch_task("kadi.records.purge_record", args=(record.id,))
