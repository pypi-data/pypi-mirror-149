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
  <a tabindex="-1" data-toggle="collapse" :href="id" @click="collapseItem">
    <i :class="iconClass"></i>
    <slot>{{ collapseText }}</slot>
  </a>
</template>

<script>
export default {
  data() {
    return {
      isCollapsed_: this.isCollapsed,
      cooldownHandle: null,
    };
  },
  props: {
    id: String,
    isCollapsed: {
      type: Boolean,
      default: false,
    },
    showIconClass: {
      type: String,
      default: 'fa-solid fa-angle-down',
    },
    hideIconClass: {
      type: String,
      default: 'fa-solid fa-angle-up',
    },
  },
  computed: {
    iconClass() {
      return this.isCollapsed_ ? this.showIconClass : this.hideIconClass;
    },
    collapseText() {
      return this.isCollapsed_ ? $t('Show') : $t('Hide');
    },
  },
  watch: {
    isCollapsed() {
      if (this.isCollapsed) {
        this.collapseItem('hide');
      } else {
        this.collapseItem('show');
      }
    },
  },
  methods: {
    collapseItem(collapse = null) {
      if (this.cooldownHandle !== null) {
        return;
      }

      if (collapse === 'hide') {
        this.isCollapsed_ = true;
        // Modifying the parent like this is not very pretty, but much easier in this case.
        $(`#${this.id}`).collapse(collapse);
      } else if (collapse === 'show') {
        this.isCollapsed_ = false;
        $(`#${this.id}`).collapse(collapse);
      } else {
        this.isCollapsed_ = !this.isCollapsed_;
        $(`#${this.id}`).collapse('toggle');
      }

      this.$emit('collapse', this.isCollapsed_);

      this.cooldownHandle = window.setTimeout(() => {
        this.cooldownHandle = null;
      }, 400);
    },
  },
};
</script>
