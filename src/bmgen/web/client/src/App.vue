<script setup>
import Controls from './components/Controls.vue';
import Editor from './components/Editor.vue'
import ProgramOutput from './components/ProgramOutput.vue'
import { ref, watch, provide, computed } from 'vue'
import { GeneratorSettings } from '@/targets';

const code = ref("Hello world!");
const config = ref({});
const name = ref("program");
const server = ref(window.location.href);
// const server = ref("http://localhost:5000");
const version = ref("");

function syncToStorage(item, key, isJson) {
  if (key in localStorage) {
    if (isJson === true) {
      item.value = JSON.parse(localStorage.getItem(key));
    } else {
      item.value = localStorage.getItem(key);
    }
  }
  watch(item, (newValue) => {
    if (isJson === true) {
      localStorage.setItem(key, JSON.stringify(newValue));
    } else {
      localStorage.setItem(key, newValue);
    }
  },
    { deep: true })
}

syncToStorage(code, "program");
syncToStorage(name, "name");
syncToStorage(config, "config", true);

provide("config", config);
provide("server", server);
provide("name", name);
provide("code", code);

if (config.value.target == undefined) {
  config.value.target = "bm";
}

const format = computed(() => GeneratorSettings[config.value.target].displayFormat);
const target = computed(() => GeneratorSettings[config.value.target].target);

fetch(new URL(`api/version`, server.value).href).then((response) => response.text()).then((data) => {
  version.value = data;
})

</script>

<template>
  <Controls ref="controls" @update-program="$refs.programOutput.updateCode()" />
  <Editor :content="code" @change="(program) => code = program" />
  <ProgramOutput ref="programOutput" :target="target" :format="format" :config="config" :program="code" :name="name"
    :server="server" />
  <div class="footer">
    BMGen v{{ version }}
  </div>

</template>

<style scoped></style>
