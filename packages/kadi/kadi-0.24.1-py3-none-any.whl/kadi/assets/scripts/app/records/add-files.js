/* Copyright 2020 Karlsruhe Institute of Technology
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

import CanvasPainter from 'scripts/lib/components/CanvasPainter.vue';
import TextEditor from 'scripts/lib/components/TextEditor.vue';
import UploadManager from 'scripts/lib/components/UploadManager.vue';
import WorkflowEditor from 'scripts/lib/components/WorkflowEditor.vue';

new Vue({
  el: '#vm',
  components: {
    CanvasPainter,
    TextEditor,
    UploadManager,
    WorkflowEditor,
  },
  data: {
    currentTab: null,
    fileTypes: {
      drawing: {
        filename: '',
        currentFile: null,
        fileUrl: null,
        unsavedChanges: false,
        uploading: false,
      },
      text: {
        filename: '',
        currentFile: null,
        fileUrl: null,
        unsavedChanges: false,
        uploading: false,
      },
      workflow: {
        filename: '',
        currentFile: null,
        fileUrl: null,
        unsavedChanges: false,
        uploading: false,
      },
    },
  },
  methods: {
    changeTab(tab) {
      this.currentTab = tab;
    },
    uploadCompleted(file, origin) {
      if (origin in this.fileTypes) {
        this.fileTypes[origin].uploading = false;
        this.fileTypes[origin].currentFile = file;
        kadi.alert($t('File uploaded successfully.'), {type: 'success', scrollTo: false});
      }
    },
    uploadCanceled(upload, origin) {
      if (origin in this.fileTypes) {
        this.fileTypes[origin].uploading = false;
      }
    },
    _uploadFile(file, fileType) {
      // When trying to replace a file that is currently being edited (or that has just been created via direct upload),
      // we skip the confirmation for replacing existing files.
      const currentFile = this.fileTypes[fileType].currentFile;
      this.$refs.uploadManager.addFile(file, currentFile && currentFile.name === file.name, fileType);

      this.fileTypes[fileType].uploading = true;
      this.fileTypes[fileType].unsavedChanges = false;
    },
    uploadFile(file, fileType) {
      const currentFile = this.fileTypes[fileType].currentFile;

      if (currentFile && currentFile.name === file.name) {
        axios.get(currentFile._links.self)
          .then((response) => {
            // Check if the content of the current file has changed since loading or last uploading it by just comparing
            // the checksums.
            if (currentFile.checksum !== response.data.checksum) {
              let warningMsg = $t('The content of the file you are currently editing changed since loading it.');
              warningMsg += `\n${$t('Do you still want to overwrite it?')}`;

              if (window.confirm(warningMsg)) {
                this._uploadFile(file, fileType);
              }
            } else {
              this._uploadFile(file, fileType);
            }
          });
      } else {
        this._uploadFile(file, fileType);
      }
    },
    saveDrawing(canvas) {
      let filename = this.fileTypes.drawing.filename;
      if (!filename.endsWith('.png')) {
        filename += '.png';
      }

      const bstr = window.atob(canvas.toDataURL().split(',')[1]);
      let n = bstr.length;
      const u8arr = new Uint8Array(n);

      while (n) {
        u8arr[n - 1] = bstr.charCodeAt(n - 1);
        n -= 1;
      }

      const file = new File([u8arr], filename);
      this.uploadFile(file, 'drawing');
    },
    saveText(document, newline) {
      let filename = this.fileTypes.text.filename;
      // Only do a very basic check whether any file extension exists at all.
      if (!filename.includes('.')) {
        filename += '.txt';
      }

      let text = document.toString();
      if (newline === 'windows') {
        text = text.replaceAll('\n', '\r\n');
      }

      const file = new File([text], filename);
      this.uploadFile(file, 'text');
    },
    saveWorkflow(editor) {
      let filename = this.fileTypes.workflow.filename;
      if (!filename.endsWith('.flow')) {
        filename += '.flow';
      }

      const file = new File([JSON.stringify(editor.toFlow())], filename);
      this.uploadFile(file, 'workflow');
    },
  },
  mounted() {
    const fileType = kadi.js_resources.file_type;
    const currentFile = kadi.js_resources.current_file;

    if (fileType !== null && fileType in this.fileTypes) {
      this.fileTypes[fileType].currentFile = currentFile;
      this.fileTypes[fileType].fileUrl = currentFile._links.download;
      this.fileTypes[fileType].filename = currentFile.name;

      // Wait until the content of the previous tab has loaded, as some components rely on the DOM to initialize their
      // size correctly.
      this.$nextTick(() => this.$refs.navTabs.changeTab(fileType));
    }
  },
});
