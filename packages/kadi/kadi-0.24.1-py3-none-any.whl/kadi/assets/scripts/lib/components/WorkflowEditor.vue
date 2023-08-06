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

<template>
  <div ref="container">
    <div v-if="toolsEndpoint">
      <div class="modal-backdrop show" v-if="toolDialogActive"></div>
      <div class="modal" tabindex="-1" ref="toolDialog">
        <div class="modal-dialog modal-dialog-centered modal-lg">
          <div class="modal-content">
            <div class="modal-body">
              <dynamic-pagination placeholder="No tools."
                                  filter-placeholder="Filter by filename or record identifier"
                                  :endpoint="toolsEndpoint"
                                  :per-page="5"
                                  :enable-filter="true">
                <template #default="props">
                  <div class="d-flex justify-content-between mb-4">
                    <div>
                      <strong>Tools</strong>
                      <span class="badge badge-pill badge-light text-muted border border-muted">{{ props.total }}</span>
                    </div>
                    <button type="button" class="close" data-dismiss="modal">
                      <i class="fa-solid fa-xmark fa-xs"></i>
                    </button>
                  </div>
                  <ul class="list-group" v-if="props.total > 0">
                    <li class="list-group-item bg-light py-2">
                      <div class="row">
                        <div class="col-lg-5">File</div>
                        <div class="col-lg-5">Tool</div>
                      </div>
                    </li>
                    <li class="list-group-item py-2" v-for="item in props.items" :key="item.id">
                      <div class="row align-items-center">
                        <div class="col-lg-5 mb-2 mb-lg-0">
                          <strong>{{ item.file }}</strong>
                          <br>
                          @{{ item.record }}
                        </div>
                        <div class="col-lg-5 mb-2 mb-lg-0">
                          <strong>{{ item.tool.name }}</strong>
                          <small>[{{ item.tool.type }}]</small>
                          <span v-if="item.tool.version">
                            <br>
                            Version {{ item.tool.version }}
                          </span>
                        </div>
                        <div class="col-lg-2 d-lg-flex justify-content-end">
                          <div>
                            <button type="button" class="btn btn-light btn-sm" @click="addTool(item.tool)">
                              <i class="fa-solid fa-plus"></i>
                            </button>
                          </div>
                        </div>
                      </div>
                    </li>
                  </ul>
                </template>
              </dynamic-pagination>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="card editor-container" :class="{'bg-light': !editable}" ref="editorContainer">
      <div class="editor-toolbar mt-1 mr-1" ref="editorToolbar">
        <button type="button" title="Reset view" :class="toolbarBtnClasses" @click="resetView">
          <i class="fa-solid fa-eye"></i>
        </button>
        <button type="button" title="Toggle fullscreen" :class="toolbarBtnClasses" @click="toggleFullscreen">
          <i class="fa-solid fa-expand"></i>
        </button>
        <button type="button" title="Reset editor" :class="toolbarBtnClasses" v-if="editable" @click="resetEditor">
          <i class="fa-solid fa-broom"></i>
        </button>
      </div>
      <div ref="editor"></div>
    </div>
    <slot :editor="editor"></slot>
  </div>
</template>

<style scoped>
.editor-container {
  border: 1px solid #ced4da;
}

.editor-toolbar {
  position: absolute;
  right: 0;
  z-index: 1;
}
</style>

<script>
import 'regenerator-runtime';

import AreaPlugin from 'rete-area-plugin';
import ConnectionPlugin from 'rete-connection-plugin';
import ContextMenuPlugin from 'rete-context-menu-plugin';
import VueRenderPlugin from 'rete-vue-render-plugin';

import WorkflowEditor from 'scripts/lib/workflows/editor';
import Menu from 'scripts/lib/workflows/core/Menu.vue';
import controlComponents from 'scripts/lib/workflows/components/control-components';
import fileIoComponents from 'scripts/lib/workflows/components/file-io-components';
import sourceComponents from 'scripts/lib/workflows/components/source-components';
import userInputComponents from 'scripts/lib/workflows/components/user-input-components';
import userOutputComponents from 'scripts/lib/workflows/components/user-output-components';
import {ToolComponent} from 'scripts/lib/workflows/components/core';

import 'styles/workflows/workflow-editor.scss';

export default {
  data() {
    return {
      version: 'kadi@0.1.0',
      editor: null,
      area: null,
      unsavedChanges_: false,
      toolDialogActive: false,
      menuItems: {},
      currX: 0,
      currY: 0,
    };
  },
  props: {
    editable: {
      type: Boolean,
      default: true,
    },
    workflowUrl: {
      type: String,
      default: null,
    },
    toolsEndpoint: {
      type: String,
      default: null,
    },
    unsavedChanges: {
      type: Boolean,
      default: false,
    },
    isRendered: {
      type: Boolean,
      default: true,
    },
    enableDebugMenu: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    toolbarBtnClasses() {
      return 'btn btn-link text-muted';
    },
  },
  watch: {
    workflowUrl() {
      this.loadWorkflow(this.workflowUrl);
    },
    unsavedChanges() {
      this.unsavedChanges_ = this.unsavedChanges;
    },
    unsavedChanges_() {
      this.$emit('unsaved-changes', this.unsavedChanges_);
    },
    isRendered() {
      this.resizeView(false);
    },
  },
  methods: {
    isFullscreen() {
      return document.fullScreen || document.mozFullScreen || document.webkitIsFullScreen;
    },
    resetView() {
      this.area.zoomAt(this.editor);
    },
    toggleFullscreen() {
      if (this.isFullscreen()) {
        document.exitFullscreen();
      } else {
        this.$refs.container.requestFullscreen();
      }
    },
    resetEditor() {
      if (!window.confirm('Are you sure you want to reset the editor?')) {
        return;
      }

      this.editor.clear();
      this.unsavedChanges_ = false;
    },
    resizeView(resetView = true) {
      // In case the component is not marked as rendered from the outside we do not attempt to resize it.
      if (!this.isRendered) {
        return;
      }

      const width = this.$refs.editorContainer.getBoundingClientRect().width;
      if (this.isFullscreen()) {
        this.$refs.editorContainer.style.height = '100vh';
        this.$refs.editorContainer.style.borderRadius = '0';
      } else {
        this.$refs.editorContainer.style.height = `${Math.round(window.innerHeight / window.innerWidth * width)}px`;
        this.$refs.editorContainer.style.borderRadius = '0.25rem';
      }
      this.editor.view.resize();

      if (resetView) {
        this.resetView();
      }
    },
    loadWorkflow(url) {
      axios.get(url)
        .then((response) => {
          // Catch errors in the custom conversion function as well.
          try {
            this.editor.fromFlow(response.data)
              .then((success) => {
                if (!success) {
                  kadi.alert('Could not fully reconstruct workflow.', {type: 'warning'});
                }
              })
              .catch((error) => {
                console.error(error);
                kadi.alert('Error parsing workflow data.');
              })
              .finally(() => this.resetView());
          } catch (error) {
            console.error(error);
            kadi.alert('Error parsing workflow data.');
          }
        })
        .catch((error) => kadi.alert('Error loading workflow.', {request: error.request}));
    },
    addTool(tool) {
      const componentName = ToolComponent.nameFromTool(tool);

      // Register the tool node if it is missing.
      if (!this.editor.components.has(componentName)) {
        this.editor.register(new ToolComponent(tool));
      }

      this.addNode(this.editor.components.get(componentName));
    },
    async addNode(component) {
      const node = await component.createNode();

      node.position[0] = this.currX;
      node.position[1] = this.currY;

      this.editor.addNode(node);
    },
    beforeUnload(e) {
      if (this.unsavedChanges_) {
        e.preventDefault();
        (e || window.event).returnValue = '';
        return '';
      }
      return null;
    },
  },
  mounted() {
    this.editor = new WorkflowEditor(this.version, this.$refs.editor);
    this.area = AreaPlugin;

    // Disable some events if the editor is not editable.
    if (!this.editable) {
      let handler = (e) => {
        // Do not disable the toolbar.
        if (!Array.from(this.$refs.editorToolbar.getElementsByTagName('*')).includes(e.target)) {
          e.preventDefault();
          e.stopPropagation();
        }
      };
      this.$refs.editorContainer.addEventListener('click', handler, {capture: true});

      handler = (e) => {
        if (e.target !== this.$refs.editor) {
          e.preventDefault();
          e.stopPropagation();
        }
      };
      this.$refs.editorContainer.addEventListener('pointerdown', handler, {capture: true});
      this.$refs.editorContainer.addEventListener('pointerup', handler, {capture: true});

      handler = (e) => {
        e.preventDefault();
        e.stopPropagation();
      };
      this.$refs.editorContainer.addEventListener('dblclick', handler, {capture: true});
      this.$refs.editorContainer.addEventListener('contextmenu', handler, {capture: true});
    }

    // Register plugins.
    this.editor.use(AreaPlugin, {snap: {size: 16, dynamic: true}});
    this.editor.use(ConnectionPlugin);
    this.editor.use(VueRenderPlugin);
    this.editor.use(ContextMenuPlugin, {
      vueComponent: Menu,
      searchBar: true,
      delay: 0,
      items: this.menuItems,
      allocate: () => null,
    });

    // Register components.
    [
      ...sourceComponents,
      ...controlComponents,
      ...fileIoComponents,
      ...userInputComponents,
      ...userOutputComponents,
    ].forEach((c) => this.editor.register(c));

    // Setup context menu.
    if (this.toolsEndpoint) {
      this.menuItems['Select Tools...'] = () => {
        this.toolDialogActive = true;
        $(this.$refs.toolDialog).modal({backdrop: false});
      };
      $(this.$refs.toolDialog).on('hidden.bs.modal', () => {
        this.toolDialogActive = false;
      });
    }

    for (const component of this.editor.components.values()) {
      if (!this.menuItems[component.menu]) {
        this.menuItems[component.menu] = {};
      }
      this.menuItems[component.menu][component.name] = () => this.addNode(component);
    }

    if (this.enableDebugMenu) {
      this.menuItems.Debug = {
        /* eslint-disable no-console */
        'Dump Flow': () => console.info(this.editor.toFlow()),
        'Dump JSON': () => console.info(this.editor.toJSON()),
        /* eslint-enable no-console */
      };
    }

    this.editor.on('showcontextmenu', ({e}) => {
      const area = this.editor.view.area;
      const rect = area.el.getBoundingClientRect();

      // Store the mouse position at the time the context menu was opened.
      this.currX = (e.clientX - rect.left) / area.transform.k;
      this.currY = (e.clientY - rect.top) / area.transform.k;
    });

    // Handle unsaved changes on all relevant events.
    const events = [
      'controlchanged',
      'profilechanged',
      'nodecreated',
      'noderemoved',
      'nodetranslated',
      'connectioncreated',
      'connectionremoved',
    ];
    this.editor.on(events.join(' '), () => {
      if (!this.editor.silent) {
        this.unsavedChanges_ = true;
      }
    });

    // Finish initializion.
    this.resizeView();

    if (this.workflowUrl) {
      this.loadWorkflow(this.workflowUrl);
    }

    window.addEventListener('resize', this.resizeView);
    window.addEventListener('beforeunload', this.beforeUnload);
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.resizeView);
    window.removeEventListener('beforeunload', this.beforeUnload);
    $(this.$refs.toolDialog).modal('dispose');
  },
};
</script>
