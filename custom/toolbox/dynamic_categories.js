goog.module("BMGen3000.Toolbox.DynamicCategories");
var { Generator } = goog.require("BMGen3000.Generator");

// Returns an array of objects.
var channelsFlyoutCallback = function (workspace) {
    const channelnames = Generator.channels;
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
    const variablenames = Generator.variables;
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
    Generator.channels.push(channelname);
};

var addVariableNameToToolbox = function (variablename) {
    Generator.variables.push(variablename);
};

exports = { registerToolboxCallbacks, addChannelNameToToolbox, addVariableNameToToolbox };