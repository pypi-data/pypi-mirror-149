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
  <div class="card">
    <div class="card-header py-2 d-flex justify-content-between align-items-center">
      {{ title }}
      <button type="button" class="btn btn-link text-muted p-0" v-if="items.length > 0" @click="clearItems">
        <i class="fa-solid fa-xmark"></i>
      </button>
    </div>
    <div class="card-body p-3">
      <div class="mb-3" v-if="items.length > 0">
        <span class="item badge badge-primary font-weight-normal mb-1 mx-1"
              :title="item.text"
              v-for="item in items"
              :key="item.id">
          {{ item.text | truncate(25) }}
          <button type="button" class="btn text-white p-0 ml-2" @click="removeItem(item)">
            <i class="fa-solid fa-xmark fa-sm"></i>
          </button>
        </span>
      </div>
      <dynamic-selection container-classes="select2-single-sm"
                         :endpoint="endpoint"
                         :placeholder="placeholder"
                         :reset-on-select="true"
                         @select="addItem">
      </dynamic-selection>
    </div>
    <slot></slot>
  </div>
</template>

<style lang="scss" scoped>
.item {
  cursor: default;
  white-space: normal;
  word-break: break-all;

  button {
    line-height: 15px;
  }
}
</style>

<script>
export default {
  data() {
    return {
      items: [],
    };
  },
  props: {
    param: String,
    endpoint: String,
    title: String,
    placeholder: String,
    initialValues: {
      type: Array,
      default: null,
    },
  },
  methods: {
    clearItems() {
      const url = kadi.utils.removeSearchParam(this.param);
      kadi.utils.replaceState(url);

      this.items = [];
      this.$emit('search');
    },
    addItem(item, search = true) {
      for (const _item of this.items) {
        if (_item.id === item.id) {
          this.removeItem(item);
          return;
        }
      }
      this.items.push({id: item.id, text: item.text});

      if (search) {
        const url = kadi.utils.setSearchParam(this.param, item.id, false);
        kadi.utils.replaceState(url);
        this.$emit('search');
      }
    },
    removeItem(item) {
      const url = kadi.utils.removeSearchParam(this.param, item.id);
      kadi.utils.replaceState(url);

      let index = 0;
      for (const _item of this.items) {
        if (_item.id === item.id) {
          this.items.splice(index, 1);
          break;
        }
        index++;
      }
      this.$emit('search');
    },
  },
  mounted() {
    // Always prefer the given initial values.
    if (this.initialValues !== null) {
      for (const value of this.initialValues) {
        this.addItem({id: value[0], text: value[1]}, false);
      }
    } else if (kadi.utils.hasSearchParam(this.param)) {
      for (const param of kadi.utils.getSearchParam(this.param, true)) {
        this.addItem({id: param, text: param}, false);
      }
    }
  },
};
</script>
