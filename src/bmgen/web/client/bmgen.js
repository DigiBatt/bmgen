var editor = null;
var outputarea = null;
var targetdropdown = null;
var programNameField = null;

const generatorSettings = {
    "bm": {
        "format": "text",
        "filenameExtension": ".txt"
    },
    "neware": {
        "format": "xml",
        "filenameExtension": ".xml"
    },
    "basytec": {
        "format": "text",
        "filenameExtension": ".pln"
    }
}

function init() {
    require.config({ paths: { vs: './node_modules/monaco-editor/min/vs' } });

    require(['vs/editor/editor.main'], function () {
        editor = monaco.editor.create(document.getElementById('codearea'), {
            value: ['from bmgen.function import *', 'charge(current=5.0)'].join('\n'),
            language: 'python'
        });
        updateCode();
    });

    codearea = document.getElementById('codearea');
    outputarea = document.getElementById('outputarea');
    targetdropdown = document.getElementById('target');
    programNameField = document.getElementById('programName');
    codearea.addEventListener('change', updateCode);
    targetdropdown.addEventListener('change', updateCode);
}

function generate(program, target, format, callback) {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", `/${target}/${format}/`);
    const formData = new FormData();
    const file = new Blob([program], { type: 'text/plain' });
    formData.append("program", file);
    xhr.send(formData);
    xhr.onload = () => callback(xhr);
}

function updateCode(event) {
    const target = targetdropdown.value;
    const program = editor.getValue();
    const callback = (xhr) => {
        if (xhr.readyState == 4 && xhr.status == 200) {
            const data = xhr.response;
            outputarea.innerHTML = data;
        } else if (xhr.readyState == 4 && xhr.status == 400) {
            const data = xhr.response;
            outputarea.innerHTML = "Error: " + data;
        }
    };
    generate(program, target, "table", callback);
}

function saveProgram() {
    const code = editor.getValue();
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(code));
    let filename = programNameField.value
    if (filename) {
        filename += '.py';
    } else {
        filename = 'program.py';
    }
    element.setAttribute('download', filename);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

function loadProgram(files) {
    var reader = new FileReader();
    reader.onload = (function () { return function (e) { editor.setValue(e.target.result); updateCode(); }; })();
    reader.readAsText(files[0]);
    document.getElementById('programName').value = files[0].name.substring(0, files[0].name.indexOf('.'));
}

function downloadProgram() {
    const target = targetdropdown.value;
    const program = editor.getValue();
    const format = generatorSettings[target].format;
    const ext = generatorSettings[target].filenameExtension;
    const callback = (xhr) => {
        if (xhr.readyState == 4 && xhr.status == 200) {
            const data = xhr.response;
            var element = document.createElement('a');
            element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(data));
            let filename = programNameField.value
            if (filename) {
                filename += ext;
            } else {
                filename = 'program' + ext;
            }
            element.setAttribute('download', filename);
            element.style.display = 'none';
            document.body.appendChild(element);
            element.click();
            document.body.removeChild(element);
        } else if (xhr.readyState == 4 && xhr.status == 400) {
            const data = xhr.response;
            outputarea.innerHTML = "Error: " + data;
        }
    };
    generate(program, target, format, callback);
}