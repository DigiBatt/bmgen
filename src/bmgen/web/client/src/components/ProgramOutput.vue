<script setup>
import { ref, watchEffect } from 'vue'
import { generateProgram } from '@/lib';

const props = defineProps({
  target: String,
  format: String,
  config: Object,
  program: String,
  name: String,
  server: String
})

const outputarea = ref(null)

function updateCode() {
  generateProgram(props.server, props.target, props.format, props.config, props.program, props.name, (data) => {
    outputarea.value.innerHTML = ""
    if (data.error != null) {
      outputarea.value.innerHTML += '<div class="error">Error: ' + data.error + '</div>';
    }
    if (data.program != null) {
      outputarea.value.innerHTML += data.program;
    }
  });
}

watchEffect(() => {
  updateCode();
})

defineExpose({ updateCode });

</script>

<template>
  <div id="outputarea" ref="outputarea"></div>
</template>