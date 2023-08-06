<!-- Copyright 2021 Karlsruhe Institute of Technology
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
    <div class="row mb-4">
      <div class="col-sm-4 mb-2 mb-sm-0">
        <a class="btn btn-sm btn-light" :href="downloadEndpoint">
          <i class="fa-solid fa-download"></i>
          {{ $t('Download') }}
        </a>
      </div>
      <div class="col-sm-8 d-sm-flex justify-content-end" v-if="isCustomizable">
        <button class="btn btn-sm btn-light mr-2" :disabled="loading" @click="updatePreview" v-if="showUpdateButton">
          <i class="fa-solid fa-eye"></i>
          {{ $t('Update preview') }}
        </button>
        <collapse-item :id="`collapse-${suffix}`"
                       :is-collapsed="true"
                       class="btn btn-sm btn-light"
                       @collapse="showUpdateButton = !$event">
          {{ $t('Customize') }}
        </collapse-item>
      </div>
    </div>
    <div class="card mb-4 collapse" :id="`collapse-${suffix}`" v-if="isCustomizable">
      <div class="card-body">
        <resource-export-filter :resource-type="resourceType"
                                :extras="extras"
                                :allow-extras-propagation="exportType === 'json'"
                                @filter="filter = $event">
        </resource-export-filter>
      </div>
    </div>
    <div v-if="!loading" ref="preview">
      <div v-if="exportType === 'json'">
        <div class="card bg-light">
          <div class="mt-3 ml-3">
            <pre class="max-vh-75">{{ exportData }}</pre>
          </div>
        </div>
      </div>
      <div v-if="exportType === 'pdf'">
        <iframe class="w-100 vh-75 border border-muted rounded" frameborder="0" allowfullscreen :src="exportData">
        </iframe>
      </div>
      <div v-if="exportType === 'qr'">
        <div class="border border-muted bg-light text-center">
          <img class="img-fluid" :src="exportData">
        </div>
      </div>
    </div>
    <i class="fa-solid fa-circle-notch fa-spin" v-else></i>
  </div>
</template>

<script>
export default {
  data() {
    return {
      suffix: kadi.utils.randomAlnum(), // To create unique IDs.
      exportData: null,
      loading: true,
      showUpdateButton: false,
      filter: {},
    };
  },
  props: {
    resourceType: String,
    exportType: String,
    endpoint: String,
    extras: {
      type: Array,
      default: () => [],
    },
  },
  computed: {
    downloadEndpoint() {
      return `${this.endpoint}?download=true&filter=${JSON.stringify(this.filter)}`;
    },
    isCustomizable() {
      return ['json', 'pdf'].includes(this.exportType);
    },
  },
  methods: {
    updateExportData(scrollIntoView = false) {
      this.loading = true;

      axios.get(this.endpoint, {params: {filter: JSON.stringify(this.filter)}})
        .then((response) => {
          this.exportData = response.data;
          this.loading = false;

          if (scrollIntoView) {
            this.$nextTick(() => kadi.utils.scrollIntoView(this.$refs.preview, 'top'));
          }
        })
        .catch((error) => kadi.alert($t('Error loading export data.'), {request: error.request}));
    },
    updatePreview() {
      this.updateExportData(true);
    },
  },
  mounted() {
    this.updateExportData();
  },
};
</script>
