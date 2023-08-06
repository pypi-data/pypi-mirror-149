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
  <div class="toast mw-100" data-animation="false" data-autohide="false" data-delay="0" ref="toast">
    <div class="toast-header bg-primary">
      <span class="mr-auto">{{ notification.data.title }}</span>
      <button type="button" class="ml-2 close text-white" @click="dismiss(notification)">
        <i class="fa-solid fa-xmark fa-xs"></i>
      </button>
    </div>
    <div class="toast-body py-2">
      <div class="wb-break-all" v-html="notification.data.body"></div>
      <div class="mt-1">
        <small class="text-muted">
          <from-now :timestamp="notification.created_at"></from-now>
        </small>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    notification: Object,
  },
  methods: {
    dismiss() {
      axios.delete(this.notification._actions.dismiss)
        .then(() => {
          $(this.$refs.toast).toast('dispose');
          kadi.getNotifications();
        })
        .catch((error) => kadi.alert($t('Error dismissing notification.'), {request: error.request}));
    },
  },
  mounted() {
    $(this.$refs.toast).toast('show');
  },
  beforeDestroy() {
    $(this.$refs.toast).toast('dispose');
  },
};
</script>
