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
  <div class="card" v-if="showBroadcastMsg">
    <div class="card-body pb-1">
      <button type="button" class="close text-primary" @click="dismissBroadcast">
        <i class="fa-solid fa-xmark fa-xs"></i>
      </button>
      <markdown-preview :input="message"></markdown-preview>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      storageKey: 'hide_broadcast_msg',
      showBroadcastMsg: false,
    };
  },
  props: {
    message: String,
    hash: String,
  },
  methods: {
    dismissBroadcast() {
      // Store the hash of the broadcast message in the local storage when dismissing it.
      window.localStorage.setItem(this.storageKey, this.hash);
      this.showBroadcastMsg = false;
    },
  },
  mounted() {
    // If the broadcast message is not empty, check if it changed since the last time it was dismissed based on its
    // hash. If it did, show it and delete the old hash from the local storage, if applicable.
    if (this.message === '') {
      window.localStorage.removeItem(this.storageKey);
    } else if (window.localStorage.getItem(this.storageKey) !== this.hash) {
      window.localStorage.removeItem(this.storageKey);
      this.showBroadcastMsg = true;
    }
  },
};
</script>
