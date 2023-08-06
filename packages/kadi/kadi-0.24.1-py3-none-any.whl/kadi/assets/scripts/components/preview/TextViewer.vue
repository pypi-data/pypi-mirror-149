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
    <div class="mb-2" v-if="encoding">
      <small class="text-muted">{{ $t('Detected encoding:') }} {{ encoding.toUpperCase() }}</small>
    </div>
    <div :class="{'card bg-light': showBorder}">
      <div class="mt-1 ml-2 mr-0">
        <!-- eslint-disable-next-line max-len -->
        <pre class="max-vh-75 mb-1"><span v-for="(line, index) in lines" :key="index" class="line"><span class="text-muted">{{ lineNum(index) }}  </span>{{ `${line}\n` }}</span></pre>
      </div>
    </div>
  </div>
</template>

<style scoped>
.line:hover {
  background-color: #d9d9d9;
}
</style>

<script>
export default {
  props: {
    lines: Array,
    encoding: {
      type: String,
      default: null,
    },
    showBorder: {
      type: Boolean,
      default: true,
    },
  },
  methods: {
    lineNum(index) {
      return `${' '.repeat(this.lines.length.toString().length - (index + 1).toString().length)}${index + 1}`;
    },
  },
};
</script>
