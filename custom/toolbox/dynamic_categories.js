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

var registrationsFlyoutCallback = function (workspace) {
    const regnames = Generator.registrations;
    var blockList = [];
    blockList.push({
        'kind': 'block',
        'type': 'registration'
    });
    for (var i = 0; i < regnames.length; i++) {
        blockList.push({
            'kind': 'block',
            'type': 'regname',
            'fields': {
                'NAME': regnames[i]
            }
        });
    }
    return blockList;
};

var registerToolboxCallbacks = function (workspace) {
    workspace.registerToolboxCategoryCallback('CHANNELS', channelsFlyoutCallback);
    workspace.registerToolboxCategoryCallback('BM_VARIABLES', variablesFlyoutCallback);
    workspace.registerToolboxCategoryCallback('REGISTRATIONS', registrationsFlyoutCallback);
};

var addChannelNameToToolbox = function (channelname) {
    Generator.channels.push(channelname);
};

var addVariableNameToToolbox = function (variablename) {
    Generator.variables.push(variablename);
};

var addRegistrationNameToToolbox = function (regname) {
    Generator.registrations.push(regname);
};

exports = { registerToolboxCallbacks, addChannelNameToToolbox, addVariableNameToToolbox, addRegistrationNameToToolbox };