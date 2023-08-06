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
  <form :action="action"
        :method="method"
        :enctype="enctype"
        @change="unsavedChanges = true"
        @submit="submit"
        ref="form">
    <slot></slot>
  </form>
</template>

<script>
export default {
  data() {
    return {
      isSubmitted: false,
      unsavedChanges: false,
    };
  },
  props: {
    action: {
      type: String,
      default: '',
    },
    method: {
      type: String,
      default: 'post',
    },
    enctype: {
      type: String,
      default: 'application/x-www-form-urlencoded',
    },
    checkDirty: {
      type: Boolean,
      default: true,
    },
  },
  methods: {
    beforeUnload(e) {
      if (this.unsavedChanges && !this.isSubmitted) {
        e.preventDefault();
        (e || window.event).returnValue = '';
        return '';
      }
      return null;
    },
    submit() {
      this.isSubmitted = true;
      this.$emit('submit');
    },
  },
  mounted() {
    if (this.checkDirty) {
      window.addEventListener('beforeunload', this.beforeUnload);
    }
  },
  beforeDestroy() {
    if (this.checkDirty) {
      window.removeEventListener('beforeunload', this.beforeUnload);
    }
  },
};
</script>
