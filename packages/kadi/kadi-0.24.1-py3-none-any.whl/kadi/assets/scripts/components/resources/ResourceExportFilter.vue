<!-- Copyright 2022 Karlsruhe Institute of Technology
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
    <strong>{{ $t('Export data to exclude') }}</strong>
    <hr class="mt-0">
    <div class="form-check form-check-inline">
      <input type="checkbox" class="form-check-input" :id="`user-${suffix}`" v-model="filter.user">
      <label class="form-check-label" :for="`user-${suffix}`">{{ $t('User information') }}</label>
    </div>
    <br>
    <div v-if="resourceType === 'collection'">
      <div class="form-check form-check-inline mt-2">
        <input type="checkbox" class="form-check-input" :id="`records-${suffix}`" v-model="filter.records">
        <label class="form-check-label" :for="`records-${suffix}`">{{ $t('Records') }}</label>
      </div>
      <br>
    </div>
    <div v-if="!filter.records">
      <label class="form-control-label mt-2" :for="`links-${suffix}`">{{ $t('Record links') }}</label>
      <select class="custom-select custom-select-sm" :id="`links-${suffix}`" v-model="filter.links">
        <option value=""></option>
        <option value="out">{{ $t('Outgoing') }}</option>
        <option value="in">{{ $t('Incoming') }}</option>
        <option value="both">{{ $t('Both') }}</option>
      </select>
    </div>
    <div v-if="resourceType === 'record' && extras.length > 0">
      <div class="row mt-3 mb-2">
        <div class="col-md-6">{{ $t('Extra metadata') }}</div>
        <div class="col-md-6 d-md-flex justify-content-end mt-2 mt-md-0" v-if="allowExtrasPropagation">
          <div class="form-check form-check-inline">
            <input type="checkbox" class="form-check-input" :id="`propagate-${suffix}`" v-model="filter.propagate">
            <label class="form-check-label" :for="`propagate-${suffix}`">
              {{ $t('Apply to linked records') }}
            </label>
          </div>
        </div>
      </div>
      <div class="card bg-light">
        <div class="card-body">
          <extras-selector :extras="extras" @select="filter.extras = $event"></extras-selector>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      suffix: kadi.utils.randomAlnum(), // To create unique IDs.
      filter: {
        user: false,
        records: false,
        links: '',
        extras: {},
        propagate: false,
      },
    };
  },
  props: {
    resourceType: String,
    extras: {
      type: Array,
      default: () => [],
    },
    allowExtrasPropagation: {
      type: Boolean,
      default: true,
    },
  },
  watch: {
    filter: {
      handler() {
        const filter = {};

        if (this.filter.user !== false) {
          filter.user = this.filter.user;
        }
        if (this.filter.records !== false) {
          filter.records = this.filter.records;
        }
        if (this.filter.links !== '') {
          filter.links = this.filter.links === 'both' ? true : this.filter.links;
        }
        if (Object.keys(this.filter.extras).length > 0) {
          filter.extras = this.filter.extras;
        }
        if (this.filter.propagate) {
          filter.propagate_extras = true;
        }

        this.$emit('filter', filter);
      },
      deep: true,
    },
  },
};
</script>
