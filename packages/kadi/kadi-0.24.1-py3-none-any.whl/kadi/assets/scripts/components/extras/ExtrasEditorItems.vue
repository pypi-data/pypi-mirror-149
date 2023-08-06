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
    <div :class="{'mt-2': nestedType && extras.length > 0}">
      <vue-draggable :list="extras"
                     :group="{name: 'extras'}"
                     :force-fallback="true"
                     :empty-insert-threshold="35"
                     scroll-sensitivity="100"
                     scroll-speed="15"
                     handle=".sort-handle"
                     @start="startDrag"
                     @end="endDrag">
        <div v-for="(extra, index) in extras" :key="extra.id">
          <extras-editor-item :extra="extra"
                              :index="index"
                              :toggle-duplicate="toggleDuplicate"
                              :show-validation="showValidation"
                              :nested-type="nestedType"
                              :depth="depth"
                              @remove-extra="removeExtra(extra)"
                              @duplicate-extra="duplicateExtra(extra)"
                              @init-nested-value="initNestedValue(extra)"
                              @save-checkpoint="$emit('save-checkpoint')">
          </extras-editor-item>
        </div>
      </vue-draggable>
    </div>
    <div class="row align-items-center">
      <div class="col-xl-3">
        <button type="button"
                class="btn btn-link text-muted p-0"
                tabindex="-1"
                :title="`${$t('Add entry')} (${$t('Ctrl')}+I)`"
                @click="addExtra(null)">
          <i class="fa-solid fa-plus mr-1"></i> {{ $t('Add entry') }}
        </button>
      </div>
      <div class="col-xl-9">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<!-- eslint-disable vue/no-mutating-props -->
<script>
import VueDraggable from 'vuedraggable';

export default {
  components: {
    VueDraggable,
  },
  props: {
    extras: Array,
    toggleDuplicate: Boolean,
    showValidation: Boolean,
    nestedType: {
      type: String,
      default: null,
    },
    depth: {
      type: Number,
      default: 0,
    },
  },
  methods: {
    newExtra(extraToCopy = null, copyErrors = true) {
      const extra = {
        // To prevent issues when reordering extras, using undo/redo, etc.
        id: kadi.utils.randomAlnum(),
        isDragging: false,
        editValidation: false,
        type: {value: 'str', errors: []},
        key: {value: null, errors: []},
        value: {value: null, errors: []},
        unit: {value: null, errors: []},
        validation: {value: null, errors: []},
      };

      // Always perform a deep copy if an extra is to be copied.
      if (extraToCopy) {
        extra.editValidation = extraToCopy.editValidation || false;

        // Assume the extra is formatted as formdata if the type (which should always exist) is an object.
        const isFormdata = typeof extraToCopy.type === 'object';

        // Copy all properties completely except for the value, since it might be nested.
        for (const prop of ['type', 'key', 'value', 'unit', 'validation']) {
          if (extraToCopy[prop]) {
            if (prop !== 'value') {
              const value = isFormdata ? extraToCopy[prop].value : extraToCopy[prop];
              extra[prop].value = JSON.parse(JSON.stringify(value));
            }

            if (isFormdata && copyErrors) {
              extra[prop].errors = extraToCopy[prop].errors.slice();
            }
          }
        }

        // Copy the value (recursively, in case it is nested).
        const value = isFormdata ? extraToCopy.value.value : extraToCopy.value;

        if (kadi.utils.isNestedType(extra.type.value)) {
          extra.value.value = [];
          value.forEach((nestedExtra) => extra.value.value.push(this.newExtra(nestedExtra, copyErrors)));
        } else {
          extra.value.value = value;
        }
      }

      return extra;
    },
    addExtra(extra, createCheckpoint = true) {
      const newExtra = this.newExtra(extra);
      this.extras.push(newExtra);
      if (createCheckpoint) {
        this.$emit('save-checkpoint');
      }
      return newExtra;
    },
    addExtras(extras, createCheckpoint = true) {
      extras.forEach((extra) => this.addExtra(extra, false));
      if (createCheckpoint) {
        this.$emit('save-checkpoint');
      }
    },
    removeExtra(extra, createCheckpoint = true) {
      kadi.utils.removeFromList(this.extras, extra);
      if (createCheckpoint) {
        this.$emit('save-checkpoint');
      }
    },
    removeExtras(createCheckpoint = true) {
      this.extras.length = 0;
      if (createCheckpoint) {
        this.$emit('save-checkpoint');
      }
    },
    duplicateExtra(extra) {
      const index = this.extras.indexOf(extra);
      const copy = this.newExtra(extra, false);
      this.extras.splice(index + 1, 0, copy);
      this.$emit('save-checkpoint');
    },
    focusExtra(extra) {
      extra.input.focus();
      kadi.utils.scrollIntoView(extra.input);
    },
    initNestedValue(extra) {
      extra.value.value = [this.newExtra()];
    },
    keydownHandler(e) {
      if (e.ctrlKey && e.key === 'i') {
        e.preventDefault();
        e.stopPropagation();
        const newExtra = this.addExtra(null);
        this.$nextTick(() => this.focusExtra(newExtra));
      }
    },
    startDrag(e) {
      const extra = e.item._underlying_vm_;
      extra.isDragging = true;
    },
    endDrag(e) {
      const extra = e.item._underlying_vm_;
      extra.isDragging = false;

      if (e.from !== e.to || e.oldIndex !== e.newIndex) {
        this.$emit('save-checkpoint');
      }
    },
  },
  mounted() {
    this.$el.addEventListener('keydown', this.keydownHandler);
  },
  beforeDestroy() {
    this.$el.removeEventListener('keydown', this.keydownHandler);
  },
};
</script>
