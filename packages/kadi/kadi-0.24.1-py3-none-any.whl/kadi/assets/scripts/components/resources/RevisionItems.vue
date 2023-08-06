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
  <dynamic-pagination :endpoint="endpoint" :placeholder="$t('No revisions.')" ref="pagination">
    <template #default="props">
      <p v-if="title">
        <strong>{{ title }}</strong>
        <span class="badge badge-pill badge-light text-muted border border-muted">{{ props.total }}</span>
      </p>
      <div v-for="(revision, index) in props.items"
           :key="revision.id"
           :class="{'mb-3': index < props.items.length - 1}">
        <div class="form-row align-items-center">
          <div class="col-xl-1 d-xl-flex justify-content-center">
            <span v-if="revision.data.state === activeState">
              <span v-if="revision.diff.state">
                <span v-if="revision.diff.state.prev === null">
                  <span class="fa-stack">
                    <i class="fa-solid fa-circle fa-stack-2x text-success"></i>
                    <i class="fa-solid fa-plus fa-stack-1x text-white"></i>
                  </span>
                </span>
                <span v-else>
                  <span class="fa-stack">
                    <i class="fa-solid fa-circle fa-stack-2x text-info"></i>
                    <i class="fa-solid fa-trash-arrow-up fa-stack-1x text-white"></i>
                  </span>
                </span>
              </span>
              <span v-if="!revision.diff.state">
                <span class="fa-stack">
                  <i class="fa-solid fa-circle fa-stack-2x text-primary"></i>
                  <i class="fa-solid fa-pencil fa-stack-1x text-white"></i>
                </span>
              </span>
            </span>
            <span v-if="revision.data.state === deletedState">
              <span class="fa-stack">
                <i class="fa-solid fa-circle fa-stack-2x text-danger"></i>
                <i class="fa-solid fa-trash fa-stack-1x text-white"></i>
              </span>
            </span>
          </div>
          <div class="col-xl-8">
            <identity-popover :user="revision.revision.user"></identity-popover>
            <span v-if="revision.data.state === activeState">
              <span v-if="revision.diff.state">
                <span v-if="revision.diff.state.prev === null">{{ $t('created', {context: 'revision'}) }}</span>
                <span v-else>restored</span>
              </span>
              <span v-if="!revision.diff.state">{{ $t('updated', {context: 'revision'}) }}</span>
            </span>
            <span v-if="revision.data.state === deletedState">{{ $t('deleted', {context: 'revision'}) }}</span>
            <slot :revision="revision">
              <strong>{{ revision.data.title }}</strong>
            </slot>
            <br>
            <a :href="revision._links.view">
              <i class="fa-solid fa-eye"></i> {{ $t('View revision') }}
            </a>
          </div>
          <div class="col-xl-3 d-xl-flex justify-content-end">
            <small class="text-muted">
              <from-now :timestamp="revision.revision.timestamp"></from-now>
            </small>
          </div>
        </div>
      </div>
    </template>
  </dynamic-pagination>
</template>

<script>
export default {
  props: {
    endpoint: String,
    title: {
      type: String,
      default: '',
    },
    activeState: {
      type: String,
      default: 'active',
    },
    deletedState: {
      type: String,
      default: 'deleted',
    },
  },
  methods: {
    // Convenience function for forcing an update from outside.
    update() {
      this.$refs.pagination.update();
    },
  },
};
</script>
