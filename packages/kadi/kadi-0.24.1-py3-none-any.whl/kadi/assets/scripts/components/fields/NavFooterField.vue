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
  <div class="mb-3">
    <label class="form-control-label">{{ field.label }}</label>
    <div v-for="(item, index) in items" :key="index">
      <div class="form-row" :class="{'mb-4 mb-md-2': index < items.length - 1}">
        <div class="col-md-5 mb-1 mb-md-0">
          <div class="input-group input-group-sm">
            <div class="input-group-prepend">
              <span class="input-group-text">{{ $t('Title') }}</span>
            </div>
            <input class="form-control" v-model.trim="item[0]">
          </div>
        </div>
        <div class="col-md-5 mb-1 mb-md-0">
          <div class="input-group input-group-sm">
            <div class="input-group-prepend">
              <span class="input-group-text">URL</span>
            </div>
            <input class="form-control" v-model.trim="item[1]">
          </div>
        </div>
        <div class="col-md-2 mb-1 mb-md-0 btn-group btn-group-sm">
          <button type="button"
                  class="btn btn-light"
                  :title="$t('Add item')"
                  @click="addItem(index)">
            <i class="fa-solid fa-plus"></i>
          </button>
          <button type="button"
                  class="btn btn-light"
                  :title="$t('Remove item')"
                  @click="removeItem(index)"
                  v-if="items.length > 1">
            <i class="fa-solid fa-xmark"></i>
          </button>
        </div>
      </div>
    </div>
    <small class="form-text text-muted">{{ field.description }}</small>
    <input type="hidden" :name="field.name" :value="serializedItems">
  </div>
</template>

<script>
export default {
  data() {
    return {
      items: [],
    };
  },
  props: {
    field: Object,
  },
  computed: {
    serializedItems() {
      const serializedItems = [];

      for (const item of this.items) {
        if (item[0] !== '' || item[1] !== '') {
          serializedItems.push(item);
        }
      }

      return JSON.stringify(serializedItems);
    },
  },
  methods: {
    addItem(index = null, item = null) {
      const newItem = item !== null ? item : ['', ''];

      if (index !== null) {
        this.items.splice(index + 1, 0, newItem);
      } else {
        this.items.push(newItem);
      }
    },
    removeItem(index) {
      this.items.splice(index, 1);
    },
  },
  mounted() {
    if (this.field.data.length > 0) {
      for (const item of this.field.data) {
        this.addItem(null, item);
      }
    } else {
      this.addItem();
    }
  },
};
</script>
