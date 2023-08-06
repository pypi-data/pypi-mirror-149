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

import StlViewer from 'scripts/lib/components/StlViewer.vue';
import WorkflowEditor from 'scripts/lib/components/WorkflowEditor.vue';

new Vue({
  el: '#vm',
  components: {
    StlViewer,
    WorkflowEditor,
  },
  data: {
    previewData: null,
    initialized: false,
  },
  mounted() {
    axios.get(kadi.js_resources.get_file_preview_endpoint)
      .then((response) => {
        this.previewData = response.data;
        this.initialized = true;
      })
      .catch((error) => {
        if (error.request.status !== 404) {
          kadi.alert($t('Error loading file preview.'), {request: error.request});
        } else {
          this.initialized = true;
        }
      });
  },
});
