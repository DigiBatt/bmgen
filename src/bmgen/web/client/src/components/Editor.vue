<script setup>
import { onMounted, watch } from 'vue'
import * as monaco from 'monaco-editor'
import editorWorker from 'monaco-editor/esm/vs/editor/editor.worker?worker'
import jsonWorker from 'monaco-editor/esm/vs/language/json/json.worker?worker'
import cssWorker from 'monaco-editor/esm/vs/language/css/css.worker?worker'
import htmlWorker from 'monaco-editor/esm/vs/language/html/html.worker?worker'
import tsWorker from 'monaco-editor/esm/vs/language/typescript/ts.worker?worker'

const props = defineProps({
    content: String
})

self.MonacoEnvironment = {
  getWorker(_, label) {
    if (label === 'json') {
      return new jsonWorker()
    }
    if (label === 'css' || label === 'scss' || label === 'less') {
      return new cssWorker()
    }
    if (label === 'html' || label === 'handlebars' || label === 'razor') {
      return new htmlWorker()
    }
    if (label === 'typescript' || label === 'javascript') {
      return new tsWorker()
    }
    return new editorWorker()
  }
}

let editor = null;

const emit = defineEmits(['change'])

function emitChanges() {
    console.log("changes");
    emit('change', editor.getValue())
}

onMounted(() => {
    editor = monaco.editor.create(document.getElementById('codearea'), {
        value: props.content,
        language: 'python'
    });
    editor.onDidBlurEditorWidget(() => emitChanges());
});

watch(() => props.content, () => {
  editor.setValue(props.content);
});

</script>

<template>
    <div id="codearea" @change="emitChanges"></div>
</template>