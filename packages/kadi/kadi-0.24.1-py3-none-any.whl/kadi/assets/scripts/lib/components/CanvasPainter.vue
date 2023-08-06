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
    <div ref="container">
      <div class="card toolbar" ref="toolbar">
        <div class="card-body px-0 py-1">
          <button type="button"
                  :title="$t('Pen')"
                  :class="toolbarBtnClasses + enabledToolClasses('pen')"
                  @click="tool = 'pen'">
            <i class="fa-solid fa-pencil"></i>
          </button>
          <button type="button"
                  :title="$t('Eraser')"
                  :class="toolbarBtnClasses + enabledToolClasses('eraser')"
                  @click="tool = 'eraser'">
            <i class="fa-solid fa-eraser"></i>
          </button>
          <button type="button"
                  :title="$t('Color picker')"
                  :class="toolbarBtnClasses + enabledToolClasses('colorpicker')"
                  @click="tool = 'colorpicker'">
            <i class="fa-solid fa-eye-dropper"></i>
          </button>
          <button type="button"
                  :title="$t('Move canvas')"
                  :class="toolbarBtnClasses + enabledToolClasses('move')"
                  @click="tool = 'move'">
            <i class="fa-solid fa-up-down-left-right"></i>
          </button>
          <button type="button" :title="$t('Reset view')" :class="toolbarBtnClasses" @click="resetView">
            <i class="fa-solid fa-eye"></i>
          </button>
          <button type="button" :title="$t('Toggle fullscreen')" :class="toolbarBtnClasses" @click="toggleFullscreen">
            <i class="fa-solid fa-expand"></i>
          </button>
          <button type="button" :title="$t('Reset canvas')" :class="toolbarBtnClasses" @click="resetCanvas">
            <i class="fa-solid fa-broom"></i>
          </button>
          <span class="color-picker" :title="$t('Color')" :style="{'background-color': color}" @click="pickColor">
          </span>
          <input class="color-input" type="color" v-model="color" ref="colorInput">
          <span class="d-inline-block mr-2">
            <input type="range"
                   class="stroke-width-input"
                   min="1"
                   max="31"
                   step="2"
                   :title="$t('Stroke width')"
                   v-model.number="strokeWidth">
            <span class="stroke-width-display-container">
              <span class="stroke-width-display"
                    :style="{'width': strokeWidth + 'px', 'height': strokeWidth + 'px'}">
              </span>
            </span>
          </span>
          <span class="d-inline-block my-1">
            <input class="form-control form-control-sm size-input"
                   :title="$t('Width')"
                   v-model.number="width"
                   @change="updateCanvasSize">
            <i class="fa-solid fa-xmark fa-sm text-muted"></i>
            <input class="form-control form-control-sm size-input"
                   :title="$t('Height')"
                   v-model.number="height"
                   @change="updateCanvasSize">
          </span>
          <button type="button" :title="$t('Reset canvas size')" :class="toolbarBtnClasses" @click="resetCanvasSize">
            <i class="fa-solid fa-rotate-left"></i>
          </button>
        </div>
      </div>
      <div ref="canvasContainer">
        <canvas class="canvas"
                @mousedown="mouseDown"
                @mousemove="mouseMove"
                @mouseup="pointerUp"
                @mouseout="pointerUp"
                @touchstart.prevent="touchStart"
                @touchmove.prevent="touchMove"
                @touchend.prevent="pointerUp"
                @touchcancel.prevent="pointerUp"
                ref="canvas">
        </canvas>
      </div>
      <svg class="d-none" :height="strokeWidth" :width="strokeWidth" ref="cursorPen">
        <circle stroke-width="0px" :cx="strokeWidth / 2" :cy="strokeWidth / 2" :r="strokeWidth / 2" :fill="color">
        </circle>
      </svg>
      <svg class="d-none" :height="strokeWidth + 2" :width="strokeWidth + 2" ref="cursorEraser">
        <circle stroke="black"
                stroke-width="1px"
                fill="white"
                :cx="(strokeWidth / 2) + 1"
                :cy="(strokeWidth / 2) + 1"
                :r="strokeWidth / 2">
        </circle>
      </svg>
    </div>
    <slot :canvas="memCanvas"></slot>
  </div>
</template>

<style scoped>
.border-active {
  border: 1px solid #ced4da;
}

.canvas {
  border: 1px solid #ced4da;
}

.color-input {
  height: 0px;
  padding: 0px;
  visibility: hidden;
  width: 0px;
  -webkit-appearance: none;
}

.color-picker {
  background-color: black;
  border: 1px solid black;
  cursor: pointer;
  display: inline-block;
  height: 25px;
  margin-left: 15px;
  margin-right: 20px;
  vertical-align: middle;
  width: 25px;
}

.size-input {
  display: inline;
  margin-left: 5px;
  margin-right: 5px;
  width: 50px;
}

.stroke-width-display {
  background-color: black;
  border-radius: 50%;
  display: inline-block;
  vertical-align: middle;
}

.stroke-width-display-container {
  align-items: center;
  display: inline-flex;
  height: 30px;
  justify-content: center;
  margin-left: 10px;
  margin-right: 15px;
  vertical-align: middle;
  width: 30px;
}

.stroke-width-input {
  vertical-align: middle;
  width: 150px;
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
  margin-left: 5px;
  margin-right: 5px;
  width: 45px;
}
</style>

<script>
export default {
  data() {
    return {
      canvas: null, // Visible canvas.
      ctx: null, // 2D drawing context of the visible canvas.
      memCanvas: null, // Actual canvas.
      memCtx: null, // 2D drawing context of the actual canvas.
      currX: 0, // Current X coordinate of the mouse while the left mouse button is down.
      currY: 0, // Current Y coordinate of the mouse while the left mouse button is down.
      prevX: 0, // Previous X coordinate of the mouse while the left mouse button was down.
      prevY: 0, // Previous Y coordinate of the mouse while the left mouse button was down.
      originX: 0, // Current X coordinate of the origin of the visible canvas in relation to the actual canvas.
      originY: 0, // Current Y coordinate of the origin of the visible canvas in relation to the actual canvas.
      width: 0, // Current width of the actual canvas.
      height: 0, // Current height of the actual canvas.
      maxSize: 5000,
      tool: 'pen',
      color: '#000000',
      strokeWidth: 3,
      points: [],
      drawing: false,
      unsavedChanges_: false,
    };
  },
  props: {
    imageUrl: {
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
  },
  computed: {
    toolbarBtnClasses() {
      return 'btn btn-link text-primary toolbar-btn my-1';
    },
  },
  watch: {
    imageUrl() {
      this.loadImage(this.imageUrl);
    },
    unsavedChanges() {
      this.unsavedChanges_ = this.unsavedChanges;
    },
    unsavedChanges_() {
      this.$emit('unsaved-changes', this.unsavedChanges_);
    },
    isRendered() {
      this.resizeVisibleCanvas(false);
    },
    tool() {
      this.updateCursor();
    },
    color() {
      this.updateCursor();
    },
    strokeWidth() {
      this.updateCursor();
    },
    width() {
      if (this.width < 1 || window.isNaN(this.width)) {
        this.width = 1;
      } else if (this.width > this.maxSize) {
        this.width = this.maxSize;
      }
    },
    height() {
      if (this.height < 1 || window.isNaN(this.height)) {
        this.height = 1;
      } else if (this.height > this.maxSize) {
        this.height = this.maxSize;
      }
    },
  },
  methods: {
    resetView() {
      this.originX = -Math.round(Math.max(this.canvas.width - this.memCanvas.width, 0) / 2);
      this.originY = -Math.round(Math.max(this.canvas.height - this.memCanvas.height, 0) / 2);
      this.redrawVisibleCanvas();
    },

    toggleFullscreen() {
      if (this.isFullscreen()) {
        document.exitFullscreen();
      } else {
        this.$refs.container.requestFullscreen();
      }
    },

    resetCanvas() {
      if (!window.confirm($t('Are you sure you want to reset the canvas?'))) {
        return;
      }
      this.clearCanvas(true);
      this.unsavedChanges_ = false;
    },

    pickColor() {
      this.$refs.colorInput.click();
    },

    updateCanvasSize() {
      const imageData = this.memCtx.getImageData(0, 0, this.memCanvas.width, this.memCanvas.height);
      this.memCanvas.width = this.width;
      this.memCanvas.height = this.height;

      this.memCtx.fillStyle = 'white';
      this.memCtx.fillRect(0, 0, this.width, this.height);
      this.memCtx.putImageData(imageData, 0, 0);

      this.redrawVisibleCanvas();
      this.unsavedChanges_ = true;
    },

    enabledToolClasses(tool) {
      return this.tool === tool ? ' border-active' : '';
    },

    isFullscreen() {
      return document.fullScreen || document.mozFullScreen || document.webkitIsFullScreen;
    },

    updateCoordinates(x, y) {
      this.prevX = this.currX;
      this.prevY = this.currY;
      this.currX = x - this.canvas.getBoundingClientRect().left;
      this.currY = y - this.canvas.getBoundingClientRect().top;
    },

    updateCursor() {
      this.$nextTick(() => {
        let cursor = 'default';
        if (this.tool === 'pen' || this.tool === 'eraser') {
          const svg = this.tool === 'pen' ? this.$refs.cursorPen : this.$refs.cursorEraser;
          const data = window.btoa(new XMLSerializer().serializeToString(svg));
          cursor = `url("data:image/svg+xml;base64,${data}") ${this.strokeWidth / 2} ${this.strokeWidth / 2}, auto`;
        } else if (this.tool === 'move') {
          cursor = 'move';
        }
        this.$refs.canvasContainer.style.cursor = cursor;
      });
    },

    getCurrentPixelColor() {
      const data = this.ctx.getImageData(this.currX, this.currY, 1, 1).data;
      // eslint-disable-next-line no-bitwise
      return `#${(`000000${((data[0] << 16) | (data[1] << 8) | data[2]).toString(16)}`).slice(-6)}`;
    },

    loadImage(url) {
      const image = new Image();

      image.onload = () => {
        let width = image.width;
        if (width > this.maxSize) {
          width = this.maxSize;
        }

        let height = image.height;
        if (height > this.maxSize) {
          height = this.maxSize;
        }

        this.width = this.memCanvas.width = width;
        this.height = this.memCanvas.height = height;

        this.memCtx.fillStyle = 'white';
        this.memCtx.fillRect(0, 0, this.width, this.height);
        this.memCtx.drawImage(image, 0, 0);

        this.resetView();
      };
      image.onerror = () => kadi.alert($t('Error loading image.'));

      image.src = url;
    },

    clearCanvas(resize = false) {
      if (resize) {
        this.resizeVisibleCanvas();
        this.width = this.memCanvas.width = this.canvas.width;
        this.height = this.memCanvas.height = this.canvas.height;
      }

      this.memCtx.fillStyle = 'white';
      this.memCtx.fillRect(0, 0, this.memCanvas.width, this.memCanvas.height);
      this.resetView();
    },

    resetCanvasSize() {
      if (!window.confirm($t('Are you sure you want to reset the size of the canvas?'))) {
        return;
      }

      this.width = this.canvas.width;
      this.height = this.canvas.height;
      this.updateCanvasSize();
      this.resetView();
    },

    draw() {
      // Reset the visible canvas to its previous state before drawing the points again.
      this.redrawVisibleCanvas();
      this.points.push({x: this.currX, y: this.currY});
      this.drawPoints();
      this.drawLimits();
    },

    redrawVisibleCanvas() {
      this.ctx.drawImage(
        this.memCanvas,
        this.originX,
        this.originY,
        this.canvas.width,
        this.canvas.height,
        0,
        0,
        this.canvas.width,
        this.canvas.height,
      );
      this.drawLimits();
    },

    drawLimits() {
      const bottomEdge = this.memCanvas.height - this.originY;
      const rightEdge = this.memCanvas.width - this.originX;

      this.ctx.fillStyle = '#ced4da';
      this.ctx.fillRect(0, 0, -this.originX, this.canvas.height);
      this.ctx.fillRect(0, 0, this.canvas.width, -this.originY);
      this.ctx.fillRect(0, bottomEdge, this.canvas.width, this.canvas.height - bottomEdge);
      this.ctx.fillRect(rightEdge, 0, this.canvas.width - rightEdge, this.canvas.height);
    },

    drawPoints() {
      if (this.tool === 'pen') {
        this.ctx.strokeStyle = this.color;
        this.ctx.fillStyle = this.color;
      } else {
        this.ctx.strokeStyle = 'white';
        this.ctx.fillStyle = 'white';
      }

      this.ctx.lineWidth = this.strokeWidth;
      this.ctx.lineJoin = 'round';
      this.ctx.lineCap = 'round';

      this.ctx.beginPath();

      // Draw a single circle until we have enough points.
      if (this.points.length < 4) {
        this.ctx.arc(this.points[0].x, this.points[0].y, this.strokeWidth / 2, 0, 2 * Math.PI);
        this.ctx.fill();
        return;
      }

      this.ctx.moveTo(this.points[0].x, this.points[0].y);

      let i = 0;
      // Draw one or more quadratic curves, using the average of two points as the control point.
      // Courtesy of https://stackoverflow.com/a/10568043
      for (i = 1; i < this.points.length - 2; i++) {
        const avgX = (this.points[i].x + this.points[i + 1].x) / 2;
        const avgY = (this.points[i].y + this.points[i + 1].y) / 2;
        this.ctx.quadraticCurveTo(this.points[i].x, this.points[i].y, avgX, avgY);
      }
      this.ctx.quadraticCurveTo(this.points[i].x, this.points[i].y, this.points[i + 1].x, this.points[i + 1].y);
      this.ctx.stroke();
    },

    resizeVisibleCanvas(resetView = true) {
      // In case the component is not marked as rendered from the outside we do not attempt to resize it.
      if (!this.isRendered) {
        return;
      }

      // Take the border width into account as well.
      this.canvas.width = this.$refs.canvasContainer.getBoundingClientRect().width - 2;

      const toolbar = this.$refs.toolbar;
      if (this.isFullscreen()) {
        this.canvas.height = this.$refs.container.getBoundingClientRect().height;
        toolbar.style.borderTopLeftRadius = toolbar.style.borderTopRightRadius = '0';
      } else {
        this.canvas.height = Math.round(window.innerHeight / window.innerWidth * this.canvas.width);
        toolbar.style.borderTopLeftRadius = toolbar.style.borderTopRightRadius = '0.25rem';
      }

      if (resetView) {
        this.resetView();
      } else {
        this.redrawVisibleCanvas();
      }
    },

    pointerDown() {
      this.drawing = true;

      if (this.tool === 'pen' || this.tool === 'eraser') {
        this.draw();
        this.unsavedChanges_ = true;
      } else if (this.tool === 'colorpicker') {
        this.color = this.getCurrentPixelColor();
      }
    },

    mouseDown(event) {
      this.updateCoordinates(event.clientX, event.clientY);
      this.pointerDown();
    },

    touchStart(event) {
      const touch = event.touches[0];
      this.updateCoordinates(touch.clientX, touch.clientY);
      this.pointerDown();
    },

    pointerMove() {
      if (this.tool === 'pen' || this.tool === 'eraser') {
        this.draw();
      } else if (this.tool === 'colorpicker') {
        this.color = this.getCurrentPixelColor();
      } else if (this.tool === 'move') {
        this.originX -= this.currX - this.prevX;
        this.originY -= this.currY - this.prevY;
        this.redrawVisibleCanvas();
      }
    },

    mouseMove(event) {
      if (!this.drawing) {
        return;
      }

      this.updateCoordinates(event.clientX, event.clientY);
      this.pointerMove();
    },

    touchMove(event) {
      if (!this.drawing) {
        return;
      }

      const touch = event.touches[0];
      this.updateCoordinates(touch.clientX, touch.clientY);
      this.pointerMove();
    },

    pointerUp() {
      if (this.drawing && (this.tool === 'pen' || this.tool === 'eraser')) {
        // Finally, persist the drawn points in the actual canvas.
        this.memCtx.clearRect(this.originX, this.originY, this.canvas.width, this.canvas.height);
        this.memCtx.drawImage(
          this.canvas,
          0,
          0,
          this.canvas.width,
          this.canvas.height,
          this.originX,
          this.originY,
          this.canvas.width,
          this.canvas.height,
        );
      }

      this.drawing = false;
      this.points = [];
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
    this.canvas = this.$refs.canvas;
    this.ctx = this.canvas.getContext('2d');
    this.memCanvas = document.createElement('canvas');
    this.memCtx = this.memCanvas.getContext('2d');

    this.resizeVisibleCanvas();
    // The initial size of the actual canvas is based on the visible canvas.
    this.width = this.memCanvas.width = this.canvas.width;
    this.height = this.memCanvas.height = this.canvas.height;

    this.clearCanvas();
    this.updateCursor();

    if (this.imageUrl) {
      this.loadImage(this.imageUrl);
    }

    window.addEventListener('resize', this.resizeVisibleCanvas);
    window.addEventListener('beforeunload', this.beforeUnload);
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.resizeVisibleCanvas);
    window.removeEventListener('beforeunload', this.beforeUnload);
  },
};
</script>
