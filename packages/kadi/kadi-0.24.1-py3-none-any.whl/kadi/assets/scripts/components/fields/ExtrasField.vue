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
  <extras-editor :id="field.id"
                 :name="field.name"
                 :label="field.label"
                 :initial-values="field.data"
                 :edit-extra-keys="editExtraKeys"
                 :template-endpoint="templateEndpoint"
                 :is-template="isTemplate">
  </extras-editor>
</template>

<script>
export default {
  props: {
    field: Object,
    editExtraKeys: {
      type: Array,
      default: () => [],
    },
    templateEndpoint: {
      type: String,
      default: null,
    },
    isTemplate: {
      type: Boolean,
      default: false,
    },
  },
};
</script>
