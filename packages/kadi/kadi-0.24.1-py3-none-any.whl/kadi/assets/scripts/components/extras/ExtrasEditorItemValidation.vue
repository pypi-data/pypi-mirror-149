<!-- Copyright 2021 Karlsruhe Institute of Technology
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
  <div class="card mt-1 mr-2">
    <div class="form-row align-items-center my-2 mx-1">
      <div class="col-sm-2 text-muted mb-2 mb-sm-0">{{ $t('Required') }}</div>
      <div class="col-sm-10">
        <input type="checkbox" class="align-middle" v-model="required">
      </div>
    </div>
    <div v-if="['str', 'int', 'float'].includes(type)">
      <div class="form-row align-items-center my-2 mx-1">
        <div class="col-sm-2 text-muted mb-2 mb-sm-0">{{ $t('Options') }}</div>
        <div class="col-sm-10">
          <div class="form-row"
               :class="{'mb-2': index < options.length - 1}"
               :key="option.id"
               v-for="(option, index) in options">
            <div class="col-sm-10 mb-1 mb-sm-0">
              <input class="form-control form-control-sm"
                     :value="option.value"
                     @change="changeOption(option, $event.target.value)">
            </div>
            <div class="col-sm-2 btn-group btn-group-sm">
              <button type="button" class="btn btn-light" @click="addOption(null, index)">
                <i class="fa-solid fa-plus"></i>
              </button>
              <button type="button" class="btn btn-light" @click="removeOption(index)" v-if="options.length > 1">
                <i class="fa-solid fa-xmark"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      initialized: false,
      required: false,
      options: [],
    };
  },
  props: {
    type: String,
    convertValue: Function,
    initialValues: {
      type: Object,
      default: () => ({}),
    },
  },
  watch: {
    type() {
      for (const option of this.options) {
        this.changeOption(option, option.value, false);
      }
      this.updateValidation();
    },
    required() {
      this.updateValidation();
    },
  },
  methods: {
    updateValidation() {
      if (!this.initialized) {
        return;
      }

      if (kadi.utils.isNestedType(this.type)) {
        this.$emit('validate', null);
        return;
      }

      const validation = {};

      // Omit the required property if it is false.
      if (this.required) {
        validation.required = true;
      }

      if (['str', 'int', 'float'].includes(this.type)) {
        validation.options = [];

        for (const option of this.options) {
          if (option.value !== null) {
            validation.options.push(option.value);
          }
        }

        // Omit the options property if it is empty.
        if (validation.options.length === 0) {
          delete validation.options;
        }
      }

      // Emit null if the validation object is empty.
      this.$emit('validate', Object.keys(validation).length === 0 ? null : validation);
    },
    addOption(option = null, index = null) {
      const newOption = {
        id: kadi.utils.randomAlnum(),
        value: this.convertValue(option),
      };

      if (index !== null) {
        this.options.splice(index + 1, 0, newOption);
      } else {
        this.options.push(newOption);
      }
    },
    removeOption(index) {
      const option = this.options.splice(index, 1)[0];
      if (option.value !== null) {
        this.updateValidation();
      }
    },
    changeOption(option, value, updateValidation = true) {
      const oldValue = option.value;
      option.value = value;

      const newValue = this.convertValue(value);
      option.value = newValue;

      if (updateValidation && oldValue !== newValue) {
        this.updateValidation();
      }
    },
  },
  mounted() {
    this.addOption();

    // This initialization is enough, since the whole component is re-rendered anyways when e.g. using the undo/redo
    // functionality.
    if (this.initialValues) {
      this.required = this.initialValues.required || false;

      if (this.initialValues.options) {
        this.removeOption(0);
        for (const option of this.initialValues.options) {
          this.addOption(option);
        }
      }
    }

    // Skip first potential change.
    this.$nextTick(() => this.initialized = true);
  },
};
</script>
