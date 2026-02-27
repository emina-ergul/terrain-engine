<script setup lang="ts">
import { ref, reactive } from 'vue'
import UploadTifFile from './components/UploadTifFile.vue'

const showingImages = ref(false)
const images = reactive({
  slope: '',
  aspect: '',
  hillshade: '',
  curvature: '',
})

async function update_images(new_images: any) {
  showingImages.value = true
  Object.assign(images, new_images)
}

function clear_images() {
  showingImages.value = false
  images.slope = ''
  images.aspect = ''
  images.hillshade = ''
  images.curvature = ''
}
</script>

<template>
  <nav class="nav">
    <h1>Terrain Engine</h1>
  </nav>
  <div class="main">
    <p>
      Upload a .tif file to visualize the terrain data. The application will process the file and
      display the terrain attributes.
    </p>
    <UploadTifFile @images-processed="update_images" />
    <button class="btn" @click="clear_images">Clear all</button>
    <div class="img-cont">
      <img v-if="showingImages" :src="images.slope" alt="Slope Map" />
      <img v-if="showingImages" :src="images.aspect" alt="Aspect Map" />
      <img v-if="showingImages" :src="images.hillshade" alt="Hillshade Map" />
      <img v-if="showingImages" :src="images.curvature" alt="Curvature Map" />
    </div>
  </div>
</template>

<style scoped></style>
