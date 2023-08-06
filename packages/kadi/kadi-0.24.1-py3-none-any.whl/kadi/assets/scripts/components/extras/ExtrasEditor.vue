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
  <div class="mb-4" tabindex="-1" ref="editor">
    <div class="row mb-2">
      <div class="col-xl-3">
        <collapse-item class="text-default" :id="id">{{ label }}</collapse-item>
      </div>
      <div class="col-xl-9 d-xl-flex justify-content-end">
        <div class="btn-toolbar btn-group-sm">
          <button type="button"
                  class="btn btn-link text-primary"
                  tabindex="-1"
                  :title="`${$t('Undo')} (${$t('Ctrl')}+Z)`"
                  :disabled="!undoable"
                  @click="undo">
            <i class="fa-solid fa-rotate-left"></i> {{ $t('Undo') }}
          </button>
          <button type="button"
                  class="btn btn-link text-primary"
                  tabindex="-1"
                  :title="`${$t('Redo')} (${$t('Ctrl')}+Y)`"
                  :disabled="!redoable"
                  @click="redo">
            <i class="fa-solid fa-rotate-right"></i> {{ $t('Redo') }}
          </button>
          <button type="button"
                  class="btn btn-link text-primary d-none d-xl-block"
                  tabindex="-1"
                  :title="toggleDuplicateTitle"
                  @click="toggleDuplicate = !toggleDuplicate">
            <span v-if="toggleDuplicate">
              <i class="fa-solid fa-xmark"></i> {{ $t('Remove') }}
            </span>
            <span v-else>
              <i class="fa-solid fa-copy"></i> {{ $t('Duplicate') }}
            </span>
          </button>
          <button type="button"
                  class="btn btn-link text-primary"
                  tabindex="-1"
                  :title="$t('Reset editor')"
                  @click="resetEditor">
            <i class="fa-solid fa-rotate"></i> {{ $t('Reset') }}
          </button>
          <button type="button"
                  class="btn btn-link text-primary"
                  tabindex="-1"
                  :title="`${$t('Toggle view')} (${$t('Ctrl')}+E)`"
                  @click="showTree = !showTree">
            <span v-if="showTree">
              <i class="fa-solid fa-pencil"></i> {{ $t('Editor view') }}
            </span>
            <span v-else>
              <i class="fa-solid fa-bars-staggered"></i> {{ $t('Tree view') }}
            </span>
          </button>
          <button type="button"
                  class="btn btn-link"
                  tabindex="-1"
                  :class="{'text-primary': showValidation, 'text-muted': !showValidation}"
                  :title="showValidation ? $t('Hide validation') : $t('Show validation')"
                  @click="showValidation = !showValidation"
                  v-if="!isTemplate">
            <span>
              <i class="fa-solid fa-check"></i> {{ $t('Validation') }}
            </span>
          </button>
        </div>
        <popover-toggle toggle-class="btn btn-sm btn-link text-muted">
          <template #toggle>
            <i class="fa-solid fa-circle-question"></i> {{ $t('Help') }}
          </template>
          <template #content>
            <p>
              {{ $t("An entry's position can be changed by dragging the label of any input (e.g. the 'Key' label).") }}
              {{ $t('Additionally, the following keyboard shortcuts are supported:') }}
            </p>
            <dl class="row mb-0">
              <dt class="col-3"><strong>{{ $t('Ctrl') }}+Z</strong></dt>
              <dd class="col-9">{{ $t('Undo the last step (up to 10 steps are recorded).') }}</dd>
              <dt class="col-3"><strong>{{ $t('Ctrl') }}+Y</strong></dt>
              <dd class="col-9">{{ $t('Redo the previous step (up to 10 steps are recorded).') }}</dd>
              <dt class="col-3"><strong>{{ $t('Ctrl') }}+B</strong></dt>
              <dd class="col-9">{{ $t('Toggle the duplicate/remove button.') }}</dd>
              <dt class="col-3"><strong>{{ $t('Ctrl') }}+E</strong></dt>
              <dd class="col-9">{{ $t('Toggle the tree/editor view.') }}</dd>
              <dt class="col-3"><strong>{{ $t('Ctrl') }}+D</strong></dt>
              <dd class="col-9">{{ $t('Toggle the validation menu of the current entry.') }}</dd>
              <dt class="col-3"><strong>{{ $t('Ctrl') }}+I</strong></dt>
              <dd class="col-9">{{ $t('Add a new entry in the same layer as the current entry.') }}</dd>
            </dl>
          </template>
        </popover-toggle>
      </div>
    </div>
    <div :id="id" class="collapse show">
      <div v-show="!showTree">
        <extras-editor-items :extras="extras"
                             :toggle-duplicate="toggleDuplicate"
                             :show-validation="showValidation"
                             @save-checkpoint="saveCheckpoint"
                             ref="extras">
          <div class="form-row align-items-center" v-if="templateEndpoint">
            <div class="offset-xl-7 col-xl-5 mt-2 mt-xl-0">
              <dynamic-selection container-classes="select2-single-sm"
                                 :placeholder="$t('Select a metadata template')"
                                 :endpoint="templateEndpoint"
                                 :reset-on-select="true"
                                 @select="loadTemplate">
              </dynamic-selection>
            </div>
          </div>
        </extras-editor-items>
      </div>
      <div class="card" v-show="showTree">
        <div class="card-body text-break py-3 px-3">
          <extras-editor-tree-view :extras="extras" @focus-extra="focusExtra"></extras-editor-tree-view>
        </div>
      </div>
    </div>
    <input type="hidden" :name="name" :value="serializedExtras">
  </div>
</template>

<script>
import undoRedoMixin from 'scripts/lib/components/mixins/undo-redo-mixin';

export default {
  mixins: [undoRedoMixin],
  data() {
    return {
      extras: [],
      toggleDuplicate: false,
      showTree: false,
      showValidation: false,
      numInitialFields: 3,
    };
  },
  props: {
    id: {
      type: String,
      default: 'extras-editor',
    },
    name: {
      type: String,
      default: 'extras-editor',
    },
    label: {
      type: String,
      default: 'Extra metadata',
    },
    initialValues: {
      type: Array,
      default: () => [],
    },
    editExtraKeys: {
      type: Array,
      default: () => [],
    },
    templateEndpoint: {
      type: String,
      default: null,
    },
    isTemplate: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    serializedExtras() {
      return JSON.stringify(this.serializeExtras(this.extras));
    },
    toggleDuplicateTitle() {
      const shortcut = `(${$t('Ctrl')}+B)`;
      const text = this.toggleDuplicate ? $t('Show remove button') : $t('Show duplicate button');
      return `${text} ${shortcut}`;
    },
  },
  methods: {
    serializeExtras(extras, nestedType = null) {
      const newExtras = [];

      for (const extra of extras) {
        if (this.extraIsEmpty(extra, nestedType)) {
          continue;
        }

        const newExtra = {
          type: extra.type.value,
          value: extra.value.value,
        };

        if (nestedType !== 'list') {
          newExtra.key = extra.key.value;
        }
        if (['int', 'float'].includes(newExtra.type)) {
          newExtra.unit = extra.unit.value;
        }
        if (extra.validation.value) {
          newExtra.validation = extra.validation.value;
        }

        if (kadi.utils.isNestedType(newExtra.type)) {
          newExtra.value = this.serializeExtras(newExtra.value, newExtra.type);
        }

        newExtras.push(newExtra);
      }

      return newExtras;
    },
    extraIsEmpty(extra, nestedType = null) {
      if (extra.key.value === null
          && extra.value.value === null
          && extra.unit.value === null
          && extra.validation.value === null
          && nestedType !== 'list') {
        return true;
      }
      return false;
    },
    initializeFields() {
      for (let i = 0; i < this.numInitialFields; i++) {
        this.$refs.extras.addExtra(null, false);
      }
    },
    resetEditor() {
      const reset = () => {
        this.$refs.extras.removeExtras(false);
        this.initializeFields();
        this.saveCheckpoint();
      };

      // Only reset the editor if it is not in initial state already.
      if (this.extras.length === this.numInitialFields) {
        for (const extra of this.extras) {
          if (!this.extraIsEmpty(extra)) {
            reset();
            return;
          }
        }
      } else {
        reset();
      }
    },
    loadTemplate(data) {
      axios.get(data.endpoint)
        .then((response) => {
          this.extras.slice().forEach((extra) => {
            // Remove empty extras on the first level.
            if (this.extraIsEmpty(extra)) {
              this.$refs.extras.removeExtra(extra, false);
            }
          });

          this.$refs.extras.addExtras(response.data.data);
        })
        .catch((error) => kadi.alert($t('Error loading template.'), {request: error.request}));
    },
    focusExtra(extra) {
      this.showTree = false;
      this.$nextTick(() => this.$refs.extras.focusExtra(extra));
    },
    keydownHandler(e) {
      if (e.ctrlKey) {
        switch (e.key) {
        case 'z':
          e.preventDefault();
          // Aside from keeping focus, this also forces a change event in case the shortcut is pressed while an input
          // field is still being edited. This in turn triggers the checkpoint creation before the undo function is
          // actually called.
          this.$refs.editor.focus();
          this.undo();
          break;
        case 'y':
          e.preventDefault();
          this.$refs.editor.focus();
          this.redo();
          break;
        case 'b':
          e.preventDefault();
          this.toggleDuplicate = !this.toggleDuplicate;
          break;
        case 'e':
          e.preventDefault();
          this.showTree = !this.showTree;
          this.$refs.editor.focus();
          break;
        default: // Do nothing.
        }
      }
    },
    getCheckpointData(triggerChange = true) {
      if (triggerChange) {
        // Dispatch a native change event every time a checkpoint is created, unless expliticely specified not to.
        this.$el.dispatchEvent(new Event('change', {bubbles: true}));
      }

      const checkpointData = [];
      // Save a deep copy of the extra metadata.
      this.extras.forEach((extra) => checkpointData.push(this.$refs.extras.newExtra(extra)));
      return checkpointData;
    },
    restoreCheckpointData(data) {
      this.$refs.extras.removeExtras(false);
      this.$refs.extras.addExtras(data, false);
    },
  },
  mounted() {
    if (this.initialValues.length > 0) {
      this.$refs.extras.addExtras(this.initialValues, false);
    } else {
      this.initializeFields();
    }
    this.saveCheckpoint(false);

    if (this.isTemplate) {
      this.showValidation = true;
    }

    if (this.editExtraKeys.length > 0) {
      let extra = null;
      let previousType = null;
      let currentExtras = this.extras;

      for (const key of this.editExtraKeys) {
        // Try to use the key as an index instead for list values.
        if (previousType === 'list') {
          const index = Number.parseInt(key, 10);
          if (isNaN(index) || index >= currentExtras.length) {
            break;
          }
          extra = currentExtras[index];
        } else {
          const result = currentExtras.find((extra) => extra.key.value === key);
          if (!result) {
            break;
          }
          extra = result;
        }

        previousType = extra.type.value;
        currentExtras = extra.value.value;

        // In case we can't continue with any nested values, just break out of the loop, even if not all keys were
        // processed yet.
        if (!Array.isArray(currentExtras)) {
          break;
        }
      }

      if (extra) {
        this.$nextTick(() => this.$refs.extras.focusExtra(extra));
      }
    }

    this.$el.addEventListener('keydown', this.keydownHandler);
  },
  beforeDestroy() {
    this.$el.removeEventListener('keydown', this.keydownHandler);
  },
};
</script>
