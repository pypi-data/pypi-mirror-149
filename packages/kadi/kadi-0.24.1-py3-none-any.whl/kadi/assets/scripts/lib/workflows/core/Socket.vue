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
  <div class="socket"
       :class="[type, socket.name, used ? 'used' : '', compatible ? '' : 'incompatible']"
       @mouseenter.stop="mouseenter"
       @mouseleave.stop="mouseleave">
    <div v-if="multi">+</div>
  </div>
</template>

<style lang="scss" scoped>
@import 'styles/workflows/workflow-editor.scss';

$bg-bool: #fa5a5a;
$bg-dep: #72de6d;
$bg-env: #636363;
$bg-float: #77dfed;
$bg-int: #c660fc;
$bg-pipe: #ebe836;
$bg-str: #6b9fff;

.socket {
  align-items: center;
  background: white;
  border: 2px solid lighten($connection-color, 15%);
  border-radius: $socket-size * 0.5;
  box-sizing: border-box;
  cursor: pointer;
  display: inline-flex;
  height: $socket-size;
  justify-content: center;
  margin: $socket-margin;
  position: relative;
  vertical-align: middle;
  width: $socket-size;
  z-index: 2;

  &.incompatible {
    opacity: 0.2;
    transition: opacity 0.25s;
  }

  &.input {
    margin-left: -$socket-size * 0.5;
  }

  &.output {
    margin-right: -$socket-size * 0.5;
  }

  &.used {
    border: 2px solid $connection-color;
  }

  &:hover {
    border-width: 4px;
    border: 2px solid darken($connection-color, 25%);
  }

  &:not(.incompatible) {
    opacity: 1;
    transition: opacity 0.5s;
  }

  /* Socket types. */

  &.bool {
    background: $bg-bool;
    color: darken($bg-bool, 25%);
  }

  &.dep {
    background: $bg-dep;
    color: darken($bg-dep, 25%);
  }

  &.env {
    background: $bg-env;
    color: darken($bg-env, 25%);
  }

  &.float {
    background: $bg-float;
    color: darken($bg-float, 25%);
  }

  &.int {
    background: $bg-int;
    color: darken($bg-int, 25%);
  }

  &.pipe {
    background: $bg-pipe;
    color: darken($bg-pipe, 25%);
  }

  &.str {
    background: $bg-str;
    color: darken($bg-str, 25%);
  }
}
</style>

<script>
import VueRenderPlugin from 'rete-vue-render-plugin';

export default {
  extends: VueRenderPlugin.Socket,
  data() {
    return {
      id: kadi.utils.randomAlnum(),
      compatible: true,
    };
  },
  props: {
    editor: Object,
    used: Boolean,
    multi: Boolean,
  },
  methods: {
    mouseenter() {
      this.editor.trigger('socketenter', {id: this.id, socket: this.socket, type: this.type});
    },
    mouseleave() {
      this.editor.trigger('socketleave');
    },
  },
  mounted() {
    this.editor.on('socketenter', ({id, socket, type}) => {
      if (this.id === id) {
        this.compatible = true;
      } else if (this.type === type) {
        this.compatible = false;
      } else if (this.type === 'input') {
        this.compatible = socket.compatibleWith(this.socket);
      } else {
        this.compatible = this.socket.compatibleWith(socket);
      }
    });
    this.editor.on('socketleave', () => this.compatible = true);
  },
};
</script>
