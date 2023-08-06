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
  <div class="card bg-light" v-if="showLangPrompt">
    <div class="card-body py-3">
      <div class="row align-items-center">
        <div class="col-lg-9">
          Based on your browser settings, you seem to prefer a different language. Do you want to change the current
          language?
        </div>
        <div class="col-lg-3 mt-2 mt-lg-0 d-lg-flex justify-content-end">
          <div>
            <button class="btn btn-sm btn-primary" @click="switchLanguage">Yes</button>
            <button class="btn btn-sm btn-light" @click="dismissPrompt">No</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      storageKey: 'hide_lang_prompt',
      showLangPrompt: false,
    };
  },
  props: {
    preferredLocale: String,
  },
  methods: {
    switchLanguage() {
      this.dismissPrompt();
      window.location.href = `?locale=${this.preferredLocale}`;
    },
    dismissPrompt() {
      window.localStorage.setItem(this.storageKey, 'true');
      this.showLangPrompt = false;
    },
  },
  mounted() {
    if (this.preferredLocale !== kadi.globals.locale && window.localStorage.getItem(this.storageKey) === null) {
      this.showLangPrompt = true;
    }
  },
};
</script>
