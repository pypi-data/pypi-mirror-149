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
    <div v-if="!nestedType">
      <div class="d-flex justify-content-between mb-2">
        <div>
          <slot></slot>
        </div>
        <div v-if="hasNestedType">
          <div class="btn-group">
            <button type="button"
                    class="btn btn-link text-muted py-0 pl-0"
                    :disabled="isCollapsing"
                    @click.prevent="collapseExtras(extras_, true)">
              <i class="fa-solid fa-square-minus"></i> {{ $t('Collapse all') }}
            </button>
            <button type="button"
                    class="btn btn-link text-muted py-0 pr-0"
                    :disabled="isCollapsing"
                    @click.prevent="collapseExtras(extras_, false)">
              <i class="fa-solid fa-square-plus"></i> {{ $t('Expand all') }}
            </button>
          </div>
        </div>
      </div>
    </div>
    <ul class="list-group mb-2">
      <li class="list-group-item extra py-1 pl-3 pr-0"
          :class="{'extra-nested': depth % 2 == 1}"
          v-for="(extra, index) in extras_"
          :key="extra.id">
        <div class="row align-items-center"
             :class="{'mb-1': kadi.utils.isNestedType(extra.type) && extra.value.length > 0 && !extra.isCollapsed}">
          <!-- Key. -->
          <div class="col-md-4">
            <span v-if="!kadi.utils.isNestedType(extra.type)">{{ extra.key || `(${index + 1})` }}</span>
            <collapse-item show-icon-class=""
                           hide-icon-class=""
                           :id="extra.id"
                           :is-collapsed="extra.isCollapsed"
                           @collapse="extra.isCollapsed = $event"
                           v-if="kadi.utils.isNestedType(extra.type)">
              <strong>{{ extra.key || `(${index + 1})` }}</strong>
            </collapse-item>
          </div>
          <!-- Value and unit. -->
          <div class="col-md-5">
            <div v-if="!kadi.utils.isNestedType(extra.type)">
              <span v-if="extra.value === null">
                <em>null</em>
              </span>
              <span v-else>
                <span v-if="extra.type !== 'date'">{{ extra.value }}</span>
                <local-timestamp :timestamp="extra.value" v-else></local-timestamp>
              </span>
              <span class="text-muted">{{ extra.unit }}</span>
            </div>
            <collapse-item show-icon-class=""
                           hide-icon-class=""
                           :id="extra.id"
                           :is-collapsed="extra.isCollapsed"
                           @collapse="extra.isCollapsed = $event"
                           v-if="kadi.utils.isNestedType(extra.type) && extra.isCollapsed && extra.value.length > 0">
              <strong>{...}</strong>
            </collapse-item>
          </div>
          <!-- Type. -->
          <div class="col-md-2 d-md-flex justify-content-end">
            <small class="text-muted mr-3">
              {{ extra.type | prettyTypeName | capitalize }}
            </small>
          </div>
          <!-- Edit link and validation toggle. -->
          <div class="col-md-1 d-md-flex justify-content-end">
            <button type="button"
                    class="float-right mr-3 mr-md-0"
                    :title="$t('Toggle validation')"
                    :class="toolbarBtnClasses"
                    @click="extra.showValidation = !extra.showValidation"
                    v-if="extra.validation">
              <i class="fa-solid fa-angle-up" v-if="extra.showValidation"></i>
              <i class="fa-solid fa-angle-down" v-else></i>
              <span class="d-md-none">{{ $t('Toggle validation') }}</span>
            </button>
            <a :title="$t('Edit extra')"
               :class="toolbarBtnClasses"
               :href="getEditLink(extra, index)"
               v-if="editEndpoint">
              <i class="fa-solid fa-pencil"></i>
              <span class="d-md-none">{{ $t('Edit extra') }}</span>
            </a>
          </div>
        </div>
        <div v-if="extra.showValidation">
          <hr class="my-1">
          <div class="row text-muted mb-2 mb-md-0" v-for="(value, key) in extra.validation" :key="key">
            <div class="col-md-4">{{ key | capitalize }}</div>
            <div class="col-md-8">{{ value }}</div>
          </div>
        </div>
        <div v-if="kadi.utils.isNestedType(extra.type) && extra.value.length > 0">
          <div :id="extra.id" class="collapse show">
            <extras-viewer :extras="extra.value"
                           :edit-endpoint="editEndpoint"
                           :nested-type="extra.type"
                           :nested-keys="[...nestedKeys, extra.key || index]"
                           :depth="depth + 1">
            </extras-viewer>
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>

<style lang="scss" scoped>
.extra {
  margin-right: -1px;
}

.extra-nested {
  background-color: #f2f2f2;
}

.text-toolbar {
  color: lighten(#95a5a6, 15%);
}
</style>

<script>
export default {
  data() {
    return {
      extras_: this.extras,
      isCollapsing: false,
    };
  },
  props: {
    extras: Array,
    editEndpoint: {
      type: String,
      default: null,
    },
    editParam: {
      type: String,
      default: 'key',
    },
    nestedType: {
      type: String,
      default: null,
    },
    nestedKeys: {
      type: Array,
      default: () => [],
    },
    depth: {
      type: Number,
      default: 0,
    },
  },
  computed: {
    toolbarBtnClasses() {
      return 'btn btn-sm text-toolbar py-0 px-0 px-md-2 mr-1';
    },
    hasNestedType() {
      for (const extra of this.extras_) {
        if (kadi.utils.isNestedType(extra.type)) {
          return true;
        }
      }
      return false;
    },
  },
  methods: {
    visitExtras(extras, callback) {
      extras.forEach((extra) => {
        callback(extra);
        if (kadi.utils.isNestedType(extra.type)) {
          this.visitExtras(extra.value, callback);
        }
      });
    },
    collapseExtras(extras, collapse) {
      this.isCollapsing = true;
      this.visitExtras(extras, (extra) => extra.isCollapsed = collapse);
      // Take the collapse cooldown into account.
      window.setTimeout(() => this.isCollapsing = false, 400);
    },
    getEditLink(extra, index) {
      const url = new URL(this.editEndpoint);
      const params = new URLSearchParams(url.search);

      for (const key of this.nestedKeys) {
        params.append(this.editParam, key);
      }
      params.append(this.editParam, extra.key || index);


      url.search = params;
      return url.toString();
    },
  },
  created() {
    this.visitExtras(this.extras_, (extra) => {
      extra.id = kadi.utils.randomAlnum();
      this.$set(extra, 'showValidation', false);
      this.$set(extra, 'isCollapsed', false);
    });
  },
};
</script>
