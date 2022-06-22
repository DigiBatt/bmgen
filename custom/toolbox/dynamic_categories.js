// Returns an array of objects.
var channelsFlyoutCallback = function (workspace) {
    const channelnames = Blockly.BMGen.channels;
    var blockList = [];
    for (var i = 0; i < channelnames.length; i++) {
        blockList.push({
            'kind': 'block',
            'type': 'channel',
            'fields': {
                'NAME': channelnames[i]
            }
        });
    }
    return blockList;
};

var variablesFlyoutCallback = function (workspace) {
    const variablenames = Blockly.BMGen.variables;
    var blockList = [];
    for (var i = 0; i < variablenames.length; i++) {
        blockList.push({
            'kind': 'block',
            'type': 'variable',
            'fields': {
                'NAME': variablenames[i]
            }
        });
    }
    return blockList;
};

var registerToolboxCallbacks = function (workspace) {
    workspace.registerToolboxCategoryCallback('CHANNELS', channelsFlyoutCallback);
    workspace.registerToolboxCategoryCallback('BM_VARIABLES', variablesFlyoutCallback);
};

var addChannelNameToToolbox = function (channelname) {
    Blockly.BMGen.channels.push(channelname);
};

var addVariableNameToToolbox = function (variablename) {
    Blockly.BMGen.variables.push(variablename);
};