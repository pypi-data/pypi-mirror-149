<!-- Copyright 2022 Karlsruhe Institute of Technology
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
    <div v-if="fileSize > maxFileSize && !forceLoad">
      <button class="btn btn-sm btn-light mb-2" @click="forceLoad = true">
        <i class="fa-solid fa-eye"></i> {{ $t('Load preview') }}
      </button>
    </div>
    <div v-else>
      <div class="border border-muted bg-light text-center" v-if="previewType === 'image'">
        <img class="img-fluid" :src="url">
      </div>
      <iframe class="w-100 vh-75 border border-muted rounded"
              frameborder="0"
              allowfullscreen
              :src="url"
              v-if="previewType === 'pdf'">
      </iframe>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      forceLoad: false,
      maxFileSize: 25 * (10 ** 6), // 25 MB.
    };
  },
  props: {
    previewType: String,
    url: String,
    fileSize: Number,
  },
};
</script>
