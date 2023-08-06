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
  <div class="input-group-append" v-if="input">
    <button type="button" class="btn btn-sm clear-btn" :class="classes" @click="clearInput">
      <i class="fa-solid fa-xmark fa-sm" v-if="small"></i>
      <i class="fa-solid fa-xmark" v-else></i>
    </button>
  </div>
</template>

<style scoped>
.clear-btn {
  background-color: white;
  border: 1px solid #ced4da;
  color: #aab7b8;
}

.clear-btn-normal {
  padding-left: 0.75rem;
  padding-right: 0.75rem;
}

.clear-btn-sm {
  padding-left: 0.5rem;
  padding-right: 0.5rem;
}
</style>

<script>
export default {
  props: {
    input: String,
    small: {
      type: Boolean,
      default: false,
    },
    focusOnClear: {
      type: Boolean,
      default: true,
    },
    inputId: {
      type: String,
      default: null,
    },
  },
  computed: {
    classes() {
      return this.small ? 'clear-btn-sm' : 'clear-btn-normal';
    },
  },
  methods: {
    clearInput() {
      this.$emit('clear-input');
      if (this.focusOnClear && this.inputId !== null) {
        document.getElementById(this.inputId).focus();
      }
    },
  },
};
</script>
