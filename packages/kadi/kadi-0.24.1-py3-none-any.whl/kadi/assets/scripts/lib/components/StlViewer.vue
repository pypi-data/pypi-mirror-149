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
  <div>
    <div v-if="fileSize > maxFileSize && !forceLoad">
      <button class="btn btn-sm btn-light mb-2" @click="loadFile">
        <i class="fa-solid fa-eye"></i> {{ $t('Load preview') }}
      </button>
    </div>
    <div class="card bg-light p-1" ref="container" v-else>
      <div class="text-muted ml-1" v-if="error">
        <i class="fa-solid fa-triangle-exclamation mr-1"></i> {{ error }}
      </div>
      <div v-else>
        <div class="toolbar mr-1" v-if="!loading">
          <button type="button"
                  class="btn btn-link text-muted"
                  :title="$t('Toggle wireframe')"
                  @click="toggleWireframe">
            <i class="fa-solid fa-cube"></i>
          </button>
          <button type="button"
                  class="btn btn-link text-muted"
                  :title="$t('Reset view')"
                  @click="resetView">
            <i class="fa-solid fa-eye"></i>
          </button>
          <button type="button"
                  class="btn btn-link text-muted"
                  :title="$t('Toggle fullscreen')"
                  @click="toggleFullscreen">
            <i class="fa-solid fa-expand"></i>
          </button>
        </div>
        <div class="text-muted ml-1" v-if="loading">
          <i class="fa-solid fa-circle-notch fa-spin mr-1"></i> {{ $t('Loading model...') }}
        </div>
        <div class="render-container" ref="renderContainer"></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.render-container {
  cursor: pointer;
}

.toolbar {
  position: absolute;
  right: 0;
  z-index: 1;
}
</style>

<script>
import * as THREE from 'three';
import {STLLoader} from 'three/examples/jsm/loaders/STLLoader.js';
import {TrackballControls} from 'three/examples/jsm/controls/TrackballControls.js';
import WebGLUtil from 'three/examples/jsm/capabilities/WebGL.js';

export default {
  data() {
    return {
      renderer: null,
      scene: null,
      camera: null,
      controls: null,
      mesh: null,
      distance: 0,
      loading: true,
      error: '',
      forceLoad: false,
      maxFileSize: 25 * (10 ** 6), // 25 MB.
    };
  },
  props: {
    modelUrl: String,
    fileSize: Number,
  },
  methods: {
    isFullscreen() {
      return document.fullScreen || document.mozFullScreen || document.webkitIsFullScreen;
    },
    resetView() {
      this.controls.reset();
      this.camera.position.set(0, 0, this.distance);
      this.camera.updateProjectionMatrix();
    },
    toggleWireframe() {
      this.mesh.material.wireframe = !this.mesh.material.wireframe;
    },
    toggleFullscreen() {
      if (this.isFullscreen()) {
        document.exitFullscreen();
      } else {
        this.$refs.container.requestFullscreen();
      }
    },
    resizeView() {
      const width = this.$refs.renderContainer.getBoundingClientRect().width;
      const height = Math.round(window.innerHeight / window.innerWidth * width);

      if (this.isFullscreen()) {
        this.$refs.renderContainer.style.height = '100vh';
        this.$refs.container.style.borderRadius = '0';
      } else {
        this.$refs.renderContainer.style.height = `${height}px`;
        this.$refs.container.style.borderRadius = '0.25rem';
      }

      this.camera.aspect = width / height;
      this.camera.updateProjectionMatrix();
      this.renderer.setSize(width, height);
    },
    animate() {
      window.requestAnimationFrame(this.animate);
      this.renderer.render(this.scene, this.camera);
      this.controls.update();
    },
    onLoad(geometry) {
      this.loading = false;

      this.renderer = new THREE.WebGLRenderer({antialias: true});
      this.renderer.setPixelRatio(window.devicePixelRatio);
      this.$refs.renderContainer.appendChild(this.renderer.domElement);

      this.scene = new THREE.Scene();
      this.scene.background = new THREE.Color(0xf7f7f7);

      this.camera = new THREE.PerspectiveCamera();
      this.scene.add(this.camera);

      this.controls = new TrackballControls(this.camera, this.renderer.domElement);
      this.controls.rotateSpeed = 2;

      this.mesh = new THREE.Mesh(geometry, new THREE.MeshNormalMaterial());
      this.mesh.geometry.center();
      this.scene.add(this.mesh);

      // Calculate a good default distance along the z-axis for the camera relative to the size of the object.
      const boundingBox = new THREE.Box3().setFromObject(this.mesh);
      const length = boundingBox.getSize(new THREE.Vector3()).length();
      const fov = this.camera.fov / 2 * (Math.PI / 180);

      this.distance = length / 2 / Math.tan(fov);

      // Check if the object would be even visible using the calculacted distance. If not, attempt to calculate a new
      // distance where at least part of the object should be visible.
      if (this.distance - this.camera.far > boundingBox.max.z) {
        this.distance = this.camera.far + boundingBox.max.z - (boundingBox.max.z / 10);
      }

      this.resizeView();
      this.resetView();
      this.animate();

      window.addEventListener('resize', this.resizeView);
    },
    onError(error) {
      this.loading = false;
      this.error = $t('Error loading model.');
      console.error(error);
    },
    async loadFile() {
      this.forceLoad = true;
      await this.$nextTick();
      new STLLoader().load(this.modelUrl, this.onLoad, null, this.onError);
    },
  },
  mounted() {
    if (!WebGLUtil.isWebGLAvailable()) {
      this.error = $t('WebGL not available.');
      return;
    }

    if (this.fileSize <= this.maxFileSize) {
      this.loadFile();
    }
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.resizeView);
  },
};
</script>
