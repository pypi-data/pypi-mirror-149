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
  <span v-html="result"></span>
</template>

<script>
import markdownit from 'markdown-it';
import markdownitSub from 'markdown-it-sub';
import markdownitSup from 'markdown-it-sup';
import markdownitTexmath from 'markdown-it-texmath';

export default {
  data() {
    return {
      renderer: null,
      result: '',
    };
  },
  props: {
    input: String,
  },
  watch: {
    input() {
      this.render();
    },
  },
  methods: {
    render() {
      this.result = this.renderer.render(this.input);
    },
    renderToken(token, attrs = [], closingTag = '>') {
      let result = `<${token.tag}`;
      const tokenAttrs = token.attrs === null ? [] : token.attrs;
      [...tokenAttrs, ...attrs].forEach((attr) => result += ` ${attr[0]}="${attr[1]}"`);
      return result + closingTag;
    },
  },
  mounted() {
    this.renderer = markdownit()
      .use(markdownitSub)
      .use(markdownitSup)
      .use(markdownitTexmath, {outerSpace: true, katexOptions: {output: 'html', maxSize: 10, maxExpand: 100}});

    // Customize some of the rendering rules.
    this.renderer.renderer.rules.heading_open = (tokens, idx) => {
      const sizes = [1.7, 1.5, 1.4, 1.3, 1.2, 1.1];
      const level = tokens[idx].markup.length - 1;
      return this.renderToken(tokens[idx], [['class', 'font-weight-bold'], ['style', `font-size: ${sizes[level]}rem`]]);
    };
    this.renderer.renderer.rules.image = (tokens, idx) => {
      return this.renderToken(tokens[idx], [['class', 'img-fluid']], '/>');
    };
    this.renderer.renderer.rules.link_open = (tokens, idx) => {
      return this.renderToken(tokens[idx], [['style', 'color: #1e8cbe']]);
    };
    this.renderer.renderer.rules.table_open = (tokens, idx) => {
      return this.renderToken(tokens[idx], [['class', 'table table-sm table-bordered table-hover']]);
    };

    this.render();
  },
};
</script>
