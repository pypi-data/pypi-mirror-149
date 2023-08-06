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

import {v4 as uuidv4} from 'uuid';
import Rete from 'rete';

import Node from 'scripts/lib/workflows/core/Node.vue';

export const sockets = {
  str: new Rete.Socket('str'),
  int: new Rete.Socket('int'),
  float: new Rete.Socket('float'),
  bool: new Rete.Socket('bool'),
  dep: new Rete.Socket('dep'),
  pipe: new Rete.Socket('pipe'),
  env: new Rete.Socket('env'),
};

export const socketCombinations = {
  str: ['int', 'float', 'bool'],
  int: ['str', 'float'],
  float: ['str', 'int'],
  bool: ['str'],
  pipe: ['str', 'int', 'float', 'bool'],
};

// Actually register all possible socket combinations.
for (const [socketIn, socketsOut] of Object.entries(socketCombinations)) {
  for (const socketOut of socketsOut) {
    sockets[socketIn].combineWith(sockets[socketOut]);
  }
}

export const commonInputs = {
  dep: {key: 'dependency', title: 'Dependencies', socket: sockets.dep, multi: true},
  pipe: {key: 'pipe', title: 'stdin', socket: sockets.pipe},
  env: {key: 'env', title: 'env', socket: sockets.env},
};

export const commonOutputs = {
  dep: {key: 'dependency', title: 'Dependents', socket: sockets.dep, multi: true},
  pipe: {key: 'pipe', title: 'stdout', socket: sockets.pipe},
  env: {key: 'env', title: 'env', socket: sockets.env},
};

const executionProfiles = ['Default', 'Skip', 'Detached'];

// Built-in input keys/port types of tool nodes that require special handling.
const builtinInputKeys = [commonInputs.dep.key, commonInputs.pipe.key, commonInputs.env.key];

/** Base class for all custom components. */
class BaseComponent extends Rete.Component {
  constructor(name, type) {
    super(name);
    this.type = type;
    this.data.component = Node;
    this.data.props = {executionProfiles};
  }

  static makeInput(input) {
    return new Rete.Input(input.key, input.title, input.socket, input.multi || false);
  }

  static makeOutput(output) {
    return new Rete.Output(output.key, output.title, output.socket, output.multi || false);
  }

  /* eslint-disable class-methods-use-this */
  builder(node) {
    node.type = this.type;

    // Check whether the node already has a UUID from loading it via a Flow file.
    if (typeof (node.id) === 'number') {
      node.id = `{${uuidv4()}}`;
    }

    // Retrieve any additional properties from Flow nodes and delete them from the data property afterwards.
    if (node.data._meta) {
      for (const [key, value] of Object.entries(node.data._meta)) {
        node[key] = value;
      }
      delete node.data._meta;
    }

    // Initialize the custom execution profile, if not already done in the previous step.
    if (!node.executionProfile) {
      node.executionProfile = executionProfiles[0];
    }
  }

  fromFlow(flowNode) {
    const node = {
      id: flowNode.id,
      name: flowNode.model.name,
      // Only some properties are passed to the created node and therefore the "builder" method, so we use the data
      // property to pass additional meta properties from a Flow node.
      data: {_meta: {
        executionProfile: flowNode.model.executionProfile,
      }},
      inputs: new Map(),
      outputs: new Map(),
      position: [flowNode.position.x, flowNode.position.y],
    };
    return node;
  }

  toFlow(node) {
    const flowNode = {
      id: node.id,
      model: {
        name: node.name,
        executionProfile: node.executionProfile,
      },
      position: {
        x: node.position[0],
        y: node.position[1],
      },
    };
    return flowNode;
  }
  /* eslint-enable class-methods-use-this */
}

/** Class for all (static) built-in components. */
export class BuiltinComponent extends BaseComponent {
  constructor(name, type, menu, inputs = [], outputs = []) {
    super(name, type);
    this.menu = menu;
    this.inputs = inputs;
    this.outputs = outputs;
  }

  builder(node) {
    super.builder(node);

    for (const input of this.inputs) {
      node.addInput(BuiltinComponent.makeInput(input));
    }
    for (const output of this.outputs) {
      node.addOutput(BuiltinComponent.makeOutput(output));
    }
  }

  fromFlow(flowNode) {
    const node = super.fromFlow(flowNode);

    for (const input of this.inputs) {
      node.inputs.set(input.key, {connections: []});
    }
    for (const output of this.outputs) {
      node.outputs.set(output.key, {connections: []});
    }

    return node;
  }
}

/** Class for all (dynamic) tool components. */
export class ToolComponent extends BaseComponent {
  constructor(tool) {
    super(ToolComponent.nameFromTool(tool), tool.type);
    this.tool = tool;
  }

  static nameFromTool(tool) {
    if (tool.version !== null) {
      return `${tool.name} ${tool.version}`;
    }

    return tool.name;
  }

  static toolFromFlow(flowNode) {
    const flowTool = flowNode.model.tool;
    const tool = {
      type: flowNode.model.name === 'ToolNode' ? 'program' : 'env',
      name: flowTool.name,
      version: flowTool.version,
      path: flowTool.path,
      param: [],
    };

    for (const port of flowNode.model.tool.ports) {
      if (!builtinInputKeys.includes(port.type)) {
        const param = {
          name: port.name,
          char: port.shortName,
          type: port.type,
          required: port.required || false,
        };
        tool.param.push(param);
      }
    }

    return tool;
  }

  static makeFlowPort(io, direction, index) {
    if (io.param) {
      return {
        name: io.param.name,
        shortName: io.param.char,
        type: io.param.type,
        required: io.param.required,
        port_direction: direction,
        port_index: index,
      };
    }

    return {
      name: io.name,
      shortName: null,
      type: io.key,
      required: false,
      port_direction: direction,
      port_index: index,
    };
  }

  builder(node) {
    super.builder(node);

    // Inputs.
    if (this.type === 'program') {
      node.addInput(ToolComponent.makeInput(commonInputs.dep));
    }

    for (let i = 0; i < this.tool.param.length; i++) {
      const param = this.tool.param[i];
      const paramName = param.name || `arg${i}`;

      let title = null;
      let socket = null;

      switch (param.type) {
      case 'string':
        title = `String: ${paramName}`;
        socket = sockets.str;
        break;
      case 'int':
      case 'long':
        title = `Integer: ${paramName}`;
        socket = sockets.int;
        break;
      case 'float':
      case 'real':
        title = `Float: ${paramName}`;
        socket = sockets.float;
        break;
      case 'bool':
      case 'flag':
        title = `Boolean: ${paramName}`;
        socket = sockets.bool;
        break;
      default:
        title = `${kadi.utils.capitalize(param.type)}: ${paramName}`;
        socket = sockets.str;
      }

      const input = new Rete.Input(`in${i}`, title, socket);
      input.param = param;
      node.addInput(input);
    }

    if (this.type === 'program') {
      node.addInput(ToolComponent.makeInput(commonInputs.env));
      node.addInput(ToolComponent.makeInput(commonInputs.pipe));
    }

    // Outputs.
    if (this.type === 'program') {
      node.addOutput(ToolComponent.makeOutput(commonOutputs.dep));
      node.addOutput(ToolComponent.makeOutput(commonOutputs.pipe));
    } else if (this.type === 'env') {
      node.addOutput(ToolComponent.makeOutput(commonOutputs.env));
    }
  }

  // eslint-disable-next-line class-methods-use-this
  fromFlow(flowNode) {
    const node = super.fromFlow(flowNode);
    node.name = ToolComponent.nameFromTool(flowNode.model.tool);

    let inputIndex = 0;
    for (const port of flowNode.model.tool.ports) {
      if (port.port_direction === 'in') {
        if (builtinInputKeys.includes(port.type)) {
          node.inputs.set(port.type, {connections: []});
        } else {
          node.inputs.set(`in${inputIndex++}`, {connections: []});
        }
      } else {
        // Tool nodes only use built-in outputs so far.
        node.outputs.set(port.type, {connections: []});
      }
    }

    return node;
  }

  toFlow(node) {
    const flowNode = super.toFlow(node);

    flowNode.model.name = this.type === 'program' ? 'ToolNode' : 'EnvNode';
    flowNode.model.tool = {
      name: this.tool.name,
      version: this.tool.version,
      // Take the path of the tool if it is included or fall back to its name.
      path: this.tool.path || this.tool.name,
      ports: [],
    };

    let iterator = node.inputs.values();

    for (let index = 0; index < node.inputs.size; index++) {
      const input = iterator.next().value;
      const port = ToolComponent.makeFlowPort(input, 'in', index);
      flowNode.model.tool.ports.push(port);
    }

    iterator = node.outputs.values();

    for (let index = 0; index < node.outputs.size; index++) {
      const output = iterator.next().value;
      const port = ToolComponent.makeFlowPort(output, 'out', index);
      flowNode.model.tool.ports.push(port);
    }

    return flowNode;
  }
}
