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
    <div class="mb-4 collapse" :id="extrasId" :class="{'show': showExtrasSearch}" v-if="extrasSearch">
      <search-extras :extras="extras" @change="extras = $event" @search="search"></search-extras>
    </div>
    <div class="form-row">
      <div class="mb-2 mb-xl-0" :class="{'col-xl-6': extrasSearch, 'col-xl-8': !extrasSearch}">
        <div class="input-group">
          <input class="form-control" :id="queryId" v-model="query" @keydown.enter="search">
          <clear-button :input="query" :input-id="queryId" @clear-input="query = ''"></clear-button>
          <div class="input-group-append">
            <button type="button" class="btn btn-light" @click="search">
              <i class="fa-solid fa-magnifying-glass"></i> {{ $t('Search') }}
            </button>
          </div>
        </div>
      </div>
      <div class="col-xl-4 mb-2 mb-xl-0">
        <div class="input-group">
          <div class="input-group-prepend">
            <label class="input-group-text" :for="sortId">{{ $t('Sort by') }}</label>
          </div>
          <select class="custom-select" :id="sortId" v-model="sort">
            <option v-for="option in sortOptions" :key="option[0]" :value="option[0]">{{ option[1] }}</option>
          </select>
        </div>
      </div>
      <div class="col-xl-2" v-if="extrasSearch">
        <collapse-item class="btn btn-block btn-light"
                       :id="extrasId"
                       :is-collapsed="!extrasSearchActive"
                       @collapse="extrasSearchActive = !$event">
          {{ $t('Search extras') }}
        </collapse-item>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      query: '',
      prevQuery: '',
      queryParam: 'query',
      queryId: kadi.utils.randomAlnum(),
      sort: '_score',
      sortParam: 'sort',
      sortId: kadi.utils.randomAlnum(),
      sortOptions: [
        ['_score', $t('Relevance')],
        ['-last_modified', $t('Last modified (newest first)')],
        ['last_modified', $t('Last modified (oldest first)')],
        ['-created_at', $t('Created at (newest first)')],
        ['created_at', $t('Created at (oldest first)')],
        ['title', $t('Title (ascending)')],
        ['-title', $t('Title (descending)')],
        ['identifier', $t('Identifier (ascending)')],
        ['-identifier', $t('Identifier (descending)')],
      ],
      extras: '[]',
      prevExtras: '[]',
      extrasParam: 'extras',
      extrasId: kadi.utils.randomAlnum(),
      extrasSearchActive: false,
      prevExtrasSearchActive: false,
      showExtrasSearch: false,
      initialized: false,
    };
  },
  props: {
    extrasSearch: {
      type: Boolean,
      default: false,
    },
  },
  watch: {
    sort() {
      if (this.initialized) {
        const url = kadi.utils.setSearchParam(this.sortParam, this.sort);
        kadi.utils.replaceState(url);
        this.$emit('search');
      }
    },
  },
  methods: {
    search() {
      // Do not search if nothing changed.
      if (this.query === this.prevQuery
          && this.extras === this.prevExtras
          && this.extrasSearchActive === this.prevExtrasSearchActive) {
        return;
      }

      let url = kadi.utils.setSearchParam(this.queryParam, this.query);
      kadi.utils.replaceState(url);

      if (this.extrasSearchActive) {
        url = kadi.utils.setSearchParam(this.extrasParam, this.extras);
      } else {
        url = kadi.utils.removeSearchParam(this.extrasParam);
      }
      kadi.utils.replaceState(url);

      this.$emit('search');

      this.prevQuery = this.query;
      this.prevExtras = this.extras;
      this.prevExtrasSearchActive = this.extrasSearchActive;
    },
  },
  beforeMount() {
    if (kadi.utils.hasSearchParam(this.queryParam)) {
      this.query = kadi.utils.getSearchParam(this.queryParam);
      this.prevQuery = this.query;
    }

    if (kadi.utils.hasSearchParam(this.extrasParam)) {
      this.extras = kadi.utils.getSearchParam(this.extrasParam);
      this.prevExtras = this.extras;
      this.prevExtrasSearchActive = this.extrasSearchActive = this.showExtrasSearch = true;
    }

    if (kadi.utils.hasSearchParam(this.sortParam)) {
      const sort = kadi.utils.getSearchParam(this.sortParam);

      for (const option of this.sortOptions) {
        if (option[0] === sort) {
          this.sort = sort;
          break;
        }
      }
    }

    // Skip first potential change.
    this.$nextTick(() => this.initialized = true);
  },
};
</script>
