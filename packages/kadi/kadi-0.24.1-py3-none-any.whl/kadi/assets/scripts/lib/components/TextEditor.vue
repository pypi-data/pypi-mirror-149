<!-- Copyright 2022 Karlsruhe Institute of Technology
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
  <div>
    <small class="text-muted">
      <i class="fa-solid fa-circle-info"></i> {{ $t('Note that text files are always handled using UTF-8 encoding.') }}
    </small>
    <div class="editor" ref="editor"></div>
    <div class="card bg-light footer">
      <div class="d-flex justify-content-between text-muted">
        <small>
          <span class="cursor-pointer" @click="changeIndentation">
            <span v-if="indentation === 'space'">{{ $t('Spaces') }}</span>
            <span v-else>{{ $t('Tabs') }}</span>
          </span>
        </small>
        <small>
          <span class="cursor-pointer" @click="changeNewline">
            <span v-if="newline === 'unix'">Unix/Mac (LF)</span>
            <span v-else>Windows (CR LF)</span>
          </span>
        </small>
      </div>
    </div>
    <slot :document="editor ? editor.state.doc : null" :newline="newline"></slot>
  </div>
</template>

<style scoped>
.editor {
  border: 1px solid #ced4da;
  font-size: 10pt;
  height: 55vh;
}

.footer {
  border-color: #ced4da;
  border-top-left-radius: 0px;
  border-top-right-radius: 0px;
  margin-top: -1px;
  padding-left: 10px;
  padding-right: 10px;
}
</style>

<script>
import {history, historyKeymap, indentLess, indentMore} from '@codemirror/commands';
import {indentUnit} from '@codemirror/language';
import {EditorState, Compartment} from '@codemirror/state';
import {
  EditorView,
  gutter,
  highlightActiveLine,
  highlightActiveLineGutter,
  keymap,
  lineNumbers,
} from '@codemirror/view';
import {detectNewlineGraceful} from 'detect-newline';
import detectIndent from 'detect-indent';

export default {
  data() {
    return {
      editor: null,
      indentCompartment: null,
      newline: 'unix',
      indentation: 'space',
      unsavedChanges_: false,
    };
  },
  props: {
    textUrl: {
      type: String,
      default: null,
    },
    unsavedChanges: {
      type: Boolean,
      default: false,
    },
  },
  watch: {
    textUrl() {
      this.loadTextFile(this.textUrl);
    },
    unsavedChanges() {
      this.unsavedChanges_ = this.unsavedChanges;
    },
    unsavedChanges_() {
      this.$emit('unsaved-changes', this.unsavedChanges_);
    },
  },
  methods: {
    createEditorState(text = '') {
      const tabBinding = {
        key: 'Tab',
        run: (command) => {
          const selection = command.state.selection.ranges[0];

          // Insert spaces/tabs when no text is selected, indent otherwise.
          if (selection.to === selection.from) {
            const indentation = this.indentation === 'space' ? '  ' : '\t';
            command.dispatch(command.state.replaceSelection(indentation));
          } else {
            indentMore(command);
          }

          return true;
        },
        shift(command) {
          indentLess(command);
          return true;
        },
      };

      const onUpdate = (update) => {
        if (update.docChanged) {
          this.unsavedChanges_ = true;
        }
      };

      // Using a Compartment for the indentation is required to reconfigure it on the fly.
      this.indentCompartment = new Compartment();

      return EditorState.create({
        doc: text,
        extensions: [
          this.indentCompartment.of(indentUnit.of(this.getIndentation())),
          EditorView.updateListener.of(onUpdate),
          gutter(),
          highlightActiveLine(),
          highlightActiveLineGutter(),
          history(),
          keymap.of([tabBinding, ...historyKeymap]),
          lineNumbers(),
        ],
      });
    },
    getIndentation() {
      return this.indentation === 'space' ? '  ' : '\t';
    },
    changeIndentation() {
      if (this.indentation === 'space') {
        this.indentation = 'tab';
      } else {
        this.indentation = 'space';
      }

      // Reconfigure the indentation as well.
      this.editor.dispatch({
        effects: this.indentCompartment.reconfigure(indentUnit.of(this.getIndentation())),
      });
    },
    changeNewline() {
      if (this.newline === 'unix') {
        this.newline = 'windows';
      } else {
        this.newline = 'unix';
      }
    },
    loadTextFile(url) {
      axios.get(url, {responseType: 'text', transformResponse: [(data) => data]})
        .then((response) => {
          this.indentation = detectIndent(response.data).type || 'space';

          if (detectNewlineGraceful(response.data) === '\n') {
            this.newline = 'unix';
          } else {
            this.newline = 'windows';
          }

          // Replace all Windows-style newlines, as we always use a single Unix-style newline internally.
          const text = response.data.replaceAll('\r\n', '\n');
          // Set a new editor state to reset the history.
          this.editor.setState(this.createEditorState(text));
          this.unsavedChanges_ = false;
        })
        .catch((error) => kadi.alert($t('Error loading text file.'), {request: error.request}));
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
    this.editor = new EditorView({
      state: this.createEditorState(),
      parent: this.$refs.editor,
    });

    if (this.textUrl) {
      this.loadTextFile(this.textUrl);
    }

    window.addEventListener('beforeunload', this.beforeUnload);
  },
  beforeDestroy() {
    this.editor.destroy();
    window.removeEventListener('beforeunload', this.beforeUnload);
  },
};
</script>
