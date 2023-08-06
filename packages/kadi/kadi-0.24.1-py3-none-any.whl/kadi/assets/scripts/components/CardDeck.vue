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
    <div class="card-deck"
         :class="{'mb-4': groupIndex < groupedItems.length - 1}"
         v-for="(itemGroup, groupIndex) in groupedItems"
         :key="itemGroup.id">
      <div class="card card-action"
           :class="index - 1 < itemGroup.items.length ? classes : 'border-0'"
           v-for="index in numCards_"
           :key="index">
        <slot :item="itemGroup.items[index - 1]" v-if="index - 1 < itemGroup.items.length"></slot>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      numCards_: this.numCards,
    };
  },
  props: {
    items: Array,
    numCards: {
      type: Number,
      default: 3,
    },
    classes: {
      type: String,
      default: '',
    },
    isResponsive: {
      type: Boolean,
      default: true,
    },
  },
  computed: {
    groupedItems() {
      const items = [];
      for (let i = 0; i < this.items.length; i += this.numCards_) {
        const itemGroup = {id: i, items: []};
        for (let j = i; j < this.items.length && j < i + this.numCards_; j++) {
          itemGroup.items.push(this.items[j]);
        }
        items.push(itemGroup);
      }
      return items;
    },
  },
  methods: {
    adjustNumCards() {
      const viewportWidth = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
      // Base the number of cards on some of the regular Bootstrap breakpoins.
      if (viewportWidth < 768) {
        this.numCards_ = Math.round(this.numCards / 3);
      } else if (viewportWidth < 1200) {
        this.numCards_ = Math.round(this.numCards / 2);
      } else {
        this.numCards_ = this.numCards;
      }
    },
  },
  mounted() {
    if (this.isResponsive) {
      this.adjustNumCards();
      window.addEventListener('resize', this.adjustNumCards);
    }
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.adjustNumCards);
  },
};
</script>
