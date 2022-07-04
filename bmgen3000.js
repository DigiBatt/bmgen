goog.module("BMGen3000");
goog.module.declareLegacyNamespace();

function loadScript(url) {
    var script = document.createElement("script");
    script.src = url;
    document.head.appendChild(script);
}

const { bts_parse_program } = goog.require("BMGen3000.BTS600.parser");
goog.require("BMGen3000.Blocks");
const { Generator } = goog.require("BMGen3000.Generator");
goog.require("BMGen3000.Generator.Channels");
goog.require("BMGen3000.Generator.Limits");
goog.require("BMGen3000.Generator.Other");
goog.require("BMGen3000.Generator.Statements");
goog.require("BMGen3000.Generator.Variables");
const { registerToolboxCallbacks, addChannelNameToToolbox, addVariableNameToToolbox } = goog.require("BMGen3000.Toolbox.DynamicCategories");
let { toolbox } = goog.require("BMGen3000.Toolbox");
const BMGenParser = goog.require("BMGen3000.Parser");
const { bmgen_to_bts } = goog.require("BMGen3000.BMGenToBTS");
goog.require("BMGen3000.BTS600.ProgramToText");
goog.require("BMGen3000.BTS600.ProgramToTable");
goog.require("BMGen3000.BTS600.ProgramToBM");
goog.require("BMGen3000.BTS600.Simplify");
const { bmgen_to_xml } = goog.require("BMGen3000.BMGenToXML");

var workspace;

function loadBMGen() {
    var blocklyArea = document.getElementById('blocklyArea');
    var blocklyDiv = document.getElementById('blocklyDiv');

    for (let category of toolbox.getElementsByTagName("category")) {
        if (category.getAttribute("name") === "Variables") {
            category.setAttribute("custom", "BM_VARIABLES");
        }
        else if (category.getAttribute("name") === "Channels") {
            category.setAttribute("custom", "CHANNELS");
        }
    }

    workspace = Blockly.inject(blocklyDiv,
        { toolbox: toolbox.documentElement });
    var onresize = function (e) {
        // Compute the absolute coordinates and dimensions of blocklyArea.
        var element = blocklyArea;
        var x = 0;
        var y = 0;
        do {
            x += element.offsetLeft;
            y += element.offsetTop;
            element = element.offsetParent;
        } while (element);
        // Position blocklyDiv over blocklyArea.
        blocklyDiv.style.left = x + 'px';
        blocklyDiv.style.top = y + 'px';
        blocklyDiv.style.width = blocklyArea.offsetWidth + 'px';
        blocklyDiv.style.height = blocklyArea.offsetHeight + 'px';
        Blockly.svgResize(workspace);
    };
    window.addEventListener('resize', onresize, false);
    onresize();
    Blockly.svgResize(workspace);

    registerToolboxCallbacks(workspace);
    workspace.addChangeListener(myUpdateFunction);
    document.getElementById('bm_format').addEventListener('change', myUpdateFunction);
    document.getElementById('codearea').addEventListener('change', updateFromCode);
}

function myUpdateFunction(event) {
    var code = Generator.workspaceToCode(workspace);
    var bts_code = bts_parse_program(bmgen_to_bts(BMGenParser.parse(code))).simplify();
    document.getElementById('codearea').value = code;
    if (document.getElementById('bm_format').checked) {
        document.getElementById('bmarea').innerHTML = '<textarea readonly style="overflow: auto; height: 95%; width: 100%">' + bts_code.toBM() + '</textarea>';
    } else {
        document.getElementById('bmarea').innerHTML = bts_code.toTable();
    }
}

function updateFromCode(event) {
    import_text_program(document.getElementById('codearea').value);
}

function import_text_program(file) {
    var program = BMGenParser.parse(file);
    import_json_program(program);
}

function import_json_program(program) {
    var xml = bmgen_to_xml(program);
    const parser = new DOMParser();
    const doc = parser.parseFromString(xml, 'application/xml');
    workspace.clear();
    Blockly.Xml.domToWorkspace(doc.documentElement, workspace);
    Generator.fillDynamicCategoriesFromProgram(program);
}

function saveProgram() {
    const code = Generator.workspaceToCode(workspace);
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(code));
    let filename = document.getElementById('programName').value
    if (filename) {
        filename += '.bmgen';
    } else {
        filename = 'program.bmgen';
    }
    element.setAttribute('download', filename);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

function loadProgram(files) {
    var reader = new FileReader();
    if (files[0].name.endsWith('xml')) {
        reader.onload = (function () { return function (e) { loadXml(e.target.result); }; })();
    } else if (files[0].name.endsWith('json')) {
        reader.onload = (function () { return function (e) { import_json_program(e.target.result); }; })();
    } else if (files[0].name.endsWith('bmgen')) {
        reader.onload = (function () { return function (e) { import_text_program(e.target.result); }; })();
    } else {
        alert("Unknown file format");
    }
    reader.readAsText(files[0]);
    document.getElementById('programName').value = files[0].name.substring(0, files[0].name.indexOf('.'));
}

function loadXml(file) {
    const parser = new DOMParser();
    const doc = parser.parseFromString(file, 'application/xml');
    workspace.clear();
    Blockly.Xml.domToWorkspace(doc.documentElement, workspace);
}

function programToClipboard() {
    var code = Blockly.BTS600.workspaceToCode(workspace);
    navigator.clipboard.writeText(code)
}

function addChannel() {
    let channelname = window.prompt("Channel name:", "");
    addChannelNameToToolbox(channelname);
}

function addVariable() {
    let variablename = window.prompt("Variable name:", "");
    addVariableNameToToolbox(variablename);
}

exports = { loadBMGen, addChannel, addVariable, loadProgram, saveProgram };