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

<!-- eslint-disable vue/no-mutating-props -->
<template>
  <div class="form-group mb-4">
    <div class="form-row" :class="{'drag-extra': extra.isDragging}">
      <!-- Type selection. -->
      <div class="col-xl-2 mb-1 mb-xl-0" :class="{'mr-3 mr-xl-0': nestedType}">
        <select class="custom-select custom-select-sm"
                tabindex="-1"
                v-model="extra.type.value"
                :class="{'has-error': extra.type.errors.length > 0 && !extra.isDragging}"
                :disabled="hasOptions && !extra.editValidation"
                @change="changeType">
          <option value="str">String</option>
          <option value="int">Integer</option>
          <option value="float">Float</option>
          <option value="bool">Boolean</option>
          <option value="date">Date</option>
          <option value="dict">Dictionary</option>
          <option value="list">List</option>
        </select>
        <div v-show="!extra.isDragging">
          <div class="invalid-feedback" v-for="error in extra.type.errors" :key="error">{{ error }}</div>
        </div>
      </div>
      <!-- Key input. -->
      <div class="col-xl-4 mb-1 mb-xl-0" :class="{'mr-3 mr-xl-0': nestedType}">
        <div class="input-group input-group-sm">
          <div class="input-group-prepend sort-handle">
            <span class="input-group-text">{{ $t('Key') }}</span>
          </div>
          <input class="form-control"
                 :value="keyModel"
                 :class="{'has-error': extra.key.errors.length > 0 && !extra.isDragging,
                          'font-weight-bold': isNestedType}"
                 :readonly="nestedType === 'list'"
                 :tabindex="nestedType === 'list' ? -1 : 0"
                 @change="changeString('key', $event.target.value)"
                 ref="key">
        </div>
        <div v-show="!extra.isDragging">
          <div class="invalid-feedback" v-for="error in extra.key.errors" :key="error">{{ error }}</div>
        </div>
      </div>
      <!-- Value input or selection and validation toggle. -->
      <div class="mb-1 mb-xl-0" :class="{'col-xl-3': showUnit, 'col-xl-5': !showUnit, 'mr-3 mr-xl-0': nestedType}">
        <div class="input-group input-group-sm">
          <div class="input-group-prepend sort-handle">
            <span class="input-group-text">
              {{ $t('Value') }} <strong class="text-danger" v-if="isRequired">*</strong>
            </span>
          </div>
          <input class="form-control"
                 :value="valueModel"
                 :class="{'has-error': extra.value.errors.length > 0 && !extra.isDragging}"
                 :readonly="isNestedType"
                 :tabindex="isNestedType ? -1 : 0"
                 v-if="!hasOptions && !['bool', 'date'].includes(extra.type.value)"
                 @change="changeValue($event.target.value)">
          <select class="custom-select"
                  :value="valueModel"
                  :class="{'has-error': extra.value.errors.length > 0 && !extra.isDragging}"
                  v-if="!hasOptions && extra.type.value === 'bool'"
                  @change="changeValue($event.target.value)">
            <option value=""></option>
            <option value="true">{{ $t('true') }}</option>
            <option value="false">{{ $t('false') }}</option>
          </select>
          <select class="custom-select"
                  :value="valueModel"
                  :class="{'has-error': extra.value.errors.length > 0 && !extra.isDragging}"
                  v-if="hasOptions"
                  @change="changeValue($event.target.value)">
            <option value=""></option>
            <option :value="option" :key="i" v-for="(option, i) in extra.validation.value.options">{{ option }}</option>
          </select>
          <input type="hidden" :value="extra.value.value" v-if="extra.type.value === 'date'">
          <date-time-picker :class="{'has-error': extra.value.errors.length > 0 && !extra.isDragging}"
                            :initial-value="extra.value.value"
                            @input="changeValue"
                            v-if="extra.type.value === 'date'">
          </date-time-picker>
          <div class="input-group-append" v-if="!isNestedType && showValidation">
            <button type="button"
                    class="input-group-text btn"
                    :title="$t('Toggle validation')"
                    @click="extra.editValidation = !extra.editValidation">
              <i class="fa-solid fa-angle-up" v-if="extra.editValidation"></i>
              <i class="fa-solid fa-angle-down" v-else></i>
            </button>
          </div>
        </div>
        <div v-show="!extra.isDragging">
          <div class="invalid-feedback" v-for="error in extra.value.errors" :key="error">{{ error }}</div>
        </div>
      </div>
      <!-- Unit input. -->
      <div class="col-xl-2 mb-1 mb-xl-0" :class="{'mr-3 mr-xl-0': nestedType}" v-show="showUnit">
        <div class="input-group input-group-sm">
          <div class="input-group-prepend sort-handle">
            <span class="input-group-text">{{ $t('Unit') }}</span>
          </div>
          <input class="form-control"
                 :value="extra.unit.value"
                 :class="{'has-error': extra.unit.errors.length > 0 && !extra.isDragging}"
                 @change="changeString('unit', $event.target.value)">
        </div>
        <div v-show="!extra.isDragging">
          <div class="invalid-feedback" v-for="error in extra.unit.errors" :key="error">{{ error }}</div>
        </div>
      </div>
      <!-- Remove and/or duplication buttons. -->
      <div class="col-xl-1" :class="{'mr-3 mr-xl-0': nestedType}">
        <div class="d-none d-xl-block pr-2">
          <button type="button"
                  class="btn btn-sm btn-light btn-block"
                  tabindex="-1"
                  :title="toggleDuplicate ? $t('Duplicate') : $t('Remove')"
                  @click="toggleDuplicate ? $emit('duplicate-extra') : $emit('remove-extra')">
            <i class="fa-solid fa-xmark" v-if="!toggleDuplicate"></i>
            <i class="fa-solid fa-copy" v-else></i>
            <span class="d-xl-none pl-1">
              <span v-if="!toggleDuplicate">{{ $t('Remove') }}</span>
              <span v-else>{{ $t('Duplicate') }}</span>
            </span>
          </button>
        </div>
        <div class="btn-group w-100 d-xl-none">
          <button type="button"
                  class="btn btn-sm btn-light"
                  tabindex="-1"
                  :title="$t('Remove')"
                  @click="$emit('remove-extra')">
            <i class="fa-solid fa-xmark pr-1"></i> {{ $t('Remove') }}
          </button>
          <button type="button"
                  class="btn btn-sm btn-light"
                  tabindex="-1"
                  :title="$t('Duplicate')"
                  @click="$emit('duplicate-extra')">
            <i class="fa-solid fa-copy pr-1"></i> {{ $t('Duplicate') }}
          </button>
        </div>
      </div>
    </div>
    <div v-show="!isNestedType && extra.editValidation && !extra.isDragging">
      <extras-editor-item-validation :class="{'has-error': extra.validation.errors.length > 0}"
                                     :type="extra.type.value"
                                     :convert-value="convertValue"
                                     :initial-values="extra.validation.value"
                                     @validate="validate">
      </extras-editor-item-validation>
      <div class="invalid-feedback" v-for="error in extra.validation.errors" :key="error">{{ error }}</div>
    </div>
    <div class="card extra mt-1 pl-3 py-2"
         :class="{'extra-nested': depth % 2 == 0}"
         v-show="!extra.isDragging"
         v-if="isNestedType">
      <extras-editor-items :extras="extra.value.value"
                           :toggle-duplicate="toggleDuplicate"
                           :show-validation="showValidation"
                           :nested-type="extra.type.value"
                           :depth="depth + 1"
                           @save-checkpoint="$emit('save-checkpoint')">
      </extras-editor-items>
    </div>
  </div>
</template>

<style scoped>
.drag-extra {
  background-color: #dee6ed;
  border-radius: 0.5rem;
  padding: 0.5rem 0 0.5rem 0.5rem;
}

.extra {
  margin-right: -1px;
}

.extra-nested {
  background-color: #f2f2f2;
}

.sort-handle {
  cursor: pointer;
}
</style>

<!-- eslint-disable vue/no-mutating-props -->
<script>
export default {
  data() {
    return {
      prevType: null,
    };
  },
  props: {
    extra: Object,
    index: Number,
    toggleDuplicate: Boolean,
    showValidation: Boolean,
    nestedType: String,
    depth: Number,
  },
  computed: {
    keyModel: {
      get() {
        return this.nestedType === 'list' ? `(${this.index + 1})` : this.extra.key.value;
      },
      set(value) {
        this.extra.key.value = value;
      },
    },
    valueModel() {
      return this.isNestedType ? '' : this.extra.value.value;
    },
    showUnit() {
      return ['int', 'float'].includes(this.extra.type.value);
    },
    isNestedType() {
      return kadi.utils.isNestedType(this.extra.type.value);
    },
    isRequired() {
      return this.extra.validation.value && this.extra.validation.value.required;
    },
    hasOptions() {
      return this.extra.validation.value && this.extra.validation.value.options;
    },
  },
  watch: {
    showValidation() {
      if (!this.showValidation) {
        this.extra.editValidation = false;
      }
    },
  },
  methods: {
    convertValue(value) {
      if (value === null) {
        return value;
      }

      let newValue = value;
      if (typeof newValue === 'string') {
        newValue = newValue.trim();
      }

      const type = this.extra.type.value;
      if (type === 'str') {
        newValue = String(newValue);
      } else if (['int', 'float'].includes(type)) {
        if (newValue) {
          if (type === 'int') {
            newValue = Number.parseInt(newValue, 10);
          } else {
            newValue = Number.parseFloat(newValue, 10);
          }

          if (window.isNaN(newValue)) {
            newValue = 0;
          }

          if (type === 'int') {
            if (newValue > Number.MAX_SAFE_INTEGER) {
              newValue = Number.MAX_SAFE_INTEGER;
            } else if (newValue < -Number.MAX_SAFE_INTEGER) {
              newValue = -Number.MAX_SAFE_INTEGER;
            }
          } else if (!window.isFinite(newValue)) {
            newValue = Number.MAX_VALUE;
          }
        }
      } else if (type === 'bool') {
        if (newValue === 'true') {
          newValue = true;
        } else if (newValue === 'false') {
          newValue = false;
        }
      }

      if (newValue === '') {
        newValue = null;
      }

      return newValue;
    },
    changeType() {
      this.extra.value.value = this.convertValue(this.extra.value.value);

      const specialInputTypes = ['bool', 'date'];
      if ((!this.isNestedType && kadi.utils.isNestedType(this.prevType))
          || specialInputTypes.includes(this.extra.type.value)
          || specialInputTypes.includes(this.prevType)) {
        this.extra.value.value = null;
      }

      if (this.isNestedType && !kadi.utils.isNestedType(this.prevType)) {
        this.$emit('init-nested-value');
      }

      this.prevType = this.extra.type.value;
      // No need to create a checkpoint here, since changing a type also triggers the "validate" function, which will
      // create the checkpoint only after possible changes in the validation based on the type have occured as well.
    },
    changeString(prop, value) {
      const oldValue = this.extra[prop].value;
      // Set the value to the given value as is first, as otherwise the view is not updated correctly if the converted
      // value ('newValue') is the same as before.
      this.extra[prop].value = value;

      let newValue = value.trim();
      if (newValue === '') {
        newValue = null;
      }
      this.extra[prop].value = newValue;

      if (oldValue !== newValue) {
        this.$emit('save-checkpoint');
      }
    },
    changeValue(value) {
      const oldValue = this.extra.value.value;
      // See comment in 'changeString'.
      this.extra.value.value = value;

      const newValue = this.convertValue(value);
      this.extra.value.value = newValue;

      if (oldValue !== newValue) {
        this.$emit('save-checkpoint');
      }
    },
    validate(validation) {
      this.extra.validation.value = validation;

      // Reset the value if it is not in any of the options.
      if (validation && validation.options && !validation.options.includes(this.extra.value.value)) {
        this.extra.value.value = null;
      }

      this.$emit('save-checkpoint');
    },
    keydownHandler(e) {
      if (e.ctrlKey && e.key === 'd') {
        e.preventDefault();
        e.stopPropagation();
        if (this.showValidation) {
          this.extra.editValidation = !this.extra.editValidation;
        }
      }
    },
  },
  mounted() {
    this.extra.input = this.$refs.key;
    this.prevType = this.extra.type.value;

    if (this.extra.validation.errors.length > 0) {
      this.extra.editValidation = true;
    }

    this.$el.addEventListener('keydown', this.keydownHandler);
  },
  beforeDestroy() {
    this.$el.removeEventListener('keydown', this.keydownHandler);
  },
};
</script>
