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
  <!-- Prevent newlines from getting rendered as space. -->
  <span><!--
 --><a tabindex="-1" data-toggle="popover" class="cursor-pointer" :class="toggleClass" ref="toggle"><!--
   --><slot name="toggle"></slot><!--
 --></a><!--
 --><span class="d-none" ref="popoverContent"><!--
   --><slot name="content"></slot><!--
 --></span><!--
 --><span class="d-none" ref="popoverTitle"><!--
   --><slot name="title"><!--
     --><span class="d-flex justify-content-between align-items-center" v-if="title || trigger === 'click'"><!--
       --><strong>{{ title }}</strong><!--
       --><button type="button" :id="closePopoverId" class="btn btn-link text-muted p-0" v-if="trigger === 'click'"><!--
         --><i class="fa-solid fa-xmark"></i><!--
       --></button><!--
     --></span><!--
   --></slot><!--
 --></span><!--
--></span>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      default: null,
    },
    toggleClass: {
      type: String,
      default: 'btn btn-light',
    },
    width: {
      type: String,
      default: '350px',
    },
    placement: {
      type: String,
      default: 'right',
    },
    trigger: {
      type: String,
      default: 'focus',
    },
    closePopoverId: {
      type: String,
      default: 'close-popover',
    },
    container: {
      type: String,
      default: 'body',
    },
  },
  mounted() {
    const vm = this;

    $(vm.$refs.toggle).popover({
      container: this.container,
      placement: this.placement,
      trigger: this.trigger,
      html: true,
      title: () => $(vm.$refs.popoverTitle).html(),
      content: () => $(vm.$refs.popoverContent).html(),
    }).on('inserted.bs.popover', function() {
      $($(this).data('bs.popover').getTipElement()).css('width', vm.width);
    });

    if (this.trigger === 'click') {
      $(document).on('click', `#${vm.closePopoverId}`, () => $(vm.$refs.toggle).popover('hide'));
    }
  },
  beforeDestroy() {
    $(this.$refs.toggle).popover('dispose');
  },
};
</script>
