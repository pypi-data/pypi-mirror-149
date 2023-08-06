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
    <div class="progress border mt-1" style="height: 5px;">
      <div class="progress-bar text-dark" :class="`bg-${strength.accent}`" :style="{width: strength.progress + '%'}">
      </div>
    </div>
    <small class="float-right" :class="`text-${strength.accent}`">{{ strength.text }}</small>
  </div>
</template>

<script>
import zxcvbn from 'zxcvbn';

export default {
  props: {
    input: String,
  },
  computed: {
    strength() {
      if (this.input.length === 0) {
        return {accent: 'danger', progress: 0, text: ''};
      }

      const score = zxcvbn(this.input).score;
      switch (score) {
      case 0: return {accent: 'danger', progress: 20, text: $t('Very weak')};
      case 1: return {accent: 'danger', progress: 40, text: $t('Weak')};
      case 2: return {accent: 'warning', progress: 60, text: $t('Medium')};
      case 3: return {accent: 'success', progress: 80, text: $t('Good')};
      case 4: return {accent: 'success', progress: 100, text: $t('Very good')};
      default: return {};
      }
    },
  },
};
</script>
