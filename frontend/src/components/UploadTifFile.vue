<script setup lang="ts">
import { ref, reactive } from 'vue'

const emits = defineEmits(['images-processed'])
const selectedFile = ref<File | null>(null)
const loading = ref(false)

function handle_file_change(event: Event) {
  selectedFile.value = (event.target as HTMLInputElement).files?.[0] || null
}

async function load_example() {
  loading.value = true

  const res = await fetch('http://127.0.0.1:8000/calculate-terrain-example', { method: 'GET' })
  const data = await res.json()
  console.log(data)
  emits('images-processed', data.images)

  loading.value = false
}

async function process_file() {
  console.log('Processing file...')

  if (!selectedFile.value) {
    console.error('No file selected')
    loading.value = false
    return
  }

  loading.value = true

  const formData = new FormData()
  formData.append('tif_file', selectedFile.value)

  const res = await fetch('http://127.0.0.1:8000/calculate-terrain-from-file', {
    method: 'POST',
    body: formData,
  })
  const data = await res.json()
  console.log(data)
  emits('images-processed', data.images)

  loading.value = false
}
</script>

<template>
  <p style="margin-bottom: 20px">
    Click <button class="example" @click="load_example">here</button> to see and example using a
    sample file of data from Brecon, Wales.
  </p>
  <div class="upload-cont">
    <input type="file" id="tif-file" @change="handle_file_change" />
    <button class="btn" @click="process_file">Upload File</button>
  </div>
</template>
