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
  <div :class="{'card bg-light max-vh-75 overflow-auto': !isNested}">
    <div :class="{'mt-3 mr-4': !isNested}">
      <ul>
        <li v-for="entry in entries_" :key="entry.id">
          <div class="d-flex justify-content-between entry px-1" v-if="!entry.is_dir">
            <div class="max-w-75">
              <i class="fa-solid fa-file"></i> {{ entry.name }}
            </div>
            <small>{{ entry.size | filesize }}</small>
          </div>
          <div v-if="entry.is_dir">
            <collapse-item class="px-1"
                           show-icon-class="fa-solid fa-folder"
                           hide-icon-class="fa-solid fa-folder-open"
                           :id="entry.id">
              <strong>{{ entry.name }}</strong>
            </collapse-item>
            <archive-viewer class="collapse show" :id="entry.id" :entries="entry.children" :is-nested="true">
            </archive-viewer>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.entry:hover {
  background-color: #d9d9d9;
}
</style>

<script>
export default {
  data() {
    return {
      entries_: [],
    };
  },
  props: {
    entries: Array,
    isNested: {
      type: Boolean,
      default: false,
    },
  },
  mounted() {
    this.entries.forEach((entry) => {
      entry.id = kadi.utils.randomAlnum();
      this.entries_.push(entry);
    });
  },
};
</script>
