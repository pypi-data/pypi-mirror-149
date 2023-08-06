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
    <label class="form-control-label" :for="field.id">{{ field.label }}</label>
    <div class="form-group" :class="{'required': field.validation.required}">
      <div class="input-group">
        <div class="input-group-prepend" v-if="fileSelected">
          <button type="button" class="btn btn-sm clear-btn" @click="clearFiles">
            <i class="fa-solid fa-xmark"></i>
          </button>
        </div>
        <div class="custom-file">
          <input type="file"
                 class="custom-file-input"
                 :lang="kadi.globals.locale"
                 :id="field.id"
                 :name="field.name"
                 :required="field.validation.required"
                 :accept="mimetypes"
                 :disabled="disabled"
                 @change="changeFile"
                 ref="files">
          <label class="custom-file-label" :class="{'has-error': field.errors.length > 0 || errorMessage}">
            {{ message }}
          </label>
        </div>
      </div>
      <div v-for="error in field.errors" :key="error" class="invalid-feedback">{{ error }}</div>
      <div class="invalid-feedback">{{ errorMessage }}</div>
      <small class="form-text text-muted" v-if="field.errors.length === 0 && !errorMessage">{{ description }}</small>
    </div>
  </div>
</template>

<style scoped>
.clear-btn {
  background-color: white;
  border: 1px solid #ced4da;
  color: #aab7b8;
  padding-left: 0.75rem;
  padding-right: 0.75rem;
}
</style>

<script>
export default {
  data() {
    return {
      message: '',
      defaultMessage: $t('No file selected'),
      errorMessage: null,
      fileSelected: false,
    };
  },
  props: {
    field: Object,
    mimetypes: Array,
    maxSize: Number,
    disabled: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    description() {
      let description = `${$t('Maximum permitted file size:')} ${kadi.utils.filesize(this.maxSize)}`;
      if (this.field.description) {
        description = `${this.field.description} ${description}`;
      }
      return description;
    },
  },
  watch: {
    disabled() {
      if (this.disabled) {
        this.clearFiles();
        this.errorMessage = null;
      }
    },
  },
  methods: {
    clearFiles() {
      this.message = this.defaultMessage;
      this.fileSelected = false;
      this.$refs.files.value = '';
    },
    changeFile(e) {
      const file = e.target.files[0];
      this.message = file.name;
      this.fileSelected = true;

      if (this.maxSize > 0) {
        if (file.size > this.maxSize) {
          this.errorMessage = $t('File exceeds the maximum size.');
          this.clearFiles();
        } else {
          this.errorMessage = null;
        }
      }
    },
  },
  mounted() {
    this.message = this.defaultMessage;
  },
};
</script>
