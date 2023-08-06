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
  <div :class="{'card': showBorder}">
    <div class="card-header py-2" v-if="title">{{ title }}</div>
    <div :class="{'card-body p-3': showBorder}">
      <select class="custom-select custom-select-sm" v-model="value">
        <option v-for="choice in choices" :key="choice[0]" :value="choice[0]">{{ choice[1] }}</option>
      </select>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      value: null,
      initialized: false,
    };
  },
  props: {
    param: String,
    choices: Array,
    title: {
      type: String,
      default: null,
    },
    showBorder: {
      type: Boolean,
      default: true,
    },
  },
  watch: {
    value() {
      if (this.initialized) {
        const url = kadi.utils.setSearchParam(this.param, this.value);
        kadi.utils.replaceState(url);
        this.$emit('search');
      }
    },
  },
  mounted() {
    this.value = this.choices[0][0];

    if (kadi.utils.hasSearchParam(this.param)) {
      const param = kadi.utils.getSearchParam(this.param);

      for (const choice of this.choices) {
        if (choice[0] === param) {
          this.value = param;

          // Skip first potential change.
          this.$nextTick(() => this.initialized = true);
          return;
        }
      }

      // If the parameter value exists but is invalid, replace it with the default.
      const url = kadi.utils.setSearchParam(this.param, this.value);
      kadi.utils.replaceState(url);
    }

    this.$nextTick(() => this.initialized = true);
  },
};
</script>
