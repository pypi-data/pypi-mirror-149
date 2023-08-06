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

import {sockets, commonInputs, commonOutputs, BuiltinComponent} from 'core';
import PortControl from 'scripts/lib/workflows/controls/port-control';

const type = 'control';
const menu = 'Control';

const variable = new BuiltinComponent(
  'Variable',
  type,
  menu,
  [
    commonInputs.dep,
    {key: 'name', title: 'Name', socket: sockets.str},
    {key: 'value', title: 'Value', socket: sockets.str},
  ],
  [commonOutputs.dep],
);

const ifBranch = new BuiltinComponent(
  'IfBranch',
  type,
  menu,
  [
    commonInputs.dep,
    {key: 'condition', title: 'Condition', socket: sockets.bool},
  ],
  [
    commonOutputs.dep,
    {key: 'true', title: 'True', socket: sockets.dep, multi: true},
    {key: 'false', title: 'False', socket: sockets.dep, multi: true},
  ],
);

const loop = new BuiltinComponent(
  'Loop',
  type,
  menu,
  [
    commonInputs.dep,
    {key: 'condition', title: 'Condition', socket: sockets.bool},
    {key: 'startIndex', title: 'Start Index [0]', socket: sockets.int},
    {key: 'endIndex', title: 'End Index', socket: sockets.int},
    {key: 'step', title: 'Step [1]', socket: sockets.int},
    {key: 'indexVarName', title: 'Index Variable Name', socket: sockets.str},
  ],
  [
    commonOutputs.dep,
    {key: 'loop', title: 'Loop', socket: sockets.dep, multi: true},
    {key: 'index', title: 'Index', socket: sockets.int, multi: true},
  ],
);

/** Branch component that supports dynamically removing/adding branch outputs. */
class BranchComponent extends BuiltinComponent {
  constructor() {
    super(
      'BranchSelect',
      type,
      menu,
      [commonInputs.dep, {key: 'selected', title: 'Selected', socket: sockets.int}],
      [commonOutputs.dep],
    );
  }

  builder(node) {
    super.builder(node);

    node.meta.prevBranches = 0;
    node.addControl(new PortControl('branches', 'Branches'));

    this.editor.on('controlchanged', (control) => {
      if (control.parent !== node) {
        return;
      }

      const branches = node.data.branches;

      if (branches > node.meta.prevBranches) {
        for (let i = node.meta.prevBranches; i < branches; i++) {
          node.addOutput(new Rete.Output(`branch${i}`, `Branch ${i + 1}`, sockets.dep, true));
        }
      } else {
        for (let i = branches; i < node.meta.prevBranches; i++) {
          const output = node.outputs.get(`branch${i}`);
          // Reverse loop since we are removing the connections as we loop.
          for (let j = output.connections.length - 1; j >= 0; j--) {
            this.editor.removeConnection(output.connections[j]);
          }
          node.removeOutput(output);
        }
      }

      node.vueContext.$forceUpdate();
      node.meta.prevBranches = branches;
    });
  }

  fromFlow(flowNode) {
    const node = super.fromFlow(flowNode);

    node.data.branches = flowNode.model.nBranches;
    for (let i = 0; i < node.data.branches; i++) {
      node.outputs.set(`branch${i}`, {connections: []});
    }

    return node;
  }

  toFlow(node) {
    const flowNode = super.toFlow(node);
    flowNode.model.nBranches = node.data.branches;
    return flowNode;
  }
}

export default [variable, ifBranch, loop, new BranchComponent()];
