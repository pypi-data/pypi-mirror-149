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
        <div class="col-md-6 order-2 order-md-1">
          <p>
            <strong>{{ title }}</strong>
            <span class="badge badge-pill badge-light text-muted border border-muted">{{ paginationProps.total }}</span>
          </p>
        </div>
        <div class="col-md-6 order-1 order-md-2">
          <slot></slot>
        </div>
      </div>
      <card-deck :items="paginationProps.items">
        <template #default="props">
          <div class="card-header py-1">{{ props.item.name }}</div>
          <div class="card-body py-2">
            <a :href="direction === 'out' ? props.item.record_to._links.view : props.item.record_from._links.view"
               class="stretched-link">
              <basic-resource-info :resource="direction === 'out' ? props.item.record_to : props.item.record_from">
              </basic-resource-info>
            </a>
          </div>
          <div class="card-footer py-1">
            <small class="text-muted">
              {{ $t('Created at') }} <local-timestamp :timestamp="props.item.created_at"></local-timestamp>
            </small>
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
    endpoint: String,
    direction: String,
    placeholder: {
      type: String,
      default: $t('No record links.'),
    },
    perPage: {
      type: Number,
      default: 6,
    },
    enableFilter: {
      type: Boolean,
      default: true,
    },
    enableDescription: {
      type: Boolean,
      default: true,
    },
  },
};
</script>
