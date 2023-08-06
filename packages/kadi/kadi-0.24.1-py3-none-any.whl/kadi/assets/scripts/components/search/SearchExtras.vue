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
    <div v-for="(query, index) in queries" :key="query.id">
      <div class="form-row mb-4 mb-xl-2">
        <div class="col-xl-1 mb-1 mb-xl-0 d-flex justify-content-center">
          <popover-toggle class="w-100"
                          toggle-class="btn btn-sm btn-block btn-light text-muted"
                          width="400px"
                          placement="bottom"
                          v-if="index === 0">
            <template #toggle>
              <i class="fa-solid fa-circle-question"></i> {{ $t('Help') }}
            </template>
            <template #content>
              {{ $t('This menu allows searching the generic extra metadata of records, including keys, types and \
different kinds of values based on the selected types.') }}
              {{ $t("Multiple such queries can be combined with an 'AND' or an 'OR' operation in the form of \
'(Q1 AND Q2) OR (Q3 AND Q4)'.") }}
              {{ $t('Exact matches for keys and string values can be required by using double quotes, e.g. "key".') }}
              <hr class="my-1">
              {{ $t("Note that keys inside of nested metadata entries are indexed in the form of 'key_1.key_2'.") }}
              {{ $t('In case of list entries, keys are replaced by the corresponding index in the list instead, \
starting at 1.') }}
            </template>
          </popover-toggle>
          <select class="custom-select custom-select-sm" v-model="query.link" v-if="index > 0">
            <option v-for="(title, value) in selectors.links" :key="value" :value="value">{{ title }}</option>
          </select>
        </div>
        <div class="col-xl-2 mb-1 mb-xl-0">
          <div class="input-group input-group-sm">
            <div class="input-group-prepend">
              <span class="input-group-text">{{ $t('Type') }}</span>
            </div>
            <select class="custom-select custom-select-sm" v-model="query.type">
              <option value=""></option>
              <option v-for="(title, value) in selectors.types" :key="value" :value="value">{{ title }}</option>
            </select>
          </div>
        </div>
        <div class="mb-1 mb-xl-0" :class="{'col-xl-3': query.type, 'col-xl-8': !query.type}">
          <div class="input-group input-group-sm">
            <div class="input-group-prepend">
              <span class="input-group-text">{{ $t('Key') }}</span>
            </div>
            <input class="form-control" v-model="query.key" @keydown.enter="search">
          </div>
        </div>
        <div class="col-xl-5 mb-1 mb-xl-0" v-if="['str', 'bool'].includes(query.type)">
          <div class="input-group input-group-sm" v-if="query.type === 'str'">
            <div class="input-group-prepend">
              <span class="input-group-text">{{ $t('Value') }}</span>
            </div>
            <input class="form-control" v-model="query.str" @keydown.enter="search">
          </div>
          <div class="input-group input-group-sm" v-if="query.type === 'bool'">
            <div class="input-group-prepend">
              <span class="input-group-text">{{ $t('Value') }}</span>
            </div>
            <select class="custom-select" v-model="query.bool">
              <option value=""></option>
              <option v-for="(title, value) in selectors.boolValues" :key="value" :value="value">{{ title }}</option>
            </select>
          </div>
        </div>
        <div class="col-xl-1 mb-1 mb-xl-0" v-if="['numeric', 'date'].includes(query.type)">
          <select class="custom-select custom-select-sm" v-model="query.range" v-if="query.type === 'numeric'">
            <option v-for="(title, value) in selectors.numRanges" :key="value" :value="value">{{ title }}</option>
          </select>
          <select class="custom-select custom-select-sm" v-model="query.range" v-if="query.type === 'date'">
            <option v-for="(title, value) in selectors.dateRanges" :key="value" :value="value">{{ title }}</option>
          </select>
        </div>
        <div class="col-xl-2 mb-1 mb-xl-0" v-if="query.type === 'numeric'">
          <div class="input-group input-group-sm">
            <input class="form-control"
                   key="numMin"
                   :placeholder="$t('Minimum')"
                   v-model="query.numeric.min"
                   @keydown.enter="search"
                   v-if="['gt', 'bt'].includes(query.range)">
            <input class="form-control"
                   key="numMax"
                   :placeholder="$t('Maximum')"
                   v-model="query.numeric.max"
                   @keydown.enter="search"
                   v-if="['lt', 'bt'].includes(query.range)">
          </div>
        </div>
        <div class="col-xl-2 mb-1 mb-xl-0" v-if="query.type === 'numeric'">
          <div class="input-group input-group-sm">
            <div class="input-group-prepend">
              <span class="input-group-text">{{ $t('Unit') }}</span>
            </div>
            <input class="form-control" key="numUnit" v-model="query.numeric.unit" @keydown.enter="search">
          </div>
        </div>
        <div class="col-xl-4 mb-1 mb-xl-0" v-if="query.type === 'date'">
          <div class="input-group input-group-sm">
            <date-time-picker key="dateMin"
                              :placeholder="$t('Start date')"
                              :initial-value="query.date.min"
                              @input="query.date.min = $event"
                              v-if="['gt', 'bt'].includes(query.range)">
            </date-time-picker>
            <date-time-picker key="dateMax"
                              :placeholder="$t('End date')"
                              :initial-value="query.date.max"
                              @input="query.date.max = $event"
                              v-if="['lt', 'bt'].includes(query.range)">
            </date-time-picker>
          </div>
        </div>
        <div class="btn-group btn-group-sm col-xl-1">
          <button type="button" class="btn btn-light" :title="$t('Add search field')" @click="addQuery(null, index)">
            <i class="fa-solid fa-plus"></i>
          </button>
          <button type="button"
                  class="btn btn-light"
                  :title="$t('Remove search field')"
                  @click="removeQuery(index)"
                  v-if="queries.length > 1">
            <i class="fa-solid fa-xmark"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      queries: [],
      selectors: {
        types: {str: 'String', numeric: $t('Numeric'), bool: 'Boolean', date: 'Date'},
        links: {and: $t('AND'), or: $t('OR')},
        dateRanges: {gt: $t('Later'), lt: $t('Before'), bt: $t('Between')},
        numRanges: {gt: $t('Greater'), lt: $t('Less'), bt: $t('Between')},
        boolValues: {true: $t('true'), false: $t('false')},
      },
    };
  },
  props: {
    extras: String,
  },
  watch: {
    queries: {
      handler() {
        const results = [];
        for (const query of this.queries) {
          const result = {
            link: query.link,
            type: query.type,
            key: query.key,
          };

          if (['numeric', 'date'].includes(query.type)) {
            result[query.type] = {...query[query.type]};

            // Ignore the max value in this case.
            if (query.range === 'gt') {
              result[query.type].max = '';
            }
            // Ignore the min value in this case.
            if (query.range === 'lt') {
              result[query.type].min = '';
            }
          } else if (query.type) {
            result[query.type] = query[query.type];
          }

          // A query needs at least a type or key in order to be included in the serialized query.
          if (result.type || result.key) {
            results.push(result);
          }
        }

        this.$emit('change', JSON.stringify(results));
      },
      deep: true,
    },
  },
  methods: {
    addQuery(query = null, index = null) {
      const newQuery = {
        id: kadi.utils.randomAlnum(),
        link: 'and',
        type: '',
        key: '',
        str: '',
        numeric: {min: '', max: '', unit: ''},
        bool: '',
        date: {min: '', max: ''},
        range: 'gt',
      };

      if (query) {
        newQuery.link = query.link || 'and';
        newQuery.key = query.key || '';

        // Validate the type at least, since it is used to render the view in certain ways.
        if (Object.keys(this.selectors.types).includes(query.type)) {
          newQuery.type = query.type;
        }

        if (['numeric', 'date'].includes(newQuery.type)) {
          newQuery[newQuery.type] = {
            min: query[newQuery.type].min || '',
            max: query[newQuery.type].max || '',
          };

          if (newQuery.type === 'numeric') {
            newQuery[newQuery.type].unit = query[newQuery.type].unit || '';
          }

          if (newQuery[newQuery.type].min && newQuery[newQuery.type].max) {
            newQuery.range = 'bt';
          } else if (newQuery[newQuery.type].max) {
            newQuery.range = 'lt';
          }
        } else if (newQuery.type) {
          newQuery[newQuery.type] = query[newQuery.type] || '';
        }
      }

      if (index !== null) {
        this.queries.splice(index + 1, 0, newQuery);
      } else {
        this.queries.push(newQuery);
      }
    },
    removeQuery(index) {
      this.queries.splice(index, 1);
    },
    search() {
      this.$emit('search');
    },
  },
  mounted() {
    try {
      const queries = JSON.parse(this.extras);
      if (Array.isArray(queries) && queries.length > 0) {
        queries.forEach((query) => this.addQuery(query));
      } else {
        this.addQuery();
      }
    } catch (e) {
      this.addQuery();
    }
  },
};
</script>
