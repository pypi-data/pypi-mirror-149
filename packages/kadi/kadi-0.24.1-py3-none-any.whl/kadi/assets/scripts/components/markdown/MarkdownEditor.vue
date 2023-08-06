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
  <div>
    <div class="card toolbar">
      <div class="card-body px-0 py-0">
        <span v-for="tool in toolbar" :key="tool.title">
          <span class="separator d-none d-md-inline" v-if="tool === '|'"></span>
          <button type="button"
                  :class="toolbarBtnClasses"
                  :title="tool.title"
                  :disabled="previewActive"
                  @click="tool.handler"
                  v-else>
            <i :class="tool.icon"></i>
          </button>
        </span>
        <span class="separator d-none d-md-inline"></span>
        <button type="button"
                :title="$t('Link')"
                :class="toolbarBtnClasses + (linkSelectionActive ? ' border-active' : '')"
                :disabled="previewActive"
                @click="insertLink(true)">
          <i class="fa-solid fa-link"></i>
        </button>
        <button type="button"
                :title="$t('Image')"
                :class="toolbarBtnClasses + (imageSelectionActive ? ' border-active' : '')"
                :disabled="previewActive"
                @click="insertImage">
          <i class="fa-solid fa-image"></i>
        </button>
        <div class="float-lg-right">
          <button type="button"
                  :title="`${$t('Preview')} (${$t('Ctrl')}+P)`"
                  :class="toolbarBtnClasses + (previewActive ? ' border-active' : '')"
                  @click="previewActive = !previewActive">
            <i class="fa-solid fa-eye"></i>
          </button>
          <span class="separator"></span>
          <button type="button"
                  :title="`${$t('Undo')} (${$t('Ctrl')}+Z)`"
                  :class="toolbarBtnClasses"
                  :disabled="!undoable"
                  @click="undo">
            <i class="fa-solid fa-rotate-left"></i>
          </button>
          <button type="button"
                  :title="`${$t('Redo')} (${$t('Ctrl')}+Y)`"
                  :class="toolbarBtnClasses"
                  :disabled="!redoable"
                  @click="redo">
            <i class="fa-solid fa-rotate-right"></i>
          </button>
        </div>
        <div class="mb-2" v-if="linkSelectionActive && !previewActive" key="link">
          <hr class="mt-0 mb-2">
          <div class="form-row">
            <div class="col-md-4 mb-2 mb-md-0">
              <button type="button" class="btn btn-sm btn-block btn-light" @click="insertLink(false)">
                <i class="fa-solid fa-link"></i> {{ $t('Insert link placeholder') }}
              </button>
            </div>
            <div class="col-md-8">
              <dynamic-selection container-classes="select2-single-sm"
                                 :placeholder="$t('Select a record file to link to')"
                                 :endpoint="linkEndpoint"
                                 :reset-on-select="true"
                                 @select="selectLink">
              </dynamic-selection>
            </div>
          </div>
        </div>
        <div class="mb-2" v-if="imageSelectionActive && !previewActive" key="image">
          <hr class="mt-0 mb-2">
          <dynamic-selection container-classes="select2-single-sm"
                             :placeholder="$t('Select an uploaded JPEG or PNG image')"
                             :endpoint="imageEndpoint"
                             :reset-on-select="true"
                             @select="selectImage">
          </dynamic-selection>
        </div>
      </div>
    </div>
    <div v-show="!previewActive">
      <textarea class="form-control editor"
                :id="id"
                :name="name"
                :required="required"
                :rows="rows"
                :class="{'has-error': hasError}"
                v-model="input"
                @keydown.tab="handleTab"
                @keydown.tab.prevent
                @keydown.enter="handleEnter"
                @keydown.enter.prevent
                ref="editor">
      </textarea>
      <div class="card bg-light footer">
        <small class="text-muted">
          {{ $t('This editor supports Markdown, including math written in LaTeX syntax rendered with') }}
          <a class="text-muted ml-1"
             href="https://katex.org/docs/supported.html"
             target="_blank"
             rel="noopener noreferrer">
            <i class="fa-solid fa-arrow-up-right-from-square"></i>
            <strong>KaTeX</strong>.
          </a>
          {{ $t('Note that HTML tags and external images are not supported.') }}
        </small>
      </div>
    </div>
    <div v-show="previewActive">
      <div class="card preview" tabindex="-1" ref="preview">
        <div class="card-body pb-0">
          <markdown-preview :input="input"></markdown-preview>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.border-active {
  border: 1px solid #ced4da;
}

.editor {
  border-radius: 0px;
  box-shadow: none;
  font-family: monospace, monospace;
  font-size: 10pt;
  position: relative;
  z-index: 1;
}

.footer {
  border-color: #ced4da;
  border-top-left-radius: 0px;
  border-top-right-radius: 0px;
  margin-top: -1px;
  padding-left: 10px;
  padding-right: 10px;
}

.preview {
  border-color: #ced4da;
  border-top-left-radius: 0px;
  border-top-right-radius: 0px;
}

.separator {
  border-right: 1px solid #dfdfdf;
  margin-left: 7px;
  margin-right: 11px;
  padding-bottom: 3px;
  padding-top: 3px;
}

.toolbar {
  border-bottom-left-radius: 0px;
  border-bottom-right-radius: 0px;
  border-color: #ced4da;
  margin-bottom: -1px;
  padding-left: 10px;
  padding-right: 10px;
}

.toolbar-btn {
  margin-left: -5px;
  margin-right: -5px;
  width: 45px;
}
</style>

<script>
import undoRedoMixin from 'scripts/lib/components/mixins/undo-redo-mixin';

export default {
  mixins: [undoRedoMixin],
  data() {
    return {
      input: this.initialValue,
      tabSize: 4,
      previewActive: false,
      linkSelectionActive: false,
      imageSelectionActive: false,
      inputTimeoutHandle: null,
      undoStackDepth: 25,
      toolbar: [
        {
          icon: 'fa-solid fa-heading',
          title: `${$t('Heading')} (${$t('Ctrl')}+H)`,
          handler: this.toggleHeading,
          shortcut: 'h',
        },
        {
          icon: 'fa-solid fa-bold',
          title: `${$t('Bold')} (${$t('Ctrl')}+B)`,
          handler: this.toggleBold,
          shortcut: 'b',
        },
        {
          icon: 'fa-solid fa-italic',
          title: `${$t('Italic')} (${$t('Ctrl')}+I)`,
          handler: this.toggleItalic,
          shortcut: 'i',
        },
        {
          icon: 'fa-solid fa-strikethrough',
          title: `${$t('Strikethrough')} (${$t('Ctrl')}+S)`,
          handler: this.toggleStrikethrough,
          shortcut: 's',
        },
        {
          icon: 'fa-solid fa-superscript',
          title: `${$t('Superscript')} (${$t('Ctrl')}+1)`,
          handler: this.toggleSuperscript,
          shortcut: '1',
        },
        {
          icon: 'fa-solid fa-subscript',
          title: `${$t('Subscript')} (${$t('Ctrl')}+2)`,
          handler: this.toggleSubscript,
          shortcut: '2',
        },
        '|',
        {
          icon: 'fa-solid fa-code',
          title: `${$t('Code')} (${$t('Ctrl')}+D)`,
          handler: this.toggleCode,
          shortcut: 'd',
        },
        {
          icon: 'fa-solid fa-square-root-variable',
          title: `${$t('Math')} (${$t('Ctrl')}+M)`,
          handler: this.toggleMath,
          shortcut: 'm',
        },
        '|',
        {
          icon: 'fa-solid fa-list-ul',
          title: `${$t('Unordered list')} (${$t('Ctrl')}+U)`,
          handler: this.toggleUnorderedList,
          shortcut: 'u',
        },
        {
          icon: 'fa-solid fa-list-ol',
          title: `${$t('Ordered list')} (${$t('Ctrl')}+O)`,
          handler: this.toggleOrderedList,
          shortcut: 'o',
        },
        '|',
        {
          icon: 'fa-solid fa-minus',
          title: $t('Horizontal rule'),
          handler: this.insertHorizontalRule,
        },
        {
          icon: 'fa-solid fa-table',
          title: $t('Table'),
          handler: this.insertTable,
        },
      ],
    };
  },
  props: {
    id: {
      type: String,
      default: 'markdown-editor',
    },
    name: {
      type: String,
      default: 'markdown-editor',
    },
    required: {
      type: Boolean,
      default: false,
    },
    initialValue: {
      type: String,
      default: '',
    },
    rows: {
      type: Number,
      default: 8,
    },
    autosize: {
      type: Boolean,
      default: true,
    },
    linkEndpoint: {
      type: String,
      default: null,
    },
    imageEndpoint: {
      type: String,
      default: null,
    },
    hasError: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    toolbarBtnClasses() {
      return 'btn btn-link text-primary toolbar-btn my-1';
    },
  },
  watch: {
    input() {
      this.$emit('input', this.input);

      window.clearTimeout(this.inputTimeoutHandle);
      this.inputTimeoutHandle = window.setTimeout(() => {
        this.saveCheckpoint();
      }, 500);
    },
  },
  methods: {
    selectRange(selectionStart, selectionEnd = null) {
      this.$nextTick(() => {
        const editor = this.$refs.editor;
        // Set a single caret first, then focus the editor to scroll to it, then apply the actual selection range, if
        // applicable. This produces somewhat consistent results across browsers.
        editor.selectionStart = editor.selectionEnd = selectionEnd || selectionStart;
        editor.focus();
        editor.selectionStart = Math.max(selectionStart, 0);
      });
    },

    getSelectedRows() {
      const selectionStart = this.$refs.editor.selectionStart;
      const selectionEnd = this.$refs.editor.selectionEnd;

      let firstRowStart = selectionStart;
      let prevChar = this.input[firstRowStart - 1];
      while (firstRowStart > 0 && prevChar !== '\n') {
        firstRowStart--;
        prevChar = this.input[firstRowStart - 1];
      }

      let lastRowEnd = selectionEnd;
      let currentChar = this.input[lastRowEnd];
      while (lastRowEnd < this.input.length && currentChar !== '\n') {
        lastRowEnd++;
        currentChar = this.input[lastRowEnd];
      }

      const currentText = this.input.substring(firstRowStart, lastRowEnd);
      const rows = currentText.split('\n');

      const selectedRows = {
        start: firstRowStart,
        end: lastRowEnd,
        rows: [],
      };

      for (let i = 0; i < rows.length; i++) {
        let row = rows[i];
        if (i < (rows.length - 1)) {
          row += '\n';
        }
        selectedRows.rows.push(row);
      }

      return selectedRows;
    },

    handleTab(e) {
      const selectionStart = this.$refs.editor.selectionStart;
      const selectionEnd = this.$refs.editor.selectionEnd;
      const selectedRows = this.getSelectedRows();
      const spaces = ' '.repeat(this.tabSize);

      const getAmountToRemove = (text) => {
        const match = text.match(/^( +)([\s\S]*)/);
        let toRemove = 0;
        if (match) {
          toRemove = Math.min(match[1].length, this.tabSize);
        }

        return toRemove;
      };

      if (selectedRows.rows.length === 1) {
        // Insert a normal tab at the current selection.
        if (!e.shiftKey) {
          this.input = this.input.substring(0, selectionStart) + spaces + this.input.substring(selectionEnd);
          this.selectRange(selectionStart + spaces.length);
        // Unindent the current line.
        } else {
          const toRemove = getAmountToRemove(selectedRows.rows[0]);
          this.input = this.input.substring(0, selectedRows.start)
                     + this.input.substring(selectedRows.start + toRemove);
          this.selectRange(Math.max(selectionStart - toRemove, selectedRows.start));
        }
      } else {
        const endText = this.input.substring(selectedRows.end);
        this.input = this.input.substring(0, selectedRows.start);

        // Indent all selected lines.
        if (!e.shiftKey) {
          for (const row of selectedRows.rows) {
            this.input += spaces + row;
          }

          this.input += endText;
          this.selectRange(selectionStart + spaces.length, selectionEnd + (selectedRows.rows.length * spaces.length));
        // Unindent all selected lines.
        } else {
          let toRemoveFirst = 0;
          let toRemoveTotal = 0;

          for (let i = 0; i < selectedRows.rows.length; i++) {
            const toRemove = getAmountToRemove(selectedRows.rows[i]);
            if (i === 0) {
              toRemoveFirst = toRemove;
            }

            this.input += selectedRows.rows[i].substring(toRemove);
            toRemoveTotal += toRemove;
          }

          this.input += endText;
          this.selectRange(Math.max(selectionStart - toRemoveFirst, selectedRows.start), selectionEnd - toRemoveTotal);
        }
      }
    },

    handleEnter() {
      const selectionStart = this.$refs.editor.selectionStart;
      const selectionEnd = this.$refs.editor.selectionEnd;
      const selectedRows = this.getSelectedRows();

      let insertText = '\n';
      // Handle unordered and ordered lists.
      const match = selectedRows.rows[0].match(/^( *)(\* |[0-9]+\. )([\s\S]*)/);
      if (match) {
        if (match[2].includes('*')) {
          insertText += `${match[1]}* `;
        } else {
          insertText += `${match[1]}${Number.parseInt(match[2], 10) + 1}. `;
        }
      // Handle spaces at the beginning.
      } else {
        const match = selectedRows.rows[0].match(/^( +)([\s\S]*)/);
        if (match) {
          insertText += match[1];
        }
      }

      this.input = this.input.substring(0, selectionStart) + insertText + this.input.substring(selectionEnd);
      this.selectRange(selectionStart + insertText.length);
    },

    toggleBlock(startChars, endChars) {
      const selectionStart = this.$refs.editor.selectionStart;
      const selectionEnd = this.$refs.editor.selectionEnd;
      let removeBlock = false;
      let newSelectionStart = selectionStart + startChars.length;
      let newSelectionEnd = selectionEnd + endChars.length;

      if (selectionStart >= startChars.length && selectionEnd <= this.input.length - endChars.length) {
        const textBlock = this.input.substring(selectionStart - startChars.length, selectionEnd + endChars.length);

        let regexStart = '';
        let regexEnd = '';
        for (const char of startChars) {
          regexStart += `\\${char}`;
        }
        for (const char of endChars) {
          regexEnd += `\\${char}`;
        }
        const regex = new RegExp(`^${regexStart}[\\s\\S]*${regexEnd}$`);

        if (regex.test(textBlock)) {
          this.input = this.input.substring(0, selectionStart - startChars.length)
                     + this.input.substring(selectionStart, selectionEnd)
                     + this.input.substring(selectionEnd + endChars.length, this.input.length);
          removeBlock = true;
          newSelectionStart = selectionStart - startChars.length;
          newSelectionEnd = selectionEnd - endChars.length;
        }
      }

      if (!removeBlock) {
        this.input = this.input.substring(0, selectionStart)
                   + startChars
                   + this.input.substring(selectionStart, selectionEnd)
                   + endChars
                   + this.input.substring(selectionEnd, this.input.length);
      }

      this.selectRange(newSelectionStart, newSelectionEnd);
    },

    togglePrefix(toggleFunction) {
      const selectionStart = this.$refs.editor.selectionStart;
      const selectionEnd = this.$refs.editor.selectionEnd;
      const selectedRows = this.getSelectedRows();
      const endText = this.input.substring(selectedRows.end);

      this.input = this.input.substring(0, selectedRows.start);

      const newSelections = toggleFunction(selectedRows, selectionStart, selectionEnd);

      this.input += endText;

      this.selectRange(Math.max(newSelections.start, selectedRows.start), newSelections.end);
    },

    insertText(text) {
      const selectionEnd = this.$refs.editor.selectionEnd;
      this.input = this.input.substring(0, selectionEnd) + text + this.input.substring(selectionEnd);
      this.selectRange(selectionEnd + text.length);
    },

    toggleHeading() {
      this.togglePrefix((selectedRows, selectionStart, selectionEnd) => {
        let start = selectionStart;
        let end = selectionEnd;

        for (let i = 0; i < selectedRows.rows.length; i++) {
          if ((/^#{1,5} [\s\S]*/).test(selectedRows.rows[i])) {
            this.input += `#${selectedRows.rows[i]}`;
            end += 1;
            if (i === 0) {
              start += 1;
            }
          } else if ((/^#{6} [\s\S]*/).test(selectedRows.rows[i])) {
            this.input += selectedRows.rows[i].substring(7);
            end -= 7;
            if (i === 0) {
              start -= 7;
            }
          } else {
            this.input += `# ${selectedRows.rows[i]}`;
            end += 2;
            if (i === 0) {
              start += 2;
            }
          }
        }

        return {start, end};
      });
    },

    toggleBold() {
      this.toggleBlock('**', '**');
    },

    toggleItalic() {
      this.toggleBlock('*', '*');
    },

    toggleStrikethrough() {
      this.toggleBlock('~~', '~~');
    },

    toggleSuperscript() {
      this.toggleBlock('^', '^');
    },

    toggleSubscript() {
      this.toggleBlock('~', '~');
    },

    toggleCode() {
      const selectedRows = this.getSelectedRows();
      if (selectedRows.rows.length === 1) {
        this.toggleBlock('`', '`');
      } else {
        this.toggleBlock('```\n', '\n```');
      }
    },

    toggleMath() {
      const selectedRows = this.getSelectedRows();
      if (selectedRows.rows.length === 1) {
        this.toggleBlock('$', '$');
      } else {
        this.toggleBlock('$$\n', '\n$$');
      }
    },

    toggleUnorderedList() {
      this.togglePrefix((selectedRows, selectionStart, selectionEnd) => {
        let start = selectionStart;
        let end = selectionEnd;

        for (let i = 0; i < selectedRows.rows.length; i++) {
          const match = selectedRows.rows[i].match(/^( *)(\* )([\s\S]*)/);
          if (match) {
            this.input += match[1] + match[3];
            end -= 2;
            if (i === 0) {
              start -= 2;
            }
          } else {
            const match = selectedRows.rows[i].match(/^( *)([\s\S]*)/);
            if (match[2] === '') {
              this.input += `* ${match[1]}`;
            } else {
              this.input += `${match[1]}* ${match[2]}`;
            }
            end += 2;
            if (i === 0) {
              start += 2;
            }
          }
        }

        return {start, end};
      });
    },

    toggleOrderedList() {
      this.togglePrefix((selectedRows, selectionStart, selectionEnd) => {
        let start = selectionStart;
        let end = selectionEnd;

        for (let i = 0; i < selectedRows.rows.length; i++) {
          const match = selectedRows.rows[i].match(/^( *)([0-9]+\. )([\s\S]*)/);
          if (match) {
            this.input += match[1] + match[3];
            end -= match[2].length;
            if (i === 0) {
              start -= match[2].length;
            }
          } else {
            const match = selectedRows.rows[i].match(/^( *)([\s\S]*)/);
            const index = `${i + 1}. `;
            this.input += match[1] + index + match[2];
            end += index.length;
            if (i === 0) {
              start += index.length;
            }
          }
        }

        return {start, end};
      });
    },

    insertHorizontalRule() {
      const rule = '\n\n---\n\n';
      this.insertText(rule);
    },

    insertTable() {
      let column = $t('Column');
      let text = $t('Text');

      const colSize = Math.max(column.length + 2, text.length);
      const divider = '-'.repeat(colSize);

      column += ' '.repeat(Math.max(0, colSize - (column.length + 2)));
      text += ' '.repeat(Math.max(0, colSize - text.length));

      const table = `\n\n| ${column} 1 | ${column} 2 | ${column} 3 |\n`
                  + `| ${divider} | ${divider} | ${divider} |\n`
                  + `| ${text} | ${text} | ${text} |\n\n`;
      this.insertText(table);
    },

    insertLink(toggleSelection) {
      if (toggleSelection && this.linkEndpoint) {
        this.imageSelectionActive = false;
        this.linkSelectionActive = !this.linkSelectionActive;
      } else {
        const link = `[${$t('Link text')}](https://)`;
        this.insertText(link);
      }
    },

    selectLink(file) {
      const link = `[${file.text}](${file.view_endpoint})`;
      this.insertText(link);
    },

    insertImage() {
      if (this.imageEndpoint) {
        this.linkSelectionActive = false;
        this.imageSelectionActive = !this.imageSelectionActive;
      } else {
        const image = `![${$t('Alternative text')}](https://)`;
        this.insertText(image);
      }
    },

    selectImage(file) {
      const imageText = `![${file.text}](${file.preview_endpoint})`;
      this.insertText(imageText);
    },

    getCheckpointData() {
      return {
        input: this.input,
        selectionStart: this.$refs.editor.selectionStart,
        selectionEnd: this.$refs.editor.selectionEnd,
      };
    },

    verifyCheckpointData(currentData, newData) {
      if (currentData.input !== newData.input) {
        // Dispatch a native change event every time a checkpoint is created.
        this.$el.dispatchEvent(new Event('change', {bubbles: true}));
        return true;
      }
      return false;
    },

    restoreCheckpointData(data) {
      this.input = data.input;
      this.selectRange(data.selectionStart, data.selectionEnd);
    },

    undo() {
      // Force a checkpoint of the current state before undoing.
      window.clearTimeout(this.inputTimeoutHandle);
      this.saveCheckpoint();

      if (this.undoable) {
        this.undoStackIndex--;
        this.restoreCheckpointData(this.undoStack[this.undoStackIndex]);
      }
    },

    keydownHandler(e) {
      if (e.ctrlKey) {
        for (const button of this.toolbar) {
          if (button.shortcut === e.key) {
            e.preventDefault();

            if (!this.previewActive) {
              button.handler();
            }
            return;
          }
        }

        switch (e.key) {
        case 'p':
          e.preventDefault();
          this.previewActive = !this.previewActive;

          this.$nextTick(() => {
            if (!this.previewActive) {
              this.$refs.editor.focus();
            } else {
              this.$refs.preview.focus();
            }
          });
          break;
        case 'z':
          e.preventDefault();
          this.undo();
          break;
        case 'y':
          e.preventDefault();
          this.redo();
          break;
        default: // Do nothing.
        }
      }
    },
  },
  mounted() {
    if (this.autosize && this.$refs.editor.scrollHeight > this.$refs.editor.clientHeight) {
      this.$refs.editor.style.height = `${Math.min(window.innerHeight - 150, this.$refs.editor.scrollHeight + 5)}px`;
    }

    this.saveCheckpoint();
    this.$el.addEventListener('keydown', this.keydownHandler);
  },
  beforeDestroy() {
    this.$el.removeEventListener('keydown', this.keydownHandler);
  },
};
</script>
