<!-- Copyright 2021 Karlsruhe Institute of Technology
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
  <div class="card" ref="container">
    <div class="toolbar mt-1 mr-1">
      <i class="fa-solid fa-circle-notch fa-spin text-muted mr-2" v-if="loading"></i>
      <button type="button"
              :title="$t('Decrease link depth')"
              :class="toolbarBtnClasses"
              :disabled="depth <= 1"
              @click="depth--">
        <i class="fa-solid fa-angle-left"></i>
      </button>
      <strong class="text-muted">{{ $t('Link depth:') }} {{ depth }}</strong>
      <button type="button"
              :title="$t('Increase link depth')"
              :class="toolbarBtnClasses"
              :disabled="depth >= 3"
              @click="depth++">
        <i class="fa-solid fa-angle-right"></i>
      </button>
      <button type="button"
              :title="$t('Toggle forces')"
              :class="toolbarBtnClasses + (forceDisabled ? ' border-active' : '')"
              @click="forceDisabled = !forceDisabled">
        <i class="fa-solid fa-thumbtack"></i>
      </button>
      <button type="button" :title="$t('Download graph')" :class="toolbarBtnClasses" @click="downloadGraph">
        <i class="fa-solid fa-download"></i>
      </button>
      <button type="button" :title="$t('Reset view')" :class="toolbarBtnClasses" @click="resetView">
        <i class="fa-solid fa-eye"></i>
      </button>
      <button type="button" :title="$t('Toggle fullscreen')" :class="toolbarBtnClasses" @click="toggleFullscreen">
        <i class="fa-solid fa-expand"></i>
      </button>
    </div>
    <div ref="svgContainer"></div>
  </div>
</template>

<style scoped>
.border-active {
  border: 1px solid #ced4da;
}

.toolbar {
  max-width: 60%;
  position: absolute;
  right: 0;
  z-index: 1;
}
</style>

<script>
import * as d3 from 'd3';

export default {
  data() {
    return {
      suffix: kadi.utils.randomAlnum(), // To create unique IDs.
      svg: null,
      legendContainer: null,
      graphContainer: null,
      zoom: null,
      simulation: null,
      nodes: [],
      links: [],
      excludedTypes: [],
      width: 0,
      height: 0,
      depth: 1,
      manyBodyStrength: -2000,
      linkStrength: 0.25,
      forceDisabled: false,
      loading: true,
      updateTimeoutHandle: null,
      colors: {
        link: '#c9c9c9',
        linkHover: '#8a8a8a',
      },
    };
  },
  props: {
    endpoint: String,
    startRecord: Number,
    direction: {
      type: String,
      default: '',
    },
    filter: {
      type: String,
      default: '',
    },
    isRendered: {
      type: Boolean,
      default: true,
    },
  },
  computed: {
    toolbarBtnClasses() {
      return 'btn btn-link text-muted';
    },
  },
  watch: {
    depth() {
      this.loading = true;

      window.clearTimeout(this.updateTimeoutHandle);
      this.updateTimeoutHandle = window.setTimeout(() => {
        this.updateData().then(() => this.forceDisabled = false);
      }, 500);
    },
    forceDisabled() {
      if (this.forceDisabled) {
        this.simulation.force('charge').strength(0);
        this.simulation.force('link').strength(0);
      } else {
        this.simulation.force('charge').strength(this.manyBodyStrength);
        this.simulation.force('link').strength(this.linkStrength);
        this.simulation.alpha(0.5).restart();
      }
    },
    direction() {
      this.updateData();
    },
    filter() {
      this.filterNodes();
    },
    isRendered() {
      this.resizeView(false);
    },
  },
  methods: {
    isFullscreen() {
      return document.fullScreen || document.mozFullScreen || document.webkitIsFullScreen;
    },
    isNodeVisible(id) {
      return this.graphContainer.select(`#node-${id}-${this.suffix}`).style('visibility') === 'visible';
    },
    getStartNode() {
      return this.nodes.find((node) => node.id === this.startRecord);
    },
    getTypeColor(scale, type, darker = false) {
      const color = type === null ? 'grey' : scale(type);
      return darker ? d3.color(color).darker(1) : color;
    },
    b64EncodeUnicode(str) {
      // See also: https://developer.mozilla.org/en-US/docs/Glossary/Base64
      return window.btoa(window.encodeURIComponent(str).replace(/%([0-9A-F]{2})/g, function(match, p1) {
        return String.fromCharCode(`0x${p1}`);
      }));
    },
    downloadGraph() {
      const svg = this.svg.node().cloneNode(true);
      const graph = svg.getElementById('graph');

      // Use the existing containers for this, as the element needs to be part of the DOM to determine the bounding box.
      const graphBBox = this.graphContainer.node().getBBox();
      const legendBBox = this.legendContainer.node().getBBox();
      // Additional margin used on all sites for the graph.
      const graphMargin = 20;
      // Additional margin used between the legend and the graph.
      const legendMargin = 10;

      // Specify the size of the SVG.
      svg.setAttribute('width', graphBBox.width + (graphMargin * 2) + legendBBox.width + legendMargin);
      svg.setAttribute('height', Math.max(graphBBox.height + (graphMargin * 2), legendBBox.height));

      // Translate the graph so it is completely visible inside the SVG.
      const translateX = -graphBBox.x + graphMargin + legendBBox.width + legendMargin;
      const translateY = -graphBBox.y + graphMargin;
      graph.setAttribute('transform', `translate(${translateX},${translateY}) scale(1)`);

      // Convert and download the SVG.
      const xmlString = `<?xml version="1.0" encoding="utf-8"?>${new XMLSerializer().serializeToString(svg)}`;
      const svgData = `data:image/svg+xml;base64,${this.b64EncodeUnicode(xmlString)}`;
      const startNode = this.getStartNode();
      const filename = `${startNode ? startNode.identifier_full : 'links'}.svg`;

      const a = document.createElement('a');
      a.href = svgData;
      a.download = filename;

      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    },
    resetView() {
      const startNode = this.getStartNode();

      if (this.forceDisabled) {
        // Translate so that the current position of the start node is at the center.
        this.zoom.translateTo(
          this.svg,
          startNode ? startNode.x : 0,
          startNode ? startNode.y : 0,
          [this.width * 0.5, this.height * 0.5],
        );
      } else {
        // Reset the position of the start node to the origin and then translate so that the origin is at the center.
        if (startNode) {
          startNode.fx = 0;
          startNode.fy = 0;
        }
        this.zoom.translateTo(this.svg, 0, 0, [this.width * 0.5, this.height * 0.5]);
      }

      this.zoom.scaleTo(this.svg, 1);
      this.simulation.alpha(0.5).restart();
    },
    toggleFullscreen() {
      if (this.isFullscreen()) {
        document.exitFullscreen();
      } else {
        this.$refs.container.requestFullscreen();
      }
    },
    resizeView(resetView = true) {
      // In case the component is not marked as rendered from the outside we do not attempt to resize it.
      if (!this.isRendered) {
        return;
      }

      // Take the border width into account as well.
      this.width = this.$refs.container.getBoundingClientRect().width - 2;
      this.height = Math.round(window.innerHeight / window.innerWidth * this.width);

      if (this.isFullscreen()) {
        this.$refs.svgContainer.style.height = '100vh';
        this.$refs.container.style.borderRadius = '0';
      } else {
        this.$refs.svgContainer.style.height = `${this.height}px`;
        this.$refs.container.style.borderRadius = '0.25rem';
      }

      this.svg.attr('width', this.width).attr('height', this.height);

      if (resetView) {
        this.resetView();
      }
    },
    filterNodes() {
      this.graphContainer.selectAll(`.node-${this.suffix}`).each((d, i, nodes) => {
        const node = d3.select(nodes[i]);

        if (this.excludedTypes.includes(d.type)) {
          node.style('visibility', 'hidden');
        } else {
          if (d.identifier.includes(this.filter.trim())) {
            node.style('visibility', 'visible');
          } else {
            node.style('visibility', 'hidden');
          }
        }
      });

      this.graphContainer.selectAll(`.link-${this.suffix}`).each((d, i, nodes) => {
        const link = d3.select(nodes[i]);

        if (this.isNodeVisible(d.source.id) && this.isNodeVisible(d.target.id)) {
          link.style('visibility', 'visible');
        } else {
          link.style('visibility', 'hidden');
        }
      });
    },
    toggleType(type) {
      let opacity = 0;

      if (this.excludedTypes.includes(type)) {
        kadi.utils.removeFromList(this.excludedTypes, type);
        opacity = 1;
      } else {
        this.excludedTypes.push(type);
        opacity = 0.3;
      }

      this.legendContainer.selectAll('circle').filter((d) => d === type).style('opacity', opacity);
      this.filterNodes();
    },
    getBezierPoints(d) {
      const dx = d.target.x - d.source.x;
      const dy = d.target.y - d.source.y;
      return {
        x1: d.source.x,
        y1: d.source.y,
        x2: d.source.x + (dx / 2) + (dy / 5 * d.link_index),
        y2: d.source.y + (dy / 2) - (dx / 5 * d.link_index),
        x3: d.target.x,
        y3: d.target.y,
      };
    },
    quadraticBezierCurve(d) {
      const pts = this.getBezierPoints(d);
      return `M ${pts.x1},${pts.y1} Q ${pts.x2} ${pts.y2} ${pts.x3} ${pts.y3}`;
    },
    linkLabelTransformation(d) {
      const pts = this.getBezierPoints(d);

      // Calculate a good position for the text along the link path.
      const t = 0.5;
      const posX = pts.x2 + (((1 - t) ** 2) * (pts.x1 - pts.x2)) + ((t ** 2) * (pts.x3 - pts.x2));
      const posY = pts.y2 + (((1 - t) ** 2) * (pts.y1 - pts.y2)) + ((t ** 2) * (pts.y3 - pts.y2));

      // Calculate the angle of the path at this position to rotate the text properly.
      const slopeX = (2 * (1 - t) * (pts.x2 - pts.x1)) + (2 * t * (pts.x3 - pts.x2));
      const slopeY = (2 * (1 - t) * (pts.y2 - pts.y1)) + (2 * t * (pts.y3 - pts.y2));

      let rotation = Math.atan2(slopeY, slopeX) * (180 / Math.PI);
      rotation = pts.x1 > pts.x3 ? rotation - 180 : rotation;

      // Calculate an additional margin between the path and the text based on the rotation.
      const margin = pts.x1 > pts.x3 ? -15 : 5;
      const marginX = Math.sin((rotation / 180) * Math.PI) * margin;
      const marginY = Math.cos((rotation / 180) * Math.PI) * margin;

      return `translate(${posX + marginX} ${posY - marginY}) rotate(${rotation})`;
    },
    drag() {
      return d3.drag()
        .on('start', (e) => {
          if (!e.active) {
            this.simulation.alphaTarget(0.5).restart();
          }
          e.subject.fx = e.subject.x;
          e.subject.fy = e.subject.y;
        })
        .on('drag', (e) => {
          e.subject.fx = e.x;
          e.subject.fy = e.y;
        })
        .on('end', (e) => {
          if (!e.active) {
            this.simulation.alphaTarget(0);
          }
          if (e.subject.id !== this.startRecord) {
            e.subject.fx = null;
            e.subject.fy = null;
          }
        });
    },
    drawGraph() {
      const typesMap = new Map();
      this.nodes.forEach((node) => {
        const typeMeta = {
          count: typesMap.has(node.type) ? typesMap.get(node.type).count + 1 : 1,
          type_full: node.type_full,
        };
        typesMap.set(node.type, typeMeta);
      });

      const typesArray = Array.from(typesMap.keys());
      typesArray.sort((a, b) => (a === null) - (b === null) || Number(a > b) || -(a < b));

      const colorScale = d3.scaleOrdinal(d3.schemePaired).domain(typesArray);

      // Draw the legend.
      const legendGroup = this.legendContainer
        .selectAll()
        .data(typesArray)
        .enter()
        .append('g');

      const radius = 9;
      const padding = 8;

      legendGroup
        .append('circle')
        .attr('r', radius)
        .attr('cx', radius + padding)
        .attr('cy', (d, i) => ((i + 1) * radius) + (i * (radius + padding)) + padding)
        .style('fill', (d) => this.getTypeColor(colorScale, d))
        .style('stroke', (d) => this.getTypeColor(colorScale, d, true))
        .style('cursor', 'pointer')
        .on('click', (e) => this.toggleType(e.target.__data__));

      legendGroup
        .append('text')
        .text((d) => `${d || 'No type'} (${typesMap.get(d).count})`)
        .attr('x', (radius * 3) + padding)
        .attr('y', (d, i) => ((i + 1) * radius) + (i * (radius + padding)) + padding)
        .attr('dy', 5)
        .style('font-family', 'sans-serif')
        .style('font-size', '90%')
        .style('font-style', (d) => (d === null ? 'italic' : 'normal'))
        .style('fill', (d) => this.getTypeColor(colorScale, d, true))
        .style('cursor', 'default')
        .filter((d) => d !== null)
        .append('title')
        .text((d) => typesMap.get(d).type_full);

      // Draw the links.
      const linkGroup = this.graphContainer
        .selectAll()
        .data(this.links)
        .enter()
        .append('g')
        .attr('class', `link-${this.suffix}`);

      linkGroup
        .append('path')
        .attr('class', `link-path-${this.suffix}`)
        .attr('fill', 'none')
        .attr('stroke', this.colors.link)
        .attr('stroke-width', 3)
        .attr('marker-end', `url(#arrowhead-${this.suffix})`)
        .on('mouseover', (e) => {
          const link = d3.select(e.target);

          link.style('stroke', this.colors.linkHover);
          link.style('marker-end', `url(#arrowhead-hover-${this.suffix})`);
        })
        .on('mouseout', (e) => {
          const link = d3.select(e.target);

          link.style('stroke', this.colors.link);
          link.style('marker-end', `url(#arrowhead-${this.suffix})`);
        });

      linkGroup
        .append('text')
        .text((d) => d.name)
        .attr('class', `link-label-${this.suffix}`)
        .style('font-family', 'sans-serif')
        .style('font-size', '85%')
        .style('text-anchor', 'middle')
        .style('cursor', 'default')
        .append('title')
        .text((d) => d.name_full);

      // Draw the nodes.
      const nodeGroup = this.graphContainer
        .selectAll()
        .data(this.nodes)
        .enter()
        .append('g')
        .attr('id', (d) => `node-${d.id}-${this.suffix}`)
        .attr('class', `node-${this.suffix}`)
        .call(this.drag());

      nodeGroup
        .append('circle')
        .attr('r', 15)
        .style('fill', (d) => this.getTypeColor(colorScale, d.type))
        .style('stroke', (d) => this.getTypeColor(colorScale, d.type, true))
        .style('stroke-width', 5)
        .style('cursor', 'pointer')
        .on('mouseover', (e, nodeData) => {
          this.graphContainer.selectAll(`.link-path-${this.suffix}`).each((linkData, i, nodes) => {
            const path = d3.select(nodes[i]);

            if (linkData.source.id === nodeData.id || linkData.target.id === nodeData.id) {
              path.style('stroke', this.colors.linkHover);
              path.style('marker-end', `url(#arrowhead-hover-${this.suffix})`);
            }
          });
        })
        .on('mouseout', () => {
          this.graphContainer.selectAll(`.link-path-${this.suffix}`).each((d, i, nodes) => {
            const path = d3.select(nodes[i]);

            path.style('stroke', this.colors.link);
            path.style('marker-end', `url(#arrowhead-${this.suffix})`);
          });
        })
        .filter((d) => d.id !== this.startRecord)
        .style('stroke-width', 2);

      nodeGroup
        .append('a')
        .attr('href', (d) => d.url)
        .append('text')
        .text((d) => `@${d.identifier}`)
        .attr('dy', 30)
        .style('font-family', 'sans-serif')
        .style('font-weight', 'bold')
        .style('text-anchor', 'middle')
        .on('mouseover', (e) => d3.select(e.target).style('fill', '#2c3e50').style('font-size', '115%'))
        .on('mouseout', (e) => d3.select(e.target).style('fill', 'black').style('font-size', '100%'))
        .append('title')
        .text((d) => d.identifier_full);

      nodeGroup
        .filter((d) => d.type !== null)
        .append('text')
        .text((d) => d.type)
        .attr('dy', 45)
        .style('font-family', 'sans-serif')
        .style('font-size', '70%')
        .style('text-anchor', 'middle')
        .style('cursor', 'default')
        .append('title')
        .text((d) => d.type_full);

      // Initialize and restart the simulation.
      this.simulation.nodes(this.nodes);
      this.simulation.force('link').links(this.links);
      this.simulation.alpha(1).restart();
    },
    updateData() {
      return axios.get(this.endpoint, {params: {depth: this.depth, direction: this.direction}})
        .then((response) => {
          const prevStartNode = this.getStartNode();

          this.nodes = response.data.nodes;
          this.links = response.data.links;

          // Give the start node a fixed position based on its previous position or use the origin as fallback.
          const startNode = this.getStartNode();
          if (startNode) {
            startNode.fx = prevStartNode ? prevStartNode.x : 0;
            startNode.fy = prevStartNode ? prevStartNode.y : 0;
          }

          this.graphContainer.selectAll('*').remove();
          this.legendContainer.selectAll('*').remove();

          this.drawGraph();

          this.excludedTypes = [];
          this.filterNodes();
        })
        .catch((error) => kadi.alert($t('Error loading record links.'), {request: error.request}))
        .finally(() => this.loading = false);
    },
  },
  mounted() {
    this.svg = d3.select(this.$refs.svgContainer).append('svg');
    this.graphContainer = this.svg.append('g').attr('id', 'graph');
    this.legendContainer = this.svg.append('g').attr('id', 'legend');

    // Definition for the arrow heads of the links.
    const defs = this.svg.append('defs');

    const _appendMarker = (id, color) => {
      defs.append('marker')
        .attr('id', id)
        .attr('viewBox', '0 0 10 10')
        .attr('refX', 19)
        .attr('refY', 4.5)
        .attr('orient', 'auto')
        .attr('markerWidth', 5)
        .attr('markerHeight', 5)
        .append('path')
        .attr('d', 'M 0 0 L 10 5 L 0 10 z')
        .style('fill', color);
    };

    _appendMarker(`arrowhead-${this.suffix}`, this.colors.link);
    _appendMarker(`arrowhead-hover-${this.suffix}`, this.colors.linkHover);

    this.zoom = d3.zoom().on('zoom', (e) => this.graphContainer.attr('transform', e.transform));
    this.svg.call(this.zoom).on('dblclick.zoom', null);

    const manyBodyForce = d3.forceManyBody().strength(this.manyBodyStrength);
    const linkForce = d3.forceLink()
      .id((d) => d.id)
      .distance((d) => (d.link_length * 7) + 200)
      .strength(this.linkStrength);

    this.simulation = d3.forceSimulation()
      .velocityDecay(0.15)
      .force('charge', manyBodyForce)
      .force('link', linkForce)
      .on('tick', () => {
        this.graphContainer
          .selectAll(`.node-${this.suffix}`)
          .attr('transform', (d) => `translate(${d.x} ${d.y})`);
        this.graphContainer
          .selectAll(`.link-path-${this.suffix}`)
          .attr('d', (d) => this.quadraticBezierCurve(d));
        this.graphContainer
          .selectAll(`.link-label-${this.suffix}`)
          .attr('transform', (d) => this.linkLabelTransformation(d));
      });

    this.resizeView(false);
    this.updateData().then(() => this.resetView());

    window.addEventListener('resize', this.resizeView);
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.resizeView);
  },
};
</script>
