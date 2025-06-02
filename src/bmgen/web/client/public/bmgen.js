var editor = null;
var outputarea = null;
var targetdropdown = null;
var programNameField = null;

const generatorSettings = {
    "bm": {
        "target": "bm",
        "displayFormat": "table",
        "downloadFormat": "text",
        "filenameExtension": ".txt"
    },
    "neware": {
        "target": "neware",
        "displayFormat": "table",
        "downloadFormat": "xml",
        "filenameExtension": ".xml"
    },
    "basytec": {
        "target": "basytec",
        "displayFormat": "table",
        "downloadFormat": "text",
        "filenameExtension": ".pln"
    },
    "bcl": {
        "target": "bcl",
        "displayFormat": "html",
        "downloadFormat": "json",
        "filenameExtension": ".json"
    },
    "jsonld": {
        "target": "jsonld",
        "displayFormat": "html",
        "downloadFormat": "html",
        "filenameExtension": ".json"
    }
}

function init() {
    require.config({ paths: { vs: './node_modules/monaco-editor/min/vs' } });

    require(['vs/editor/editor.main'], function () {
        editor = monaco.editor.create(document.getElementById('codearea'), {
            value: '',
            language: 'python'
        });
        initCode();
    });

    codearea = document.getElementById('codearea');
    outputarea = document.getElementById('outputarea');
    targetdropdown = document.getElementById('target');
    programNameField = document.getElementById('programName');
    codearea.addEventListener('change', updateCode);
    targetdropdown.addEventListener('change', updateCode);
    targetdropdown.addEventListener('change', updateConfig);
    document.getElementById('more-config').addEventListener('change', updateCode);
    updateConfig();
}

function initCode() {
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "example.py");
    xhr.send()
    xhr.onload = () => {
        if (xhr.readyState == 4 && xhr.status == 200) {
            const data = xhr.response;
            editor.setValue(data);
            updateCode();
        }
    };
}

function generate(program, target, format, callback) {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", `api/generate/${target}/${format}/`);
    const formData = new FormData();
    const file = new Blob([program], { type: 'text/plain' });
    formData.append("program", file);
    const config = new Blob([JSON.stringify(getConfig())], { type: 'application/json' });;
    formData.append("config", config);
    xhr.send(formData);
    xhr.onload = () => callback(xhr);
}

function download(program, target, format, callback) {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", `api/download/${target}/${format}/`);
    xhr.responseType = "blob";
    const formData = new FormData();
    const file = new Blob([program], { type: 'text/plain' });
    formData.append("program", file);
    const config = new Blob([JSON.stringify(getConfig())], { type: 'application/json' });;
    formData.append("config", config);
    xhr.send(formData);
    xhr.onload = () => callback(xhr);
}

function updateCode(event) {
    const target = generatorSettings[targetdropdown.value].target;
    const program = editor.getValue();
    const format = generatorSettings[targetdropdown.value].displayFormat;
    const callback = (xhr) => {
        if (xhr.readyState == 4) {
            const data = JSON.parse(xhr.response);
            outputarea.innerHTML = ""
            if (data.error != null) {
                outputarea.innerHTML += '<div class="error">Error: ' + data.error + '</div>';
            }
            if (data.program != null) {
                outputarea.innerHTML += data.program;
            }
        }
    };
    generate(program, target, format, callback);
}

function saveProgram() {
    const code = editor.getValue();
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(code));
    let filename = programNameField.value;
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
    const target = generatorSettings[targetdropdown.value].target;
    const program = editor.getValue();
    const format = generatorSettings[targetdropdown.value].downloadFormat;
    const ext = generatorSettings[targetdropdown.value].filenameExtension;
    const callback = (xhr) => {
        if (xhr.readyState == 4 && xhr.status == 200) {
            const data = xhr.response;
            var element = document.createElement('a');
            const objectUrl = URL.createObjectURL(data);
            element.setAttribute('href', objectUrl);
            let filename = programNameField.value;
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
            URL.revokeObjectURL(objectUrl);
        } else if (xhr.readyState == 4 && xhr.status == 400) {
            const data = xhr.response;
            outputarea.innerHTML = "Error: " + data;
        }
    };
    download(program, target, format, callback);
}

function toggleConfig() {
    document.getElementById("toggleConfig").classList.toggle("active");
    var content = document.getElementById("more-config");
    if (content.style.display === "block") {
        content.style.display = "none";
    } else {
        content.style.display = "block";
    }
}

function updateConfig() {
    const target = targetdropdown.value;
    var elements = document.getElementsByClassName("target-config");
    for (var i = 0; i < elements.length; i++) {
        if (elements[i].id === target + "-config") {
            elements[i].style.display = "block";
        } else {
            elements[i].style.display = "none";
        }
    }
}

function getConfig() {
    var config = {};
    var elements = document.getElementsByClassName("configitem");
    for (var i = 0; i < elements.length; i++) {
        const key = elements[i].id;
        const parts = key.split("_");
        let node = config;
        for (var j = 0; j < parts.length - 1; j++) {
            if (node[parts[j]] === undefined) {
                node[parts[j]] = {};
            }
            node = node[parts[j]];
        }
        var value = elements[i].value;
        if (elements[i].classList.contains("float")) {
            value = parseFloat(value);
        } else if (elements[i].classList.contains("bool")) {
            value = elements[i].checked;
        }
        node[parts[parts.length - 1]] = value;
    }
    return config;
}

function saveConfig() {
    const data = JSON.stringify(getConfig(), null, 4);
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(data));
    const filename = "bmgen_config.json";
    element.setAttribute('download', filename);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

function loadConfig(files) {
    var reader = new FileReader();
    reader.onload = (function () {
        return function (e) {
            const data = JSON.parse(e.target.result);
            setConfigValues("", data);
            updateCode();
        };
    })();
    reader.readAsText(files[0]);
}

function setConfigValues(prefix, data) {
    for (const [key, value] of Object.entries(data)) {
        console.log(prefix + "; " + key + "; " + value);
        var configkey = "";
        if (prefix === "") {
            configkey = key;
        } else {
            configkey = prefix + "_" + key;
        }
        if (typeof value === 'object' && value !== null) {
            setConfigValues(configkey, value);
        } else {
            var element = document.getElementById(configkey);
            if (typeof value === 'boolean') {
                element.checked = value;
            } else {
                element.value = value;
            }
        }
    }
}