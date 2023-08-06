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
  <div class="dropdown" :id="`dropdown-${id}`" :class="{'show': dropdownActive}">
    <div class="input-group input-group-sm responsive-width" @click="showDropdown">
      <input class="form-control custom-input" :placeholder="$t('Quick search')" v-model="query" ref="input">
      <div class="input-group-append" v-if="query">
        <button type="button" class="btn btn-sm clear-btn input-group-append-content" @click.stop="clearQuery">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>
      <div class="input-group-append" v-else>
        <span class="search-btn input-group-text input-group-append-content">
          <i class="fa-solid fa-magnifying-glass fa-sm"></i>
        </span>
      </div>
    </div>
    <div class="dropdown-menu responsive-width p-0 mt-2" :class="{'d-block': dropdownActive}">
      <div v-if="initialized">
        <div class="px-2 my-1" v-if="items.length === 0">
          <strong class="text-muted font-sm">{{ $t('No results.') }}</strong>
        </div>
        <div v-for="(item, index) in items" :key="item.endpoint" v-else>
          <a class="dropdown-item p-2" :href="item.endpoint">
            <div class="d-flex justify-content-between">
              <strong class="font-sm">{{ item.identifier }}</strong>
              <div>
                <span class="badge badge-light border border-muted font-weight-normal ml-3">{{ item.type }}</span>
              </div>
            </div>
            <small>
              {{ $t('Last modified') }} <from-now :timestamp="item.timestamp"></from-now>
            </small>
          </a>
          <div class="dropdown-divider m-0" v-if="index < items.length - 1"></div>
        </div>
      </div>
      <i class="fa-solid fa-circle-notch fa-spin text-muted p-2" v-if="!initialized"></i>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.clear-btn, .search-btn {
  background-color: #1a252f !important;
  transition: none;
}

.custom-input {
  background-color: #1a252f;
  border: none;
  box-shadow: none;
  cursor: pointer;
  -webkit-appearance: none;
}

.dropdown.show {
  .custom-input, .clear-btn, .search-btn {
    background-color: white !important;
  }
}

.dropdown-item {
  white-space: normal;
  word-break: break-all;
}

.font-sm {
  font-size: 90%;
}

.input-group-append-content {
  background-color: white;
  border: none;
  color: #aab7b8;
  padding-left: 0.75rem !important;
  padding-right: 0.75rem !important;
}

.responsive-width {
  width: 200px;

  @media (min-width: 1200px) {
    width: 300px;
  }
}
</style>

<script>
export default {
  data() {
    return {
      id: kadi.utils.randomAlnum(),
      query: '',
      items: [],
      dropdownActive: false,
      initialized: false,
      searchTimeoutHandle: null,
    };
  },
  props: {
    endpoint: String,
  },
  watch: {
    query() {
      this.search();
    },
  },
  methods: {
    search() {
      window.clearTimeout(this.searchTimeoutHandle);
      this.searchTimeoutHandle = window.setTimeout(() => {
        axios.get(`${this.endpoint}?query=${this.query}`)
          .then((response) => {
            this.items = response.data;
            this.initialized = true;
          });
      }, 500);
    },
    showDropdown() {
      if (!this.dropdownActive) {
        this.dropdownActive = true;

        if (!this.initialized) {
          this.search();
        }
      }
    },
    clearQuery() {
      this.query = '';
      this.dropdownActive = true;
      this.$refs.input.focus();
    },
    outsideClickHandler(event) {
      if (event.target.closest(`#dropdown-${this.id}`) === null) {
        this.dropdownActive = false;
      }
    },
  },
  mounted() {
    window.addEventListener('click', this.outsideClickHandler);
  },
  beforeDestroy() {
    window.removeEventListener('click', this.outsideClickHandler);
  },
};
</script>
