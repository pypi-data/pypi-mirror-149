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
  <div class="context-menu"
       v-if="visible"
       :style="style"
       @mouseleave.prevent
       @mouseover.prevent
       @contextmenu.prevent
       @wheel.stop
       ref="menu">
    <search v-if="searchBar" v-model="filter" @search="onSearch"></search>
    <item v-for="item in filtered" :key="item.title" :item="item" :args="args" :delay="delay / 2"></item>
  </div>
</template>

<style lang="scss" scoped>
@import 'styles/workflows/workflow-editor.scss';

.context-menu {
  left: 0;
  margin-left: -$context-menu-width * 0.5;
  margin-top: -20px;
  padding: 10px;
  position: fixed;
  top: 0;
  width: $context-menu-width;
  z-index: 1000;

  .search {
    @extend .item
  }
}
</style>

<script>
import {Menu} from 'rete-context-menu-plugin';

import Item from 'Item.vue';
import Search from 'Search.vue';

export default {
  extends: Menu,
  components: {Item, Search},
  data() {
    return {
      maxItems: 5,
    };
  },
  computed: {
    filtered() {
      if (!this.filter) {
        return this.items;
      }

      const regex = new RegExp(this.filter, 'i');
      const items = [];

      for (const item of this.extractLeafs(this.items)) {
        if (this.searchKeep(item.title) || item.title.match(regex)) {
          if (items.length === this.maxItems) {
            items.push({title: '...', onClick: () => this.maxItems += 5, keepOpen: true});
            break;
          }

          items.push(item);
        }
      }

      return items;
    },
  },
  watch: {
    filter() {
      this.maxItems = 5;
    },
  },
};
</script>
