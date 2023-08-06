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
from datetime import timedelta

from flask import current_app

from .files import remove_file
from .files import remove_temporary_file
from .models import File
from .models import TemporaryFile
from .models import Upload
from .uploads import remove_upload
from kadi.ext.db import db
from kadi.lib.utils import utcnow


def clean_files(inside_task=False):
    """Clean all deleted and/or expired uploads and/or files.

    Note that this function may issue one or more database commits.

    :param inside_task: (optional) A flag indicating whether the function is executed in
        a task. In that case, additional information will be logged.
    """

    # Delete expired and inactive uploads.
    active_expiration_date = utcnow() - timedelta(
        seconds=current_app.config["UPLOADS_MAX_AGE"]
    )
    # Leave inactive uploads intact for at least a small amount of time, so their status
    # can always be queried in case the upload required a task for processing it and
    # something went wrong.
    inactive_expiration_date = utcnow() - timedelta(minutes=5)
    uploads = Upload.query.filter(
        db.or_(
            db.and_(
                Upload.state == "active", Upload.last_modified < active_expiration_date
            ),
            db.and_(
                Upload.state == "inactive",
                Upload.last_modified < inactive_expiration_date,
            ),
        )
    )

    if inside_task and uploads.count() > 0:
        current_app.logger.info(
            f"Deleting {uploads.count()} expired or inactive upload(s)."
        )

    for upload in uploads:
        remove_upload(upload)

    # Delete expired inactive files.
    expiration_date = utcnow() - timedelta(
        seconds=current_app.config["INACTIVE_FILES_MAX_AGE"]
    )
    files = File.query.filter(
        File.state == "inactive", File.last_modified < expiration_date
    )

    if inside_task and files.count() > 0:
        current_app.logger.info(f"Deleting {files.count()} inactive file(s).")

    for file in files:
        remove_file(file, delete_from_db=False)

    # Delete expired temporary files.
    expiration_date = utcnow() - timedelta(
        seconds=current_app.config["TEMPORARY_FILES_MAX_AGE"]
    )
    temporary_files = TemporaryFile.query.filter(
        TemporaryFile.last_modified < expiration_date
    )

    if inside_task and temporary_files.count() > 0:
        current_app.logger.info(
            f"Deleting {temporary_files.count()} expired temporary file(s)."
        )

    for temporary_file in temporary_files:
        remove_temporary_file(temporary_file)
