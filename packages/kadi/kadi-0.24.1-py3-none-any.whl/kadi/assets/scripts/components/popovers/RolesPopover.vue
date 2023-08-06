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
  <popover-toggle toggle-class="btn btn-light" :title="$t('Role permissions')" v-if="roles.length > 0">
    <template #toggle>
      <i class="fa-solid fa-circle-info"></i> {{ $t('Role permissions') }}
    </template>
    <template #content>
      <div v-for="(role, index) in roles" :key="role.name">
        <strong>{{ role.name | capitalize }}</strong>
        <br>
        <div class="row" v-for="action in role.permissions" :key="action.action">
          <div class="col-lg-4">{{ action.action }}</div>
          <div class="col-lg-8">
            <small>{{ action.description }}</small>
          </div>
        </div>
        <hr v-if="index < roles.length - 1">
      </div>
    </template>
  </popover-toggle>
</template>

<script>
export default {
  props: {
    roles: Array,
  },
};
</script>
