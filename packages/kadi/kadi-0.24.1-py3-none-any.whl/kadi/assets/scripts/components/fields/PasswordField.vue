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
  <base-field :field="field" ref="base">
    <template #default="props">
      <input type="password"
             :id="field.id"
             :name="field.name"
             :required="field.validation.required"
             :disabled="disabled"
             :class="[{'has-error': props.hasError}, classes]"
             v-model="input">
      <slot></slot>
    </template>
  </base-field>
</template>

<script>
export default {
  data() {
    return {
      input: '',
    };
  },
  props: {
    field: Object,
    disabled: {
      type: Boolean,
      default: false,
    },
    classes: {
      type: String,
      default: 'form-control',
    },
  },
  watch: {
    input() {
      this.$emit('input', this.input);
      this.$refs.base.validate(this.input);
    },
  },
};
</script>
