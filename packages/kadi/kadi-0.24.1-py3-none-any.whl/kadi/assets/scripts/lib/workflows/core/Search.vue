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
  <div class="search">
    <input placeholder="Filter" v-model="value_" ref="input" @pointerdown.stop>
  </div>
</template>

<style lang="scss" scoped>
@import 'styles/workflows/workflow-editor.scss';

.search  {
  input {
    background: transparent;
    border: 1px solid $context-menu-accent-color;
    border-radius: 3px;
    box-sizing: border-box;
    font-size: 15px;
    padding: 1px 8px;
    width: 100%;
  }
}
</style>

<script>
import {Search} from 'rete-context-menu-plugin';

export default {
  extends: Search,
  data() {
    return {
      value_: '',
    };
  },
  watch: {
    value() {
      this.value_ = this.value;
    },
    value_() {
      this.$emit('search', this.value_);
    },
  },
  mounted() {
    this.$refs.input.focus();
  },
};
</script>
