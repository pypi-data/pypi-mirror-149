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

import {sockets, commonInputs, commonOutputs, BuiltinComponent} from 'core';
import ShortcutControl from 'scripts/lib/workflows/controls/shortcut-control';

const type = 'io';
const menu = 'File I/O';

const fileInput = new BuiltinComponent(
  'FileInput',
  type,
  menu,
  [commonInputs.dep, {key: 'path', title: 'File Path', socket: sockets.str}],
  [commonOutputs.dep, commonOutputs.pipe],
);

/** File output component that contains an additional shortcut control. */
class FileOutputComponent extends BuiltinComponent {
  constructor() {
    super(
      'FileOutput',
      type,
      menu,
      [
        commonInputs.dep,
        {key: 'path', title: 'File Path', socket: sockets.str},
        {key: 'append', title: 'Append', socket: sockets.bool},
        commonInputs.pipe,
      ],
      [commonOutputs.dep],
    );
  }

  builder(node) {
    super.builder(node);
    node.addControl(new ShortcutControl('shortcut'));
  }

  fromFlow(flowNode) {
    const node = super.fromFlow(flowNode);
    node.data.shortcut = flowNode.model.createShortcut;
    return node;
  }

  toFlow(node) {
    const flowNode = super.toFlow(node);
    flowNode.model.createShortcut = node.data.shortcut;
    return flowNode;
  }
}

export default [fileInput, new FileOutputComponent()];
