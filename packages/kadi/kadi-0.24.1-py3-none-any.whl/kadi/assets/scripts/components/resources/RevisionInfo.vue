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
    <div v-if="initialized">
      <!-- If we don't have a link to the object itself, we probably don't care about the ID anyways. -->
      <div class="row mb-2" v-if="revision._links.view_object">
        <span class="col-md-2">{{ $t('Object ID') }}</span>
        <a class="col-md-10" :href="revision._links.view_object">
          <strong>{{ revision.object_id }}</strong>
        </a>
      </div>
      <div class="row">
        <span class="col-md-2">{{ $t('Revision ID') }}</span>
        <span class="col-md-10">{{ revision.id }}</span>
      </div>
      <div class="row mt-2">
        <span class="col-md-2">{{ $t('User') }}</span>
        <identity-popover class="col-md-10" :user="revision.revision.user"></identity-popover>
      </div>
      <div class="row mt-2">
        <span class="col-md-2">{{ $t('Timestamp') }}</span>
        <div class="col-md-10">
          <local-timestamp :timestamp="revision.revision.timestamp"></local-timestamp>
          <br>
          <small class="text-muted">
            (<from-now :timestamp="revision.revision.timestamp"></from-now>)
          </small>
        </div>
      </div>
      <hr>
      <div v-for="(value, prop, index) in revision.data" :key="prop">
        <!-- First line, containing the property and either the unchanged value or the potential previous value. -->
        <div class="row">
          <span class="col-md-2">
            <strong>{{ prop | capitalize }}</strong>
          </span>
          <!-- Unchanged value. -->
          <div class="col-md-10" v-if="!revision.diff[prop]">
            <pre class="d-inline ws-pre-wrap" v-if="value !== null">{{ revisionValue(value) }}</pre>
            <pre class="d-inline" v-else><em>null</em></pre>
          </div>
          <!-- Potential previous value. -->
          <div class="col-md-10 diff-delete" v-if="revision.diff[prop]">
            <pre class="crossed d-inline ws-pre-wrap"
                 v-if="revision.diff[prop]['prev'] !== null">{{ revisionValue(revision.diff[prop]['prev']) }}</pre>
            <pre class="crossed text-muted d-inline" v-else><em>null</em></pre>
          </div>
        </div>
        <!-- Second line, containing the potential new value. -->
        <div class="row" v-if="revision.diff[prop]">
          <div class="col-md-10 offset-md-2 diff-add">
            <pre class="d-inline ws-pre-wrap"
                 v-if="revision.diff[prop]['new'] !== null">{{ revisionValue(revision.diff[prop]['new']) }}</pre>
            <pre class="text-muted d-inline" v-else><em>null</em></pre>
          </div>
        </div>
        <br v-if="index < Object.keys(revision.data).length - 1">
      </div>
    </div>
    <i class="fa-solid fa-circle-notch fa-spin" v-if="!initialized"></i>
  </div>
</template>

<style scoped>
.diff-add {
  background-color: #ecfdf0;
}

.diff-delete {
  background-color: #fbe9eb;
}
</style>

<script>
export default {
  data() {
    return {
      revision: null,
      initialized: false,
    };
  },
  props: {
    endpoint: String,
  },
  methods: {
    revisionValue(value) {
      // Visualize an empty string using two double quotes.
      return value === '' ? '""' : value;
    },
  },
  mounted() {
    axios.get(this.endpoint)
      .then((response) => {
        this.revision = response.data;
        this.initialized = true;
      })
      .catch((error) => kadi.alert($t('Error loading revision.'), {request: error.request}));
  },
};
</script>
