/* Copyright 2021 Karlsruhe Institute of Technology
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License. */

import Rete from 'rete';

/** Base class for all custom controls. */
export class BaseControl extends Rete.Control {
  constructor(key, component, defaultValue) {
    super(key);
    this.component = component;
    this.props = {ikey: key, defaultValue};
    this.events = {};
  }
}

/** Mixin to add common basic functionality to custom control Vue components. */
export const InputControlMixin = {
  props: {
    getData: Function,
    putData: Function,
    ikey: String,
  },
  data() {
    return {
      value: null,
    };
  },
  watch: {
    value() {
      this.validateValue();
      if (this.ikey) {
        this.putData(this.ikey, this.value);
      }
      this.$emit('change-value');
    },
  },
  methods: {
    validateValue() {
      // Can be overridden for custom validation logic.
    },
  },
  /* eslint-disable no-undefined */
  mounted() {
    this.value = this.getData(this.ikey);
    if (this.value === undefined) {
      if (this.defaultValue !== undefined) {
        this.value = this.defaultValue;
      } else {
        this.value = null;
      }
    }
    this.putData(this.ikey, this.value);
  },
  /* eslint-enable no-undefined */
};
