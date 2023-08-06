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

/** Upload provider for direct uploads. */
export default class DirectUpload extends BaseUpload {
  constructor(uploadEndpoint, onSuccess, onError) {
    super('direct');
    this.uploadEndpoint = uploadEndpoint;
    this.successCallback = onSuccess;
    this.errorCallback = onError;
  }

  create(config) {
    const upload = super.create(config);
    upload.file = config.file;
    upload.size = config.size;
    return upload;
  }

  async upload(upload) {
    const formData = new FormData();

    formData.append('storage_type', upload.storageType);
    formData.append('replace_file', upload.forceReplace || false);
    formData.append('name', upload.file.name);
    formData.append('size', upload.file.size);
    formData.append('blob', upload.file);

    const uploadState = await this.uploadFile(upload, formData);

    if (uploadState.retryUpload) {
      formData.set('replace_file', uploadState.replaceFile);
      await this.uploadFile(upload, formData);
    }
  }

  /* eslint-disable class-methods-use-this */
  // eslint-disable-next-line no-unused-vars
  cancel(upload) {
    // We have nothing storage specific to cancel here.
    return Promise.resolve();
  }

  async uploadFile(upload, formData) {
    // The cancel token allows us to cancel an ongoing request.
    const source = axios.CancelToken.source();
    upload.source = source;

    const config = {
      onUploadProgress: (e) => {
        upload.progress = (e.loaded / e.total) * 100;
      },
      cancelToken: source.token,
    };

    const uploadState = {
      retryUpload: false,
      replaceFile: false,
    };

    try {
      const response = await axios.post(this.uploadEndpoint, formData, config);

      const data = response.data;
      upload.createdAt = data.created_at;
      upload.viewFileEndpoint = data._links.view;
      upload.state = 'completed';

      if (data._meta) {
        upload.replacedFile = data._meta.replaced_file || null;
      }

      this.successCallback(upload, data);
    } catch (error) {
      // Check if the request was canceled.
      if (axios.isCancel(error)) {
        return uploadState;
      }

      const errorResult = await this.errorCallback(error, upload);

      if (error.request.status === 409 && errorResult) {
        uploadState.replaceFile = true;
        uploadState.retryUpload = true;

        // eslint-disable-next-line require-atomic-updates
        upload.replacedFile = error.response.data.file;
      }
    } finally {
      // eslint-disable-next-line require-atomic-updates
      upload.source = null;
    }

    return uploadState;
  }
  /* eslint-enable class-methods-use-this */
}
