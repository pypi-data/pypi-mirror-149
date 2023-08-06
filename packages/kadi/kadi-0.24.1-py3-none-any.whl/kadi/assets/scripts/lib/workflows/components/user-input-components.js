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

import {sockets, commonInputs as commonCoreInputs, commonOutputs, BuiltinComponent} from 'core';
import PortControl from 'scripts/lib/workflows/controls/port-control';

const type = 'user-input';
const menu = 'User Input';

const commonInputs = [commonCoreInputs.dep, {key: 'prompt', title: 'Prompt', socket: sockets.str}];
const commonDefaultValues = {key: 'default', title: 'Default'};
const commonOutputValues = {key: 'value', title: 'Value', multi: true};

const userInputText = new BuiltinComponent(
  'UserInputText',
  type,
  menu,
  [...commonInputs, {...commonDefaultValues, socket: sockets.str}],
  [commonOutputs.dep, {...commonOutputValues, socket: sockets.str}],
);

const userInputInteger = new BuiltinComponent(
  'UserInputInteger',
  type,
  menu,
  [...commonInputs, {...commonDefaultValues, socket: sockets.int}],
  [commonOutputs.dep, {...commonOutputValues, socket: sockets.int}],
);

const userInputFloat = new BuiltinComponent(
  'UserInputFloat',
  type,
  menu,
  [...commonInputs, {...commonDefaultValues, socket: sockets.float}],
  [commonOutputs.dep, {...commonOutputValues, socket: sockets.float}],
);

const userInputBool = new BuiltinComponent(
  'UserInputBool',
  type,
  menu,
  [...commonInputs, {...commonDefaultValues, socket: sockets.bool}],
  [commonOutputs.dep, {...commonOutputValues, socket: sockets.bool}],
);

const userInputFile = new BuiltinComponent(
  'UserInputFile',
  type,
  menu,
  [...commonInputs, {...commonDefaultValues, socket: sockets.str}],
  [commonOutputs.dep, {...commonOutputValues, socket: sockets.str}],
);

const userInputCropImages = new BuiltinComponent(
  'UserInputCropImages',
  type,
  menu,
  [...commonInputs, {key: 'imagePath', title: 'Image Path', socket: sockets.str}],
  [commonOutputs.dep, {key: 'cropInfo', title: 'Crop Info', socket: sockets.str, multi: true}],
);

const userInputPeriodicTable = new BuiltinComponent(
  'UserInputPeriodicTable',
  type,
  menu,
  [...commonInputs, {...commonDefaultValues, socket: sockets.str}],
  [commonOutputs.dep, {key: 'selectedElements', title: 'Selected elements', socket: sockets.str, multi: true}],
);

/** Choose component that supports dynamically removing/adding option inputs. */
class ChooseComponent extends BuiltinComponent {
  constructor() {
    super(
      'UserInputChoose',
      type,
      menu,
      [...commonInputs, {...commonDefaultValues, socket: sockets.int}],
      [commonOutputs.dep, {key: 'selected', title: 'Selected', socket: sockets.int, multi: true}],
    );
  }

  builder(node) {
    super.builder(node);

    node.meta.prevOptions = 0;
    node.addControl(new PortControl('options', 'Options'));

    this.editor.on('controlchanged', (control) => {
      if (control.parent !== node) {
        return;
      }

      const options = node.data.options;

      if (options > node.meta.prevOptions) {
        for (let i = node.meta.prevOptions; i < options; i++) {
          node.addInput(new Rete.Input(`option${i}`, `Option ${i + 1}`, sockets.str));
        }
      } else {
        for (let i = options; i < node.meta.prevOptions; i++) {
          const input = node.inputs.get(`option${i}`);
          // Reverse loop since we are removing the connections as we loop.
          for (let j = input.connections.length - 1; j >= 0; j--) {
            this.editor.removeConnection(input.connections[j]);
          }
          node.removeInput(input);
        }
      }

      node.vueContext.$forceUpdate();
      node.meta.prevOptions = options;
    });
  }

  fromFlow(flowNode) {
    const node = super.fromFlow(flowNode);

    node.data.options = flowNode.model.nOptions;
    for (let i = 0; i < node.data.options; i++) {
      node.inputs.set(`option${i}`, {connections: []});
    }

    return node;
  }

  toFlow(node) {
    const flowNode = super.toFlow(node);
    flowNode.model.nOptions = node.data.options;
    return flowNode;
  }
}

export default [
  userInputText,
  userInputInteger,
  userInputFloat,
  userInputBool,
  userInputFile,
  userInputCropImages,
  userInputPeriodicTable,
  new ChooseComponent(),
];
