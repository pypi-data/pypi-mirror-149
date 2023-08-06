/* Copyright 2021 Karlsruhe Institute of Technology
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License. */

import BaseUpload from 'scripts/lib/upload/core.js';

/** Upload provider for chunked uploads. */
export default class ChunkedUpload extends BaseUpload {
  constructor(newUploadEndpoint, getUploadsEndpoint, onSuccess, onError, onCancel, onPause) {
    super('chunked', true);
    this.newUploadEndpoint = newUploadEndpoint;
    this.getUploadsEndpoint = getUploadsEndpoint;
    this.successCallback = onSuccess;
    this.errorCallback = onError;
    this.cancelCallback = onCancel;
    this.pauseCallback = onPause;
  }

  static initiateUpload(upload, endpoint = null) {
    let requestFunc = null;
    let _endpoint = endpoint;
    const data = {size: upload.size, storage: {storage_type: upload.storageType}};

    // Initial request to initiate the upload process and to retrieve the upload infos.
    if (!_endpoint) {
      requestFunc = axios.post;
      _endpoint = upload.newUploadEndpoint;
      data.name = upload.name;
    } else {
      requestFunc = axios.put;
    }

    return requestFunc(_endpoint, data)
      .then((response) => {
        const data = response.data;
        upload.id = data.id;
        upload.chunkSize = data._meta.chunk_size;
        upload.chunkCount = data.chunk_count;
        upload.createdAt = data.created_at;
        upload.uploadChunkEndpoint = data._actions.upload_chunk;
        upload.finishUploadEndpoint = data._actions.finish_upload;
        upload.deleteUploadEndpoint = data._actions.delete;
        upload.getStatusEndpoint = data._links.status;
      });
  }

  static findNextChunkIndex(upload) {
    let chunkIndex = null;
    for (let index = 0; index < upload.chunkCount; index++) {
      const found = upload.chunks.find((chunk) => chunk.index === index && chunk.state === 'active');

      if (!found) {
        chunkIndex = index;
        break;
      }
    }

    return chunkIndex;
  }

  static getTotalChunkSize(upload) {
    // eslint-disable-next-line no-param-reassign
    return upload.chunks.reduce((acc, chunk) => (chunk.state === 'active' ? acc += chunk.size : acc), 0);
  }

  static getUploadProgress(upload, additionalSize = 0) {
    // Special case for files with a size of 0.
    if (upload.size === 0) {
      return (upload.chunks.length > 0 && upload.chunks[0].state === 'active') ? 100 : 0;
    }
    return ((ChunkedUpload.getTotalChunkSize(upload) + additionalSize) / upload.size) * 100;
  }

  create(config) {
    const upload = super.create(config);

    upload.file = config.file;
    upload.size = config.size;
    upload.chunks = [];
    upload.chunkSize = null;
    upload.chunkCount = null;
    upload.uploadChunkEndpoint = null;
    upload.finishUploadEndpoint = null;
    upload.deleteUploadEndpoint = null;
    upload.getStatusEndpoint = null;
    upload.newUploadEndpoint = this.newUploadEndpoint;

    return upload;
  }

  async upload(upload) {
    // Check if the upload was already initiated. We could check any property that will be set from the backend.
    if (!upload.chunkCount) {
      try {
        await ChunkedUpload.initiateUpload(upload);
      } catch (error) {
        if (!await this.errorCallback(error, upload)) {
          return;
        }

        // Storage specific errors.
        if (error.request.status === 409) {
          try {
            // Restart the upload.
            await ChunkedUpload.initiateUpload(upload, error.response.data.file._actions.edit_data);

            // eslint-disable-next-line require-atomic-updates
            upload.replacedFile = error.response.data.file;
          } catch (error) {
            await this.errorCallback(error, upload);
          }
        }
      }
    }

    if (!await this.uploadChunks(upload)) {
      return;
    }

    /* eslint-disable require-atomic-updates */
    upload.state = 'processing';

    try {
      await axios.post(upload.finishUploadEndpoint);
    } catch (error) {
      upload.state = 'uploading';

      if (error.request.status === 413) {
        // Use the error message from the backend.
        kadi.alert(error.response.data.description, {type: 'warning'});
      } else {
        kadi.alert($t('Error finishing upload.'), {request: error.request});
      }
      this.pauseCallback(upload);
      return;
    }

    this.finalizeUpload(upload);
    /* eslint-disable require-atomic-updates */
  }

  /* eslint-disable class-methods-use-this */
  cancel(upload) {
    if (upload.deleteUploadEndpoint) {
      return axios.delete(upload.deleteUploadEndpoint);
    }

    return Promise.resolve();
  }

  isPausable(upload) {
    return ['pending', 'uploading'].includes(upload.state);
  }

  isResumable(upload) {
    // Special case for files with a size of 0.
    if (upload.size === 0) {
      return upload.state === 'paused'
        && (upload.file !== null
        || (upload.chunks.length > 0 && upload.chunks[0].state === 'active'));
    }

    return upload.state === 'paused'
      && (upload.file !== null || ChunkedUpload.getTotalChunkSize(upload) === upload.size);
  }

  loadUploads() {
    return axios.get(this.getUploadsEndpoint)
      .then((response) => {
        const uploads = [];

        response.data.items.forEach((upload) => {
          upload.storageType = upload.storage.storage_type;
          upload.uploadType = upload.upload_type;
          upload.replacedFile = upload.file;
          upload.chunkCount = upload.chunk_count;
          upload.createdAt = upload.created_at;
          upload.uploadChunkEndpoint = upload._actions.upload_chunk;
          upload.finishUploadEndpoint = upload._actions.finish_upload;
          upload.deleteUploadEndpoint = upload._actions.delete;
          upload.getStatusEndpoint = upload._links.status;
          upload.chunkSize = response.data._meta.chunk_size;
          upload.progress = ChunkedUpload.getUploadProgress(upload);
          upload.file = null;
          upload.source = null;
          upload.viewFileEndpoint = null;

          if (upload.state === 'active') {
            upload.state = 'paused';
          } else if (upload.state === 'processing') {
            this.finalizeUpload(upload);
          }

          uploads.push(upload);
        });

        return uploads;
      });
  }

  uploadChunk(upload, blob, index) {
    // The chunk and its metadata is uploaded using multipart/form-data encoding.
    const chunkFormData = new FormData();
    chunkFormData.append('blob', blob);
    chunkFormData.append('index', index);
    chunkFormData.append('size', blob.size);

    // The cancel token allows us to cancel an ongoing request.
    const source = axios.CancelToken.source();
    upload.source = source;

    const config = {
      onUploadProgress: (e) => {
        // Stop the progress from jumping around when pausing the upload.
        upload.progress = Math.max(
          ChunkedUpload.getUploadProgress(upload, Math.min(e.loaded, blob.size)),
          upload.progress,
        );
      },
      cancelToken: source.token,
    };

    return axios.put(upload.uploadChunkEndpoint, chunkFormData, config)
      .then((response) => {
        upload.chunks = response.data.chunks;
        upload.progress = ChunkedUpload.getUploadProgress(upload);
      })
      .finally(() => upload.source = null);
  }

  async uploadChunks(upload) {
    const errorMsg = $t('Error uploading chunk.');

    // Loop until all chunks have been uploaded successfully. Currently, the chunks are uploaded sequentially.
    while (true) {
      // Check if the upload state was modified from outside.
      if (upload.state !== 'uploading') {
        return false;
      }

      // Find the next chunk index to upload.
      const chunkIndex = ChunkedUpload.findNextChunkIndex(upload);

      // No index for the next chunk could be found, so we are done uploading.
      if (chunkIndex === null) {
        break;
      }

      const start = chunkIndex * upload.chunkSize;
      const end = Math.min(start + upload.chunkSize, upload.size);
      const blob = upload.file.slice(start, end);
      let timeout = 0;

      // Loop until the current chunk was uploaded successfully or the upload cannot be completed.
      while (true) {
        // Check if the upload state was modified from outside.
        if (upload.state !== 'uploading') {
          return false;
        }

        try {
          /* eslint-disable no-await-in-loop */
          await this.uploadChunk(upload, blob, chunkIndex);
          break;
        } catch (error) {
          // Check if the request was canceled.
          if (axios.isCancel(error)) {
            return false;
          }

          // There is no point in retrying when some quota was exceeded.
          if (error.request.status === 413) {
            // Use the error message from the backend.
            kadi.alert(error.response.data.description, {type: 'warning'});
            this.pauseCallback(upload);
            return false;
          }

          timeout += 5000;

          const timeoutMsg = $t('Retrying in {{timeout}} seconds.', {timeout: timeout / 1000});
          kadi.alert(`${errorMsg} ${timeoutMsg}`, {request: error.request, timeout});

          await kadi.utils.sleep(timeout);
          /* eslint-enable no-await-in-loop */
        }
      }
    }

    return true;
  }

  finalizeUpload(upload) {
    let timeout = 0;

    const _updateStatus = () => {
      if (timeout < 30000) {
        timeout += 1000;
      }

      axios.get(upload.getStatusEndpoint)
        .then((response) => {
          const data = response.data;
          if (data._meta.file) {
            // The upload finished successfully.
            upload.state = 'completed';
            upload.viewFileEndpoint = data._meta.file._links.view;

            this.successCallback(upload, data);
          } else if (data._meta.error) {
            // The upload finished with an error.
            kadi.alert(data._meta.error);

            this.cancelCallback(true, upload);
          } else {
            // The upload is still processing.
            window.setTimeout(_updateStatus, timeout);
          }
        })
        .catch((error) => {
          kadi.alert($t('Error updating upload status.'), {request: error.request});
        });
    };

    window.setTimeout(_updateStatus, 100);
  }
  /* eslint-enable class-methods-use-this */
}
