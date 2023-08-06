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
    <slot :items="items" :paginated-items="paginatedItems"></slot>
    <em class="text-muted" v-if="initialized && total === 0">{{ placeholder }}</em>
    <i class="fa-solid fa-circle-notch fa-spin" v-if="!initialized"></i>
    <div class="row align-items-end"
         :class="{'mt-4': total > perPage || (enableFilter && initialized && items.length > 1)}">
      <div class="col-sm-8 mb-2 mb-sm-0" v-show="total > perPage">
        <pagination-control :total="total" :per-page="perPage" @update-page="updatePage"></pagination-control>
      </div>
      <div class="col-sm-4" v-if="enableFilter && initialized && items.length > 1">
        <div class="input-group input-group-sm">
          <input :id="filterId" class="form-control" :placeholder="filterPlaceholder" v-model="filter">
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
      page: 1,
      filter: '',
      filterId: kadi.utils.randomAlnum(),
      initialized: false,
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
    filterProps: {
      type: Array,
      default: () => [],
    },
  },
  computed: {
    filteredItems() {
      const filter = this.filter.toLowerCase().trim();
      if (!this.enableFilter || filter === '') {
        return this.items;
      }

      const items = [];
      this.items.slice().forEach((item) => {
        for (const prop of this.filterProps) {
          if (kadi.utils.getProp(item, prop).toLowerCase().includes(filter)) {
            items.push(item);
            break;
          }
        }
      });

      return items;
    },
    paginatedItems() {
      const start = (this.page - 1) * this.perPage;
      const end = start + this.perPage;
      return this.filteredItems.slice(start, end);
    },
    total() {
      return this.filteredItems.length;
    },
  },
  methods: {
    updatePage(page) {
      this.page = page;
    },
    updateData() {
      axios.get(this.endpoint, {params: this.args})
        .then((response) => {
          this.initialized = true;
          this.items = response.data;
        })
        .catch((error) => kadi.alert($t('Error loading data.'), {request: error.request, scrollTo: false}));
    },
    // Convenience function for forcing an update from outside.
    update() {
      this.updateData();
    },
  },
  mounted() {
    this.updateData();
  },
};
</script>
