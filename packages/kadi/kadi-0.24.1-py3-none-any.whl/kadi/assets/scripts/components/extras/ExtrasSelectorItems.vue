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
  <div>
    <div v-for="(extra, index) in extras" :key="extra.id">
      <div class="row mb-2 mb-md-0">
        <div class="col-md-10">
          <div class="form-check form-check-inline">
            <input type="checkbox"
                   class="form-check-input"
                   :id="`checkbox-${extra.id}`"
                   :checked="extra.checked"
                   :disabled="extra.disabled"
                   @click="checkExtra(extra, $event.target.checked)">
            <label class="form-check-label key"
                   :for="`checkbox-${extra.id}`"
                   v-if="!kadi.utils.isNestedType(extra.type)">
              {{ extra.key || `(${index + 1})` }}
            </label>
            <collapse-item show-icon-class=""
                           hide-icon-class=""
                           :id="extra.id"
                           :is-collapsed="extra.collapsed"
                           @collapse="extra.collapsed = $event"
                           v-else>
              <strong class="key" :class="{'text-muted': extra.disabled}">{{ extra.key || `(${index + 1})` }}</strong>
            </collapse-item>
          </div>
        </div>
        <div class="col-md-2 d-md-flex justify-content-end">
          <small class="text-muted ml-4 ml-md-0">{{ extra.type | prettyTypeName | capitalize }}</small>
        </div>
      </div>
      <div class="collapse" :id="extra.id" v-if="kadi.utils.isNestedType(extra.type)">
        <extras-selector-items class="border-dotted pl-5 ml-2" :extras="extra.value"></extras-selector-items>
      </div>
    </div>
  </div>
</template>

<style scoped>
.border-dotted {
  border-left: 1px dotted #2c3e50;
}

.key {
  word-break: break-all;
}
</style>

<script>
export default {
  props: {
    extras: Array,
  },
  methods: {
    checkExtra(extra, checked, disable = false) {
      let extras = extra;
      if (!Array.isArray(extras)) {
        extras = [extras];
      }

      extras.forEach((extra) => {
        extra.checked = checked;

        if (disable) {
          extra.disabled = extra.checked;
        }
        if (kadi.utils.isNestedType(extra.type)) {
          this.checkExtra(extra.value, checked, true);
        }
      });
    },
  },
};
</script>
