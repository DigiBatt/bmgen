// Returns an array of objects.
var channelsFlyoutCallback = function (workspace) {
    const channelnames = Blockly.BTS600.channels;
    var blockList = [];
    for (var i = 0; i < channelnames.length; i++) {
        blockList.push({
            'kind': 'block',
            'type': 'channel',
            'fields': {
                'CHANNEL': channelnames[i]
            }
        });
    }
    return blockList;
};

var variablesFlyoutCallback = function (workspace) {
    const variablenames = Blockly.BTS600.variables;
    var blockList = [];
    blockList.push({
        'kind': 'block',
        'type': 'assignment',
        'fields': {
            'RHS': 0
        }
    });
    for (var i = 0; i < variablenames.length; i++) {
        blockList.push({
            'kind': 'block',
            'type': 'variable',
            'fields': {
                'VARIABLE': variablenames[i]
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
    Blockly.BTS600.channels.push(channelname);
};

var addVariableNameToToolbox = function (variablename) {
    Blockly.BTS600.variables.push(variablename);
};