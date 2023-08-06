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
  <span>
    <span class="badge badge-primary badge-mt-plus font-weight-normal float-right ml-3"
          v-if="!compactLayout && resource.type">
      <!-- Kind of a hacky check whether we are dealing with a template or not. -->
      <span v-if="resource.data">{{ resource.type | capitalize }}</span>
      <span v-else>{{ resource.type | truncate(25) }}</span>
    </span>
    <small>
      <i class="fa-solid mr-1"
         :class="{'fa-lock-open': resource.visibility === 'public', 'fa-lock': resource.visibility === 'private'}">
      </i>
    </small>
    <strong>{{ resource.title }}</strong>
    <br>
    <small>@{{ resource.identifier }}</small>
    <span v-if="!compactLayout">
      <br>
      <small class="text-muted" v-if="resource.plain_description">
        {{ resource.plain_description | truncate(100) }}
      </small>
      <small class="text-muted" v-else>
        <em>{{ $t('No description.') }}</em>
      </small>
    </span>
  </span>
</template>

<script>
export default {
  props: {
    resource: Object,
    compactLayout: {
      type: Boolean,
      default: false,
    },
  },
};
</script>
