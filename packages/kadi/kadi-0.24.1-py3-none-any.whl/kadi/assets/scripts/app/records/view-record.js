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

import RecordLinksGraph from 'scripts/lib/components/RecordLinksGraph.vue';

new Vue({
  el: '#vm',
  components: {
    RecordLinksGraph,
  },
  data: {
    currentTab: null,
    renderLinksGraph: false,
    visualizeLinks: false,
    visualizeLinksParam: 'visualize',
    linkDirection: '',
    linkFilter: '',
  },
  watch: {
    visualizeLinks() {
      if (this.visualizeLinks) {
        // If we render the links graph component before it is shown, its size cannot be initialized correctly.
        this.renderLinksGraph = true;
      }

      const url = kadi.utils.setSearchParam(this.visualizeLinksParam, this.visualizeLinks);
      kadi.utils.replaceState(url);
    },
  },
  methods: {
    changeTab(tab) {
      this.currentTab = tab;

      let url = null;

      if (this.currentTab === 'links') {
        url = kadi.utils.setSearchParam(this.visualizeLinksParam, this.visualizeLinks);
      } else {
        url = kadi.utils.removeSearchParam(this.visualizeLinksParam);
      }

      kadi.utils.replaceState(url);
    },
    deleteFile(file) {
      if (!window.confirm($t('Are you sure you want to delete this file?'))) {
        return;
      }

      this.$set(file, 'disabled', true);

      axios.delete(file._actions.delete)
        .then(() => {
          this.$refs.filesPagination.update();
          // Update the file revisions as well if they were loaded already.
          if (this.$refs.fileRevisionsPagination) {
            this.$refs.fileRevisionsPagination.update();
          }
          kadi.alert($t('File deleted successfully.'), {type: 'success', scrollTo: false});
        })
        .catch((error) => {
          kadi.alert($t('Error deleting file.'), {request: error.request});
          file.disabled = false;
        });
    },
  },
  created() {
    const visualizeLinks = kadi.utils.getSearchParam(this.visualizeLinksParam);

    if (visualizeLinks === 'true') {
      this.visualizeLinks = true;
    }
  },
});
