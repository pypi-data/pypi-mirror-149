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
  <dynamic-pagination :endpoint="endpoint" :placeholder="placeholder" :per-page="perPage" :enable-filter="enableFilter">
    <template #default="paginationProps">
      <div class="row">
        <div class="col-lg-4">
          <p>
            <strong>{{ title }}</strong>
            <span class="badge badge-pill badge-light text-muted border border-muted">{{ paginationProps.total }}</span>
          </p>
        </div>
        <div class="col-lg-8">
          <slot></slot>
        </div>
      </div>
      <card-deck :items="paginationProps.items">
        <template #default="props">
          <div class="card-body py-2">
            <a :is="getLink(props.item) ? 'a' : 'div'" :href="getLink(props.item)" :class="getLinkClass(props.item)">
              <div v-if="props.item.user">
                <img class="img-thumbnail float-xl-right mb-2 ml-xl-2"
                     width="75"
                     :src="props.item.user._links.image"
                     v-if="props.item.user._links.image">
                <strong>{{ props.item.user.identity.displayname }}</strong>
                <br>
                <small>@{{ props.item.user.identity.username }}</small>
                <br>
                <small class="text-muted">{{ $t('Account type:') }} {{ props.item.user.identity.identity_name }}</small>
              </div>
              <div v-if="props.item.group">
                <img class="img-thumbnail float-xl-right mb-2 ml-xl-2"
                     width="75"
                     :src="props.item.group._links.image"
                     v-if="props.item.group._links.image">
                <basic-resource-info :resource="props.item.group"></basic-resource-info>
              </div>
            </a>
          </div>
          <div class="card-footer d-flex justify-content-between align-items-center py-1">
            <strong class="text-primary">{{ props.item.role.name | capitalize }}</strong>
            <span class="badge badge-light border border-muted font-weight-normal"
                  v-if="props.item.user && creator === props.item.user.id">
              {{ $t('Creator') }}
            </span>
          </div>
        </template>
      </card-deck>
    </template>
  </dynamic-pagination>
</template>

<script>
export default {
  props: {
    title: String,
    placeholder: String,
    endpoint: String,
    creator: {
      type: Number,
      default: null,
    },
    perPage: {
      type: Number,
      default: 6,
    },
    enableFilter: {
      type: Boolean,
      default: true,
    },
  },
  methods: {
    getLink(item) {
      return item.user ? item.user._links.view : (item.group._links ? item.group._links.view : '');
    },
    getLinkClass(item) {
      return (item.group && !item.group._links) ? 'text-muted' : 'stretched-link';
    },
  },
};
</script>
