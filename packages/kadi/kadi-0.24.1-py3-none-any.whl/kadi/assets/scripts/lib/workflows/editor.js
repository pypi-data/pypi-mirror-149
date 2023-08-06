/* Copyright 2020 Karlsruhe Institute of Technology
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

import {ToolComponent} from 'components/core';

/** Custom node editor class representing the workflow editor. */
export default class WorkflowEditor extends Rete.NodeEditor {
  constructor(id, container) {
    super(id, container);

    // Register all custom events.
    this.bind('controlchanged');
    this.bind('profilechanged');
    this.bind('socketenter');
    this.bind('socketleave');

    // Clear all selected nodes when clicking outside any node.
    this.on('click', () => {
      this.selected.clear();
      this.nodes.map((n) => n.update());
    });

    // Disable zoom on double click.
    this.on('zoom', ({source}) => source !== 'dblclick');

    // Move the currently selected node to the 'top' of the DOM, if not already the case.
    this.on('nodeselected', (node) => {
      const nodeElement = this.view.nodes.get(node).el;
      const parentElement = nodeElement.parentElement;

      if (parentElement.lastElementChild !== nodeElement) {
        parentElement.lastElementChild.after(nodeElement);
      }
    });
  }

  static iterValueAt(iterator, index) {
    let _index = index;
    for (const value of iterator) {
      if (--_index < 0) {
        return value;
      }
    }
    return null;
  }

  /** Restore the contents of the editor using the custom Flow JSON format. */
  fromFlow(flowData) {
    const data = {
      id: flowData.id || this.id,
      nodes: {},
    };

    // Handle the nodes first, without their connections.
    let node = null;
    for (const flowNode of flowData.nodes) {
      if (['ToolNode', 'EnvNode'].includes(flowNode.model.name)) {
        const componentName = ToolComponent.nameFromTool(flowNode.model.tool);

        // Register the tool node if it is missing.
        if (!this.components.has(componentName)) {
          const tool = ToolComponent.toolFromFlow(flowNode);
          this.register(new ToolComponent(tool));
        }

        const component = this.components.get(componentName);
        node = component.fromFlow(flowNode);
      } else {
        const component = this.components.get(flowNode.model.name);
        // Continue if the built-in component is missing.
        if (component) {
          node = component.fromFlow(flowNode);
        } else {
          continue;
        }
      }

      data.nodes[flowNode.id] = node;
    }

    // Handle the node connections.
    for (const connection of flowData.connections) {
      const outNode = data.nodes[connection.out_id];
      const inNode = data.nodes[connection.in_id];

      if (outNode && inNode) {
        const outputKey = WorkflowEditor.iterValueAt(outNode.outputs.keys(), connection.out_index);
        const inputKey = WorkflowEditor.iterValueAt(inNode.inputs.keys(), connection.in_index);

        const output = outNode.outputs.get(outputKey);
        const input = inNode.inputs.get(inputKey);

        if (output && input) {
          output.connections.push({node: inNode.id, input: inputKey, data: {}});
          input.connections.push({node: outNode.id, output: outputKey, data: {}});
        }
      }
    }

    // Convert all maps back to primitive objects.
    for (const key in data.nodes) {
      data.nodes[key].outputs = Object.fromEntries(data.nodes[key].outputs);
      data.nodes[key].inputs = Object.fromEntries(data.nodes[key].inputs);
    }

    return this.fromJSON(data);
  }

  /** Save the contents of the editor using the custom Flow JSON format. */
  toFlow() {
    const flowData = {
      id: this.id,
      connections: [],
      nodes: [],
    };

    for (const node of this.nodes) {
      const component = this.components.get(node.name);
      const flowNode = component.toFlow(node);

      // Handle the connections of the node. Only the outputs are considered for each node.
      const iterator = node.outputs.values();
      for (let index = 0; index < node.outputs.size; index++) {
        const output = iterator.next().value;

        for (const connection of output.connections) {
          // Since maps are used for the inputs, the indices can be safely retrieved from this array.
          const connectionKeys = [...connection.input.node.inputs.keys()];
          const flowConnection = {
            in_id: connection.input.node.id,
            in_index: connectionKeys.findIndex((key) => key === connection.input.key),
            out_id: node.id,
            out_index: index,
          };
          flowData.connections.push(flowConnection);
        }
      }

      flowData.nodes.push(flowNode);
    }

    return flowData;
  }
}
