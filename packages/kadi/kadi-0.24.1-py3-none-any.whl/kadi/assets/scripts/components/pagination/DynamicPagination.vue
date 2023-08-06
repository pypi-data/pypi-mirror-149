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
    <slot :items="items" :total="total" :total-unfiltered="totalUnfiltered"></slot>
    <em class="text-muted" v-if="initialized && total === 0">{{ placeholder }}</em>
    <i class="fa-solid fa-circle-notch fa-spin" v-if="!initialized"></i>
    <div class="row align-items-end" :class="{'mt-4': total > perPage || (enableFilter && initialized)}">
      <div :class="{'col-lg-8 mb-2 mb-lg-0': enableFilter, 'col-lg-12': !enableFilter}" v-show="total > perPage">
        <pagination-control :total="total" :per-page="perPage" @update-page="updatePage" ref="pagination">
          <i class="fa-solid fa-circle-notch fa-spin ml-4 align-self-center" v-if="loading"></i>
        </pagination-control>
      </div>
      <div class="col-lg-4" v-if="enableFilter && initialized">
        <div class="input-group input-group-sm">
          <input class="form-control" :id="filterId" :placeholder="filterPlaceholder" v-model="filter">
          <clear-button :input-id="filterId" :input="filter" :small="true" @clear-input="filter = ''"></clear-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      items: [],
      total: 0,
      totalUnfiltered: 0,
      page: 1,
      filter: '',
      filterId: kadi.utils.randomAlnum(),
      initialized: false,
      loading: false,
      updateTimeoutHandle: null,
    };
  },
  props: {
    endpoint: String,
    args: {
      type: Object,
      default: () => ({}),
    },
    placeholder: {
      type: String,
      default: $t('No results.'),
    },
    perPage: {
      type: Number,
      default: 10,
    },
    enableFilter: {
      type: Boolean,
      default: false,
    },
    filterPlaceholder: {
      type: String,
      default: $t('Filter'),
    },
  },
  watch: {
    endpoint() {
      this.$refs.pagination.updatePage(1, true);
    },
    args() {
      this.$refs.pagination.updatePage(1, true);
    },
    filter() {
      this.$refs.pagination.updatePage(1, true);
    },
  },
  methods: {
    updatePage(page) {
      this.page = page;
      this.updateData();
    },
    updateData(forceUpdate = false) {
      this.loading = true;

      const _updateData = () => {
        const args = {...this.args};
        if (this.enableFilter) {
          args.filter = this.filter;
        }

        axios.get(this.endpoint, {params: {page: this.page, per_page: this.perPage, ...args}})
          .then((response) => {
            this.initialized = true;
            this.items = response.data.items;
            this.total = response.data._pagination.total_items;

            if (!this.filter) {
              this.totalUnfiltered = this.total;
            }
          })
          .catch((error) => kadi.alert($t('Error loading data.'), {request: error.request, scrollTo: false}))
          .finally(() => this.loading = false);
      };

      if (forceUpdate) {
        _updateData();
      } else {
        window.clearTimeout(this.updateTimeoutHandle);
        this.updateTimeoutHandle = window.setTimeout(_updateData, 500);
      }
    },
    // Convenience function for forcing an update from outside.
    update() {
      this.updateData(true);
    },
  },
  mounted() {
    this.updateData(true);
  },
};
</script>
