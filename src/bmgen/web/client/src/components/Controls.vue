<script setup>
import { ref, computed, inject } from 'vue'
import Button from 'primevue/button';
import Select from 'primevue/select';
import Checkbox from 'primevue/checkbox';
import InputText from 'primevue/inputtext';
import DynamicForm from './DynamicForm.vue'
import Menubar from 'primevue/menubar';
import { GeneratorSettings } from '@/targets';
import { downloadProgram, saveFile, basename } from '@/lib';

const props = defineProps({})

const examples = ref([]);
const showConfig = ref(false);
const configButtonIcon = computed(() => showConfig.value === true ? "pi pi-angle-down" : "pi pi-angle-right");
const config = inject("config");
const server = inject("server");
const code = inject("code");
const selectedExample = ref();
const programName = inject("name");

// for (const [key, value] of Object.entries(object)) {

const targets = Object.keys(GeneratorSettings).map((name) => { return { name: GeneratorSettings[name].label, value: name } });

const options =
{
    "battery": [{ "name": "nominalCapacity", "label": "Capacity", "type": "float" },
    { "name": "nominalVoltage", "label": "Nominal Voltage", "type": "float" },
    { "name": "minChargeTemperature", "label": "Minimum Charge Temperature", "type": "float" },
    { "name": "contChargeCurrent", "label": "Continuous Charge Current", "type": "float" },
    { "name": "minVoltage", "label": "Minimum Voltage", "type": "float" },
    { "name": "maxChargeTemperature", "label": "Maximum Charge Temperature", "type": "float" },
    { "name": "peakChargeCurrent", "label": "Peak Charge Current", "type": "float" },
    { "name": "maxVoltage", "label": "Maximum Voltage", "type": "float" },
    { "name": "minDischargeTemperature", "label": "Minimum Discharge Temperature", "type": "float" },
    { "name": "contDischargeCurrent", "label": "Continuous Discharge Current", "type": "float" },
    { "name": "eodVoltage", "label": "End-Of-Discharge Voltage", "type": "float" },
    { "name": "maxDischargeTemperature", "label": "Maximum Discharge Temperature", "type": "float" },
    { "name": "peakDischargeCurrent", "label": "Peak Discharge Current", "type": "float" },
    { "name": "eocVoltage", "label": "End-Of-Charge Voltage", "type": "float" },
    { "name": "weight", "label": "Weight", "type": "float" },
    { "name": "nominalCurrent", "label": "Nominal Current", "type": "float" },
    { "name": "internalResistance", "label": "Internal Resistance", "type": "float" },
    { "name": "energyDensity", "label": "Energy Density", "type": "float" }],
    "bm": [
        { "name": "cell-temperature", "label": "Cell Temperature", "type": "string" },
        { "name": "safetask", "label": "Generate SafeTask for MaCy", "type": "boolean" },
        { "name": "pythonEval", "label": "Evaluate variable values in Python", "type": "boolean" },
        { "name": "env-temperature", "label": "Environment Temperature", "type": "string" },
        { "name": "oldArrays", "label": "Use old array implementation without custom operators", "type": "boolean" },
        { "name": "pythonArrays", "label": "Evaluate array operations in Python", "type": "boolean" },
    ]
}

const examplesMenu = ref({ label: 'Load Examples', items: [] });
const menuItems = ref([
    { label: 'Save', icon: 'pi pi-save', command: saveProgram },
    { label: 'Load', icon: 'pi pi-folder-open', command: () => document.getElementById("fileupload").click() },
    { label: 'Download program', icon: 'pi pi-download', command: downloadGenerated },
    examplesMenu.value,
    { label: 'Import JSON-LD', command: () => document.getElementById("jsonupload").click() },
])

fetch(new URL(`api/examples`, server.value).href).then((response) => response.json()).then((data) => {
    examples.value = data;
    examplesMenu.value.items = data.map((item) => { return { label: item, command: () => loadExample(item) } });
})

function loadExample(selectedExample) {
    fetch(new URL(`examples/${selectedExample}`, server.value).href).then((response) => response.text()).then((data) => {
        code.value = data;
        programName.value = basename(selectedExample);
    })
}

function saveProgram() {
    const basename = programName.value ? programName.value : 'program';
    const filename = basename + '.py';
    saveFile(code.value, filename);
}

function loadProgram(files) {
    var reader = new FileReader();
    reader.onload = (function () { return function (e) { code.value = e.target.result; }; })();
    reader.readAsText(files[0]);
    programName.value = basename(files[0].name);
}

function importJsonLD(files) {
    const callback = (xhr) => {
        if (xhr.readyState == 4) {
            code.value = xhr.response;
        }
    };
    var reader = new FileReader();
    reader.onload = (function () {
        return function (e) {
            const url = new URL(`api/import/jsonld/`, server.value);
            const xhr = new XMLHttpRequest();
            xhr.open("POST", url.href);
            const formData = new FormData();
            const file = new Blob([e.target.result], { type: 'application/json' });
            formData.append("program", file);
            xhr.send(formData);
            xhr.onload = () => callback(xhr);
        };
    })();
    reader.readAsText(files[0]);
    programName.value = basename(files[0].name);
}

function downloadGenerated() {
    downloadProgram(server.value, GeneratorSettings[config.value.target].target, GeneratorSettings[config.value.target].downloadFormat, config.value, code.value, programName.value, (data) => {
        const extension = GeneratorSettings[config.value.target].filenameExtension;
        const basename = programName.value ? programName.value : 'program';
        const filename = basename + extension;
        saveFile(data, filename);
    })
}

if (code.value === "") {
    loadExample("simple_program.py");
}

const emit = defineEmits(['updateProgram'])

</script>

<template>
    <Menubar class="menu" :model="menuItems">
        <template #start>BM Generator</template>
        <template #end>
            <div class="p-menubar-item">
                <div class="p-menubar-item-content">
                    <a class="p-menubar-item-link" href="docs/index.html" target="_blank"><span
                            class="p-menubar-item-label">View documentation</span></a>
                </div>
            </div>
        </template>
    </Menubar>
    <div id="controls">
        <div id="container">
            <div>
                <span class="group">
                Program Name:
                <InputText v-model="programName" type="text" />
                </span>

                <span class="group">
                Target:
                <Select v-model="config.target" id="target" :options="targets" option-label="name"
                    option-value="value" />
                </span>

                <span>
                    <input type="file" id="fileupload" class="hidden" name="Load"
                        @change="(e) => loadProgram(e.target.files)" />
                    <input type="file" id="jsonupload" class="hidden" name="Import JSON-LD"
                        @change="(e) => importJsonLD(e.target.files)" />
                </span>
            </div>
            <div>
                <Button @click="() => emit('updateProgram')" label="Refresh output" severity="secondary"></Button>
            </div>
        </div>
        <Button :icon="configButtonIcon" variant="text" @click="() => showConfig = !showConfig"></Button>
        Show additional config options
        <div v-if="showConfig">
            <h2>Battery Parameters</h2>
            <Checkbox binary v-model="config.predefinedBattery"></Checkbox>
            Use fixed values for battery parameters instead of variables
            <DynamicForm ref="batteryForm" :model="options.battery" v-model="config.battery" :columns="3">
            </DynamicForm>
            <div v-if="['bm', 'bm_sql'].includes(config.target)">
                <h2>Battery Manager</h2>
                <DynamicForm ref="bmForm" :model="options.bm" v-model="config.bm" :columns="3">
                </DynamicForm>
            </div>
        </div>
    </div>
</template>

<style lang="css" scoped>
#container {
    display: flex;
    justify-content: space-between;
}

.group {
    margin-right: 1em;
}

#controls {
    margin-bottom: 2vh;
}

/* #grid {
    display: grid;
    grid-template-columns: auto auto;
    align-items: center;
    column-gap: 0.5em;
    row-gap: 0.5em;
}

#grid span>* {
    margin-right: 0.5em;
}

#grid span>*:last-child {
    margin-right: 0em;
} */

#examples {
    width: 20em;
}
</style>