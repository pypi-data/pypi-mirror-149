<!-- Copyright 2020 Karlsruhe Institute of Technology
   -
   - Licensed under the Apache License, Version 2.0 (the "License");
   - you may not use this file except in compliance with the License.
   - You may obtain a copy of the License at
   -
   -     http://www.apache.org/licenses/LICENSE-2.0
   -
   - Unless required by applicable law or agreed to in writing, software
   - distributed under the License is distributed on an "AS IS" BASIS,
   - WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   - See the License for the specific language governing permissions and
   - limitations under the License. -->

<template>
  <div>
    <div class="modal" tabindex="-1" ref="replaceDialog">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-body" ref="replaceDialogText"></div>
          <div class="modal-footer d-flex justify-content-between">
            <div class="form-check form-check-inline">
              <input type="checkbox" class="form-check-input" :id="`apply-all-${suffix}`" v-model="replaceApplyAll">
              <label class="form-check-label" :for="`apply-all-${suffix}`">{{ $t('Apply to all') }}</label>
            </div>
            <div>
              <button type="button"
                      class="btn btn-sm btn-light btn-modal"
                      data-dismiss="modal"
                      ref="replaceDialogBtnNo">
                {{ $t('No') }}
              </button>
              <button type="button"
                      class="btn btn-sm btn-primary btn-modal"
                      data-dismiss="modal"
                      ref="replaceDialogBtnYes">
                {{ $t('Yes') }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="row align-items-center mb-2">
      <div class="col-lg-8 mb-2 mb-lg-0">
        <slot></slot>
      </div>
      <div class="col-lg-4 d-flex align-items-center mb-2 mb-lg-0">
        <span class="text-muted flex-shrink-0 mr-2">{{ $t('Storage type:') }}</span>
        <select class="custom-select custom-select-sm" v-model="selectedStorage">
          <option v-for="storageType in storageTypes" :value="storageType.id" :key="storageType.id">
            {{ storageType.title }}
          </option>
        </select>
      </div>
    </div>
    <upload-dropzone @add-file="addFile"></upload-dropzone>
    <input type="file" class="input" @change="resumeFileInputChange" ref="resumeFileInput">
    <div class="card bg-light py-2 px-4 mt-4 mb-3" v-if="uploads.length > 0">
      <div class="form-row align-items-center">
        <div class="col-xl-8">
          {{ uploadsCompletedText }}
          <i class="fa-solid fa-check fa-sm ml-2" v-if="completedUploadsCount === uploads.length"></i>
        </div>
        <div class="col-xl-2 d-xl-flex justify-content-end">
          <small class="text-muted">{{ totalUploadSize | filesize }}</small>
        </div>
        <div class="col-xl-2 d-xl-flex justify-content-end">
          <div class="btn-group btn-group-sm">
            <button type="button"
                    class="btn btn-primary"
                    :title="$t('Resume all uploads')"
                    :disabled="!uploadsResumable"
                    @click="resumeUploads()">
              <i class="fa-solid fa-play"></i>
            </button>
            <button type="button"
                    class="btn btn-primary"
                    :title="$t('Pause all uploads')"
                    :disabled="!uploadsPausable"
                    @click="pauseUploads()">
              <i class="fa-solid fa-pause"></i>
            </button>
            <button type="button"
                    class="btn btn-primary"
                    :title="$t('Cancel all uploads')"
                    :disabled="!uploadsCancelable"
                    @click="cancelUploads(false)">
              <i class="fa-solid fa-ban"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
    <div class="card"
         v-for="(upload, index) in paginatedUploads"
         :class="{'mb-3': index < uploads.length - 1}"
         :key="upload.id">
      <div class="card-body py-2">
        <div class="form-row align-items-center" :class="{'mb-2': upload.state !== 'completed'}">
          <div class="col-xl-8">
            <strong v-if="upload.state === 'completed'">
              <a :href="upload.viewFileEndpoint" v-if="upload.viewFileEndpoint">{{ upload.name }}</a>
              <span v-else>{{ upload.name }}</span>
            </strong>
            <span class="text-muted" v-else>{{ upload.name }}</span>
          </div>
          <div class="col-xl-2 d-xl-flex justify-content-end">
            <small class="text-muted">{{ upload.size | filesize }}</small>
          </div>
          <div class="col-xl-2 d-xl-flex justify-content-end">
            <span class="badge badge-primary">{{ stateNames[upload.state] }}</span>
          </div>
        </div>
        <div class="form-row align-items-center" v-if="upload.state !== 'completed'">
          <div class="col-xl-10 py-1">
            <div class="progress border border-muted" style="height: 17px;">
              <div class="progress-bar" :style="{width: Math.floor(upload.progress) + '%'}">
                {{ Math.floor(upload.progress) }}%
              </div>
            </div>
          </div>
          <div class="col-xl-2 mt-2 mt-xl-0 d-xl-flex justify-content-end">
            <i class="fa-solid fa-circle-notch fa-spin" v-if="upload.state === 'processing'"></i>
            <div class="btn-group btn-group-sm">
              <button type="button"
                      class="btn btn-light"
                      :title="$t('Pause upload')"
                      @click="pauseUploads(upload)"
                      v-if="supportsResuming(upload) && isPausable(upload)">
                <i class="fa-solid fa-pause"></i>
              </button>
              <button type="button"
                      class="btn btn-light"
                      :title="$t('Resume upload')"
                      @click="resumeUploads(upload)"
                      v-if="supportsResuming(upload) && upload.state === 'paused'">
                <i class="fa-solid fa-play" v-if="isResumable(upload)"></i>
                <i class="fa-solid fa-folder-open" v-else></i>
              </button>
              <button type="button"
                      class="btn btn-light"
                      :title="$t('Cancel upload')"
                      @click="cancelUploads(false, upload)"
                      v-if="['pending', 'paused', 'uploading'].includes(upload.state)">
                <i class="fa-solid fa-ban"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
      <div class="card-footer py-1" v-if="upload.replacedFile !== null || upload.createdAt !== null">
        <div class="d-flex justify-content-between">
          <div>
            <div v-if="upload.replacedFile !== null">
              <span class="text-muted">{{ $t('Replaces') }}</span>
              <a class="text-muted" :href="upload.replacedFile._links.view">
                <strong>{{ upload.replacedFile.name }}</strong>
              </a>
            </div>
          </div>
          <div>
            <small class="text-muted" v-if="upload.createdAt !== null">
              {{ $t('Created at') }} <local-timestamp :timestamp="upload.createdAt"></local-timestamp>
            </small>
          </div>
        </div>
      </div>
    </div>
    <pagination-control :total="uploads.length" :per-page="perPage" @update-page="page = $event"></pagination-control>
  </div>
</template>

<style scoped>
.btn-modal {
  width: 100px;
}

.input {
  position: absolute;
  visibility: hidden;
}
</style>

<script>
import ChunkedUpload from 'scripts/lib/upload/chunked.js';
import DirectUpload from 'scripts/lib/upload/direct.js';
import UploadDropzone from 'scripts/lib/components/UploadDropzone.vue';

export default {
  components: {
    UploadDropzone,
  },
  data() {
    return {
      suffix: kadi.utils.randomAlnum(), // To create unique IDs.
      uploadTypes: {},
      selectedStorage: 'local',
      uploads: [],
      uploadQueue: [],
      uploadTimeoutHandle: null,
      resumedUpload: null,
      replaceApplyAll: false,
      page: 1,
      stateNames: {
        paused: $t('Paused'),
        pending: $t('Pending'),
        uploading: $t('Uploading'),
        processing: $t('Processing'),
        completed: $t('Completed'),
      },
    };
  },
  props: {
    newUploadEndpoint: String,
    getUploadsEndpoint: String,
    directUploadEndpoint: String,
    storageTypes: Array,
    chunkedUploadBoundary: Number,
    perPage: {
      type: Number,
      default: 5,
    },
  },
  computed: {
    paginatedUploads() {
      return kadi.utils.paginateList(this.uploads, this.page, this.perPage);
    },
    totalUploadSize() {
      /* eslint-disable no-param-reassign */
      return this.uploads.reduce((acc, upload) => acc += upload.size, 0);
    },
    completedUploadsCount() {
      return this.uploads.reduce((acc, upload) => (upload.state === 'completed' ? acc += 1 : acc), 0);
      /* eslint-enable no-param-reassign */
    },
    uploadInProgress() {
      return this.uploads.slice().some((upload) => upload.state === 'uploading');
    },
    uploadsResumable() {
      return this.uploads.slice().some((upload) => this.supportsResuming(upload) && this.isResumable(upload));
    },
    uploadsPausable() {
      return this.uploads.slice().some((upload) => this.supportsResuming(upload) && this.isPausable(upload));
    },
    uploadsCancelable() {
      return this.uploads.slice().some((upload) => ['pending', 'uploading', 'paused'].includes(upload.state));
    },
    uploadsCompletedText() {
      const completedText = this.uploads.length === 1 ? $t('upload completed') : $t('uploads completed');
      return `${this.completedUploadsCount}/${this.uploads.length} ${completedText}`;
    },
  },
  watch: {
    uploadQueue() {
      // When adding lots of files simultaneously, wait until they have all been added to the queue before uploading.
      window.clearTimeout(this.uploadTimeoutHandle);
      this.uploadTimeoutHandle = window.setTimeout(() => this.uploadNextFile(), 100);
    },
  },
  methods: {
    addFile(file, force = false, origin = null) {
      const uploadMethod = file.size < this.chunkedUploadBoundary ? 'direct' : 'chunked';

      const upload = this.uploadTypes[uploadMethod].create({
        file,
        name: file.name,
        size: file.size,
        forceReplace: force,
        origin,
        storageType: this.selectedStorage,
      });

      this.uploadQueue.push(upload);
      this.uploads.push(upload);
    },

    confirmReplace(upload) {
      let replaceMsg = $t(
        'A file with the name \'{{filename}}\' already exists in the current record.',
        {filename: upload.name},
      );
      replaceMsg += `\n${$t('Do you want to replace it?')}`;

      return new Promise((resolve) => {
        $(this.$refs.replaceDialog).modal({backdrop: 'static', keyboard: false});
        this.$refs.replaceDialogText.innerText = replaceMsg;

        let cancelUploadHandler = null;
        let replaceFileHandler = null;

        // Make sure that the event listeners are removed again and the checkbox is reset after resolving the promise by
        // closing the modal via one of the buttons.
        const resolveDialog = (status) => {
          resolve({status, applyAll: this.replaceApplyAll});
          this.replaceApplyAll = false;
          this.$refs.replaceDialogBtnNo.removeEventListener('click', cancelUploadHandler);
          this.$refs.replaceDialogBtnYes.removeEventListener('click', replaceFileHandler);
        };

        cancelUploadHandler = () => resolveDialog(false);
        replaceFileHandler = () => resolveDialog(true);

        this.$refs.replaceDialogBtnNo.addEventListener('click', cancelUploadHandler);
        this.$refs.replaceDialogBtnYes.addEventListener('click', replaceFileHandler);
      });
    },

    resumeFileInputChange(e) {
      const file = e.target.files[0];
      const confirmMsg = $t('Do you still want to continue?');

      let uploadSizeMsg = $t('The file you have selected has a different size than the previous upload.');
      uploadSizeMsg += `\n${confirmMsg}`;

      if (file.size !== this.resumedUpload.size) {
        if (!window.confirm(uploadSizeMsg)) {
          return;
        }
      }

      let filenameMsg = $t('The file you have selected has a different name than the previous upload.');
      filenameMsg += `\n${confirmMsg}`;

      if (file.name !== this.resumedUpload.name) {
        if (!window.confirm(filenameMsg)) {
          return;
        }
      }

      this.resumedUpload.file = file;
      this.resumedUpload.state = 'pending';
      this.uploadQueue.push(this.resumedUpload);
    },

    async handleFileReplacement(upload) {
      // Check if an existing file should be replaced without asking for confirmation.
      if (upload.forceReplace) {
        return true;
      }

      // Show a confirmation dialog.
      const input = await this.confirmReplace(upload);

      // Either mark all files to be replaced or just continue with the upload as normal.
      if (input.status && input.applyAll) {
        for (const _upload of this.uploads.slice()) {
          _upload.forceReplace = true;
        }
      // If applicable, mark all current uploads to be skipped and cancel the current upload.
      } else if (!input.status) {
        // Mark all pending uploads as not to be replaced.
        if (input.applyAll) {
          for (const _upload of this.uploads.slice()) {
            _upload.skipReplace = true;
          }
        }

        // Cancel the current upload either way.
        this.cancelUploads(true, upload);
        return false;
      }

      return true;
    },

    async handleFileExists(upload) {
      // Check if an existing file should not be replaced without asking for confirmation.
      if (upload.skipReplace) {
        this.cancelUploads(true, upload);
        return false;
      }

      // Ask the user if the file should be replaced.
      const replacedByUser = await this.handleFileReplacement(upload);
      return replacedByUser;
    },

    async handleError(error, upload) {
      // Handle file already existing.
      if (error.request.status === 409) {
        // Reset the progress of the upload, in case the actual upload process was already started.
        upload.progress = 0;

        const replaceFile = await this.handleFileExists(upload);
        return replaceFile;
      }

      // Check if some quota was exceeded or some other error occured.
      const errorType = error.request.status === 413 ? 'warning' : 'danger';
      // If applicable, use the error message from the backend.
      const errorMsg = error.response.data.description
        ? error.response.data.description
        : $t('Error initiating upload.');

      kadi.alert(errorMsg, {request: error.request, type: errorType});

      this.cancelUploads(true, upload);
      return false;
    },

    async uploadNextFile() {
      // Check precondition to start the next upload. There will be only one upload at a time.
      if (this.uploadQueue.length === 0 || this.uploadInProgress) {
        return;
      }

      // Get the next upload in the queue.
      const upload = this.uploadQueue[0];

      // Check if the upload was already started just in case.
      if (upload.state !== 'pending') {
        return;
      }

      upload.state = 'uploading';

      // Start the provider specific upload.
      await this.uploadTypes[upload.uploadType].upload(upload);

      // Remove the upload from the queue regardless of whether it was successful or not. At this point, the upload
      // provider tried its best to upload the file, so we are done.
      kadi.utils.removeFromList(this.uploadQueue, upload);
    },

    cancelUploads(force, upload = null) {
      const _removeUpload = (upload) => {
        kadi.utils.removeFromList(this.uploadQueue, upload);
        kadi.utils.removeFromList(this.uploads, upload);
        this.$emit('upload-canceled', upload, upload.origin);
      };

      let uploads = [];
      let message = '';

      if (upload === null) {
        uploads = this.uploads.slice();
        message = $t('Are you sure you want to cancel all uploads?');
      } else {
        uploads.push(upload);
        message = $t('Are you sure you want to cancel this upload?');
      }

      if (!force && !window.confirm(message)) {
        return;
      }

      for (const _upload of uploads) {
        // If the upload is already processing or completed we just ignore the cancel request.
        if (!force && ['processing', 'completed'].includes(_upload.state)) {
          continue;
        }

        // Cancel the current request if possible.
        if (_upload.source) {
          _upload.source.cancel();
          _upload.source = null;
        }

        // Cancel the provider specific upload.
        this.uploadTypes[_upload.uploadType].cancel(_upload)
          .then(() => _removeUpload(_upload))
          .catch((error) => {
            if (error.request.status !== 404) {
              kadi.alert($t('Error removing upload.'), {request: error.request});
            } else {
              _removeUpload(_upload);
            }
          });
      }
    },

    pauseUploads(upload = null) {
      let uploads = [];
      if (upload === null) {
        uploads = this.uploads.slice();
      } else {
        uploads.push(upload);
      }

      for (const _upload of uploads) {
        if (!this.supportsResuming(_upload) || !this.isPausable(_upload)) {
          continue;
        }

        _upload.state = 'paused';

        // Cancel the current request if possible.
        if (_upload.source) {
          _upload.source.cancel();
          _upload.source = null;
        }

        kadi.utils.removeFromList(this.uploadQueue, _upload);
      }
    },

    resumeUploads(upload = null) {
      if (upload !== null) {
        if (this.supportsResuming(upload)) {
          if (this.isResumable(upload)) {
            // The upload is directly resumable.
            upload.state = 'pending';
            this.uploadQueue.push(upload);
          } else {
            // The upload was started in a previous session, so a new file needs to be selected.
            this.resumedUpload = upload;
            this.$refs.resumeFileInput.click();
          }
        }
      } else {
        // For bulk resuming, we only take uploads that are directly resumable into account.
        for (const _upload of this.uploads.slice()) {
          if (this.supportsResuming(_upload) && this.isResumable(_upload)) {
            _upload.state = 'pending';
            this.uploadQueue.push(_upload);
          }
        }
      }
    },

    supportsResuming(upload) {
      return this.uploadTypes[upload.uploadType].resumable;
    },

    isResumable(upload) {
      return this.uploadTypes[upload.uploadType].isResumable(upload);
    },

    isPausable(upload) {
      return this.uploadTypes[upload.uploadType].isPausable(upload);
    },

    beforeUnload(e) {
      if (this.uploadQueue.length > 0) {
        e.preventDefault();
        (e || window.event).returnValue = '';
        return '';
      }
      return null;
    },
  },
  mounted() {
    const chunkedUploadProvider = new ChunkedUpload(
      this.newUploadEndpoint,
      this.getUploadsEndpoint,
      (upload, data) => this.$emit('upload-completed', data._meta.file, upload.origin),
      this.handleError,
      this.cancelUploads,
      this.pauseUploads,
    );

    this.uploadTypes.chunked = chunkedUploadProvider;

    // Get all incomplete uploads so the user can resume them.
    chunkedUploadProvider.loadUploads()
      .then((fetchedUploads) => {
        this.uploads = this.uploads.concat(fetchedUploads);
      })
      .catch((error) => {
        kadi.alert($t('Error loading uploads.'), {request: error.request});
      });

    const directUploadProvider = new DirectUpload(
      this.directUploadEndpoint,
      (upload, data) => this.$emit('upload-completed', data, upload.origin),
      this.handleError,
    );

    this.uploadTypes.direct = directUploadProvider;

    window.addEventListener('beforeunload', this.beforeUnload);

    // Move the modal replace dialog to the document body so it is always shown, even if the upload manager is not
    // visible, and to also avoid general rendering issues.
    document.getElementsByTagName('body')[0].appendChild(this.$refs.replaceDialog);
  },
  beforeDestroy() {
    window.removeEventListener('beforeunload', this.beforeUnload);
    $(this.$refs.replaceDialog).modal('dispose');
  },
};
</script>
