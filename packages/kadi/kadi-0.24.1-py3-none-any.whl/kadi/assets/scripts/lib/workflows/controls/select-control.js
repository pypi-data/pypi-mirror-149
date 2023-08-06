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

import {BaseControl} from 'core';
import VueSelectControl from 'SelectControl.vue';

function getControl(connection) {
  // Source nodes should have only one control.
  return connection.output.node.controls.values().next().value;
}

/** Custom control for predefined values using a dynamically populated select input. */
export default class SelectControl extends BaseControl {
  constructor(key) {
    super(key, VueSelectControl, null);
    this.events = {
      connectioncreated: this.connectioncreated.bind(this),
      connectionremoved: this.connectionremoved.bind(this),
    };
  }

  connectioncreated(connection) {
    const control = getControl(connection);
    if (this === control) {
      const choices = connection.input.node.inputs.get(connection.input.key).param.choices;
      this.vueContext.setChoices(choices);
    }
  }

  connectionremoved(connection) {
    const control = getControl(connection);
    if (this === control) {
      this.vueContext.resetChoices();
    }
  }
}
