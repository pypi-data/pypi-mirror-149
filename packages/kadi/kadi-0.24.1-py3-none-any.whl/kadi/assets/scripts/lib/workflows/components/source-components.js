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

import {sockets, BuiltinComponent} from 'core';
import CheckboxControl from 'scripts/lib/workflows/controls/checkbox-control';
import FloatControl from 'scripts/lib/workflows/controls/float-control';
import IntControl from 'scripts/lib/workflows/controls/int-control';
import TextControl from 'scripts/lib/workflows/controls/text-control';

/** Class for all source components, which contain different controls and widgets for their input. */
class SourceComponent extends BuiltinComponent {
  constructor(name, socket, widget) {
    super(name, 'source', 'Source', [], [{key: 'out', title: name, socket, multi: true}]);
    this.widget = widget;
  }

  builder(node) {
    super.builder(node);
    // eslint-disable-next-line new-cap
    node.addControl(new this.widget('value'));
  }

  fromFlow(flowNode) {
    const node = super.fromFlow(flowNode);
    node.data.value = flowNode.model.value;
    return node;
  }

  toFlow(node) {
    const flowNode = super.toFlow(node);
    // All values are currently stored as strings.
    flowNode.model.value = String(node.data.value);
    return flowNode;
  }
}

const string = new SourceComponent('String', sockets.str, TextControl);
const integer = new SourceComponent('Integer', sockets.int, IntControl);
const float = new SourceComponent('Float', sockets.float, FloatControl);
const boolean = new SourceComponent('Boolean', sockets.bool, CheckboxControl);

export default [string, integer, float, boolean];
