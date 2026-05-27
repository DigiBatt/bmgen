<script setup>
import { ref, toRef, defineModel } from 'vue'
import Select from 'primevue/select';
import InputText from 'primevue/inputtext';
import InputNumber from 'primevue/inputnumber';
import Checkbox from 'primevue/checkbox';
import { Form } from '@primevue/forms';

const props = defineProps({
    model: Object,
    columns: Number,
    disabled: Boolean
})

const model = ref(props.model);
const values = defineModel();
const form = ref();
const columns = toRef(() => props.columns ? props.columns : 1)

const emit = defineEmits(['submit', 'change'])

function getValues() {
    const values = {};
    for (var key in form.value.states) {
        values[key] = form.value.states[key].value;
    }
    return values;
}

function emitChange(name) {
    values.value[name] = form.value.states[name].value;
}

function getRows() {
    let chunks = [];
    for (let i = 0; i < model.value.length; i += columns.value) {
        chunks.push(model.value.slice(i, i + columns.value))
    }
    return chunks;
}

defineExpose({getValues});

</script>

<template>
    <Form ref="form" v-slot="$form" :initial-values="values" @submit="(e) => emit('submit', e)">
        <table>
            <tr v-for="row in getRows()">
                <template v-for="entry in row">
                    <td>
                        <Checkbox v-if="entry.type === 'boolean'" :name="entry.name" binary :disabled="props.disabled" @change="emitChange(entry.name)"></Checkbox>
                        <label v-else-if="'label' in entry">{{ entry.label }}</label>
                    </td>
                    <td>
                        <InputText class="inputfield" v-if="entry.type === 'string'" :name="entry.name" type="text" @change="emitChange(entry.name)" :disabled="props.disabled">
                        </InputText>
                        <InputNumber class="inputfield" v-if="entry.type === 'integer'" :name="entry.name" @blur="emitChange(entry.name)" :disabled="props.disabled" locale="en-US"></InputNumber>
                        <InputNumber class="inputfield" v-if="entry.type === 'float'" :name="entry.name" :max-fraction-digits="20" locale="en-US"
                            @blur="emitChange(entry.name)" :disabled="props.disabled">
                        </InputNumber>
                        <Select class="inputfield" v-if="entry.type === 'options'" :name="entry.name" :options="entry.options"
                            option-label="label" option-value="name"  :disabled="props.disabled" @change="emitChange(entry.name)"/>
                        <label v-if="entry.type === 'boolean' && 'label' in entry">{{ entry.label }}</label>
                    </td>
                </template>
            </tr>
        </table>
    </Form>
</template>

<style lang="css" scoped>
#container {
    display: flex;
    justify-content: space-between;
}

#grid {
    display: grid;
    grid-template-columns: auto auto auto;
    align-items: center;
    column-gap: 0.5em;
    row-gap: 0.5em;
}

#grid span>* {
    margin-right: 0.5em;
}

#examples {
    width: 20em;
}

td:nth-child(2n)>*:last-child {
    margin-right: 1em;
}

</style>