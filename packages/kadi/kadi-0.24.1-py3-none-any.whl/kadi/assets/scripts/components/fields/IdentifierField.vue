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
      <div class="input-group">
        <input :id="field.id"
               :name="field.name"
               :required="field.validation.required"
               :class="[{'has-error': props.hasError}, classes]"
               :readonly="!editIdentifier"
               v-model="identifier"
               ref="input">
        <div class="input-group-append" v-if="input !== null">
          <button type="button"
                  class="input-group-text btn"
                  :title="editIdentifier ? $t('Revert to default') : $t('Edit identifier')"
                  @click="toggleEdit">
            <i class="fa-solid fa-pencil" v-if="!editIdentifier"></i>
            <i class="fa-solid fa-rotate-left" v-if="editIdentifier"></i>
          </button>
        </div>
      </div>
    </template>
  </base-field>
</template>

<script>
export default {
  data() {
    return {
      identifier: this.field.data,
      editIdentifier: false,
    };
  },
  props: {
    field: Object,
    input: {
      type: String,
      default: null,
    },
    classes: {
      type: String,
      default: 'form-control form-control-sm',
    },
  },
  watch: {
    input() {
      if (!this.editIdentifier) {
        this.identifier = this.generateIdentifier(this.input);
      }
    },
    identifier() {
      const identifier = this.generateIdentifier(this.identifier);
      const selectionStart = this.$refs.input.selectionStart;

      if (this.identifier !== identifier) {
        // Prevent the cursor from jumping to the end of the input.
        this.$nextTick(() => this.$refs.input.selectionEnd = selectionStart);
      }

      this.identifier = identifier;
      this.$emit('identifier', this.identifier);
      this.$refs.base.validate(this.identifier);
    },
  },
  methods: {
    toggleEdit() {
      this.editIdentifier = !this.editIdentifier;
      if (!this.editIdentifier) {
        this.identifier = this.generateIdentifier(this.input);
      }
    },
    generateIdentifier(value) {
      let identifier = value;

      identifier = identifier.toLowerCase();
      identifier = identifier.replace(/[^a-z0-9-_ ]+/g, '');
      identifier = identifier.replace(/[ ]+/g, '-');

      if (!this.editIdentifier && this.field.validation.max) {
        identifier = identifier.substring(0, this.field.validation.max);
      }

      return identifier;
    },
  },
  mounted() {
    if (this.identifier !== '' || this.input === null) {
      this.editIdentifier = true;
    }
  },
};
</script>
