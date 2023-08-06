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
    <div v-for="(extra, index) in extras" :key="extra.id">
      <div class="row mb-2 mb-md-0">
        <div class="col-md-9">
          <div class="d-flex align-items-center">
            <collapse-item class="mr-2"
                           show-icon-class="fa-solid fa-square-plus"
                           hide-icon-class="fa-solid fa-square-minus"
                           :id="extra.id"
                           v-if="kadi.utils.isNestedType(extra.type.value)">
              <span></span>
            </collapse-item>
            <button type="button"
                    class="btn btn-link text-primary text-left w-100 px-0 py-1 key"
                    @click="$emit('focus-extra', extra)">
              <strong>{{ extra.key.value || `(${index + 1})` }}</strong>
            </button>
          </div>
        </div>
        <div class="col-md-3 d-md-flex justify-content-end">
          <small class="text-muted">{{ extra.type.value | prettyTypeName | capitalize }}</small>
        </div>
      </div>
      <div class="border-dotted pl-5 ml-1 collapse show"
           :id="extra.id"
           v-if="kadi.utils.isNestedType(extra.type.value)">
        <extras-editor-tree-view :extras="extra.value.value" @focus-extra="$emit('focus-extra', $event)">
        </extras-editor-tree-view>
      </div>
    </div>
  </div>
</template>

<style scoped>
.border-dotted {
  border-left: 1px dotted #2c3e50;
}

.key:hover {
  background-color: #dee6ed;
}
</style>

<script>
export default {
  props: {
    extras: Array,
  },
};
</script>
