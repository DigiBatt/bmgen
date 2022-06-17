const Align = Blockly.Input.Align;
const Mutator = Blockly.Mutator;
const xmlUtils = Blockly.utils.xml;

Blockly.defineBlocksWithJsonArray([
    {
        "type": "goto",
        "message0": "GOTO %1",
        "args0": [
            {
                "type": "field_input",
                "name": "LABEL",
                "text": "label"
            }
        ],
        "inputsInline": true,
        "previousStatement": null,
        "colour": 0,
        "tooltip": "",
        "helpUrl": ""
    },
    {
        "type": "label",
        "message0": "LABEL %1",
        "args0": [
            {
                "type": "field_input",
                "name": "LABEL",
                "text": "label"
            }
        ],
        "inputsInline": true,
        "previousStatement": null,
        "nextStatement": null,
        "colour": 0,
        "tooltip": "",
        "helpUrl": ""
    },
    {
        "type": "limit",
        "message0": "%1",
        "args0": [
            {
                "type": "input_value",
                "name": "EXPRESSION",
                "check": "Boolean"
            }
        ],
        "inputsInline": true,
        "previousStatement": null,
        "nextStatement": null,
        "colour": 230,
        "tooltip": "",
        "helpUrl": ""
    },
    {
        "type": "err",
        "message0": "ERR %1",
        "args0": [
            {
                "type": "field_number",
                "name": "ERRNUM",
                "value": 1,
                "min": 0,
                "max": 127,
                "precision": 1
            }
        ],
        "inputsInline": true,
        "previousStatement": null,
        "colour": 0,
        "tooltip": "",
        "helpUrl": ""
    },
    {
        "type": "set",
        "message0": "SET %1 VALUE %2 LIMIT %3 REGISTRATION %4",
        "args0": [
            {
                "type": "input_dummy"
            },
            {
                "type": "input_statement",
                "name": "VALUE"
            },
            {
                "type": "input_statement",
                "name": "LIMIT",
                "check": "limit"
            },
            {
                "type": "input_statement",
                "name": "REGISTRATION"
            }
        ],
        "previousStatement": null,
        "nextStatement": null,
        "colour": 290,
        "tooltip": "",
        "helpUrl": ""
    },
    {
        "type": "statement",
        "message0": "%1 %2 VALUE %3 LIMIT %4 REGISTRATION %5",
        "args0": [
            {
                "type": "field_input",
                "name": "OPERATOR",
            },
            {
                "type": "input_dummy"
            },
            {
                "type": "input_value",
                "name": "VALUE"
            },
            {
                "type": "input_value",
                "name": "LIMIT",
                "check": "limit"
            },
            {
                "type": "input_value",
                "name": "REGISTRATION"
            }
        ],
        "previousStatement": null,
        "nextStatement": null,
        "colour": 290,
        "tooltip": "",
        "helpUrl": ""
    },
    {
        "type": "beg",
        "message0": "BEG %1",
        "args0": [
            {
                "type": "field_input",
                "name": "NAME",
                "text": "name"
            }
        ],
        "previousStatement": null,
        "nextStatement": null,
        "colour": 290,
        "tooltip": "",
        "helpUrl": ""
    },
    {
        "type": "cyc",
        "message0": "CYC %1 *",
        "args0": [
            {
                "type": "field_number",
                "name": "VALUE",
                "value": 1,
                "min": 1,
                "precision": 1
            }
        ],
        "previousStatement": null,
        "nextStatement": null,
        "colour": 290,
        "tooltip": "",
        "helpUrl": ""
    },
    {
        "type": "sto",
        "message0": "STO",
        "previousStatement": null,
        "colour": 290,
        "tooltip": "",
        "helpUrl": ""
    },
    {
        "type": "cha",
        "message0": "CHA %1 VALUE %2 LIMIT %3",
        "args0": [
            {
                "type": "input_dummy"
            },
            {
                "type": "input_value",
                "name": "VALUE",
                "check": [
                    "Number",
                    "channel"
                ]
            },
            {
                "type": "input_statement",
                "name": "LIMIT"
            }
        ],
        "previousStatement": null,
        "nextStatement": null,
        "colour": 290,
        "tooltip": "",
        "helpUrl": ""
    },
    {
        "type": "limit_action",
        "message0": "if %1 %2",
        "args0": [
            {
                "type": "input_value",
                "name": "EXPRESSION",
                "check": "Boolean"
            },
            {
                "type": "input_statement",
                "name": "ACTION"
            }
        ],
        "inputsInline": true,
        "previousStatement": null,
        "nextStatement": null,
        "colour": 230,
        "tooltip": "",
        "helpUrl": ""
    },
    {
        "type": "dch",
        "message0": "DCH %1 VALUE %2 LIMIT %3",
        "args0": [
            {
                "type": "input_dummy"
            },
            {
                "type": "input_value",
                "name": "VALUE",
                "check": [
                    "Number",
                    "channel"
                ]
            },
            {
                "type": "input_statement",
                "name": "LIMIT"
            }
        ],
        "previousStatement": null,
        "nextStatement": null,
        "colour": 290,
        "tooltip": "",
        "helpUrl": ""
    },
    {
        "type": "registration",
        "message0": "%1",
        "args0": [
            {
                "type": "field_input",
                "name": "REGISTRATION",
                "text": "default"
            }
        ],
        "inputsInline": true,
        "previousStatement": null,
        "nextStatement": null,
        "colour": 230,
        "tooltip": "",
        "helpUrl": ""
    },
    {
        "type": "factor",
        "message0": "%1 * %2",
        "args0": [
            {
                "type": "input_value",
                "name": "FACTOR",
                "check": "Number"
            },
            {
                "type": "input_value",
                "name": "VALUE",
                "check": [
                    "Number",
                    "channel"
                ]
            }
        ],
        "inputsInline": true,
        "output": "Number",
        "colour": 230,
        "tooltip": "",
        "helpUrl": ""
    },
    {
        "type": "compare",
        "message0": "%1 %2 %3",
        "args0": [
            {
                "type": "field_dropdown",
                "name": "OPERATOR",
                "options": [
                    [
                        "<",
                        "LT"
                    ],
                    [
                        ">",
                        "GT"
                    ],
                    [
                        "<=",
                        "LTE"
                    ],
                    [
                        ">=",
                        "GTE"
                    ]
                ]
            },
            {
                "type": "input_value",
                "name": "FACTOR",
                "check": "Number"
            },
            {
                "type": "input_value",
                "name": "CHANNEL",
                "check": "channel"
            }
        ],
        "inputsInline": true,
        "output": "Boolean",
        "colour": 230,
        "tooltip": "",
        "helpUrl": ""
    },
    {
        "type": "and",
        "message0": "%1 & %2",
        "args0": [
            {
                "type": "input_value",
                "name": "LHS",
                "check": "Boolean"
            },
            {
                "type": "input_value",
                "name": "RHS",
                "check": "Boolean"
            }
        ],
        "inputsInline": true,
        "output": "Boolean",
        "colour": 230,
        "tooltip": "",
        "helpUrl": ""
    },
    {
        "type": "time",
        "message0": "%1 %2",
        "args0": [
            {
                "type": "field_number",
                "name": "VALUE",
                "value": 0
            },
            {
                "type": "field_dropdown",
                "name": "UNIT",
                "options": [
                    [
                        "sec",
                        "SECONDS"
                    ],
                    [
                        "min",
                        "MINUTES"
                    ],
                    [
                        "h",
                        "HOURS"
                    ]
                ]
            }
        ],
        "inputsInline": true,
        "output": "Boolean",
        "colour": 230,
        "tooltip": "",
        "helpUrl": ""
    },
    {
        "type": "channel",
        "message0": "%1",
        "args0": [
            {
                "type": "field_label_serializable",
                "name": "CHANNEL",
                "text": "channel"
            }
        ],
        "inputsInline": true,
        "output": "channel",
        "colour": 120,
        "tooltip": "",
        "helpUrl": ""
    },
    {
        "type": "variable",
        "message0": "%1",
        "args0": [
            {
                "type": "field_label_serializable",
                "name": "VARIABLE",
                "text": "variable"
            }
        ],
        "inputsInline": true,
        "output": "BTSVariable",
        "colour": 65,
        "tooltip": "",
        "helpUrl": ""
    },
    {
        "type": "assignment",
        "message0": "%1 = %2",
        "args0": [
            {
                "type": "field_variable",
                "name": "LHS",
                "variableTypes": ["BTSVariable"],
                "defaultType": "BTSVariable"
            },
            {
                "type": "field_number",
                "name": "RHS",
                "value": 0
            }
        ],
        "inputsInline": true,
        "previousStatement": null,
        "nextStatement": null,
        "colour": 65,
        "tooltip": "",
        "helpUrl": ""
    },
    {
        "type": "pau",
        "message0": "PAU %1 LIMIT %2",
        "args0": [
            {
                "type": "input_dummy"
            },
            {
                "type": "input_statement",
                "name": "LIMIT"
            }
        ],
        "previousStatement": null,
        "nextStatement": null,
        "colour": 290,
        "tooltip": "",
        "helpUrl": ""
    },
    {
        "type": "comment",
        "message0": "! %1",
        "args0": [
            {
                "type": "field_input",
                "name": "COMMENT",
                "text": "comment"
            }
        ],
        "previousStatement": null,
        "nextStatement": null,
        "colour": 180,
        "tooltip": "",
        "helpUrl": ""
    },
    {
        "type": "statement_mutator_container",
        "message0": "%1",
        "args0": [
            {
                "type": "input_statement",
                "name": "STACK"
            }
        ],
        "colour": 230,
        "tooltip": "",
        "helpUrl": ""
    },
    {
        "type": "statement_mutator_item",
        "message0": "%1",
        "args0": [
            {
                "type": "field_label_serializable",
                "name": "TYPE",
                "text": ""
            }
        ],
        "previousStatement": null,
        "nextStatement": null,
        "colour": 230,
        "tooltip": "",
        "helpUrl": ""
    }
]);


Blockly.Blocks['statement_asdf'] = {
    /**
     * Block for creating a list with any number of elements of any type.
     * @this {Block}
     */
    init: function () {
        this.valueCount_ = 1;
        this.limitCount_ = 0;
        this.registrationCount_ = 0;
        this.appendDummyInput()
            .appendField(new Blockly.FieldLabelSerializable("SET"), "OPERATOR");
        this.setInputsInline(false);
        this.setColour(230);
        this.updateShape_();
        // this.setOutput(true, 'BTSLine');
        this.setMutator(new Mutator(['statement_mutator_item']));
    },
    /**
     * Create XML to represent list inputs.
     * Backwards compatible serialization implementation.
     * @return {!Element} XML storage element.
     * @this {Block}
     */
    mutationToDom: function () {
        const container = xmlUtils.createElement('mutation');
        container.setAttribute('values', this.valueCount_);
        container.setAttribute('limits', this.limitCount_);
        container.setAttribute('registrations', this.registrationCount_);
        return container;
    },
    /**
     * Parse XML to restore the list inputs.
     * Backwards compatible serialization implementation.
     * @param {!Element} xmlElement XML storage element.
     * @this {Block}
     */
    domToMutation: function (xmlElement) {
        this.valueCount_ = parseInt(xmlElement.getAttribute('values'), 10);
        this.limitCount_ = parseInt(xmlElement.getAttribute('limits'), 10);
        this.registrationCount_ = parseInt(xmlElement.getAttribute('registrations'), 10);
        this.updateShape_();
    },
    /**
     * Returns the state of this block as a JSON serializable object.
     * @return {{itemCount: number}} The state of this block, ie the item count.
     */
    saveExtraState: function () {
        return {
            'valueCount': this.valueCount_,
            'limitCount': this.limitCount_,
            'registrationCount': this.registrationCount_,
        };
    },
    /**
     * Applies the given state to this block.
     * @param {*} state The state to apply to this block, ie the item count.
     */
    loadExtraState: function (state) {
        this.valueCount_ = state['valueCount'];
        this.limitCount_ = state['limitCount'];
        this.registrationCount_ = state['registrationCount'];
        this.updateShape_();
    },
    /**
     * Populate the mutator's dialog with this block's components.
     * @param {!Workspace} workspace Mutator's workspace.
     * @return {!Block} Root block in mutator.
     * @this {Block}
     */
    decompose: function (workspace) {
        const containerBlock = workspace.newBlock('statement_mutator_container');
        containerBlock.initSvg();
        let connection = containerBlock.getInput('STACK').connection;
        for (let i = 0; i < this.valueCount_; i++) {
            const itemBlock = workspace.newBlock('statement_mutator_item');
            itemBlock.initSvg();
            connection.connect(itemBlock.previousConnection);
            connection = itemBlock.nextConnection;
        }
        for (let i = 0; i < this.limitCount_; i++) {
            const itemBlock = workspace.newBlock('statement_mutator_item');
            itemBlock.initSvg();
            connection.connect(itemBlock.previousConnection);
            connection = itemBlock.nextConnection;
        }
        for (let i = 0; i < this.registrationCount_; i++) {
            const itemBlock = workspace.newBlock('statement_mutator_item');
            itemBlock.initSvg();
            connection.connect(itemBlock.previousConnection);
            connection = itemBlock.nextConnection;
        }
        return containerBlock;
    },
    /**
     * Reconfigure this block based on the mutator dialog's components.
     * @param {!Block} containerBlock Root block in mutator.
     * @this {Block}
     */
    compose: function (containerBlock) {
        let itemBlock = containerBlock.getInputTargetBlock('STACK');
        // Count number of inputs.
        const connections = [];
        while (itemBlock && !itemBlock.isInsertionMarker()) {
            connections.push(itemBlock.valueConnection_);
            itemBlock =
                itemBlock.nextConnection && itemBlock.nextConnection.targetBlock();
        }
        // Disconnect any children that don't belong.
        // for (let i = 0; i < this.itemCount_; i++) {
        //     const connection = this.getInput('ADD' + i).connection.targetConnection;
        //     if (connection && connections.indexOf(connection) === -1) {
        //         connection.disconnect();
        //     }
        // }
        this.valueCount_ = connections.length;
        this.updateShape_();
        // Reconnect any child blocks.
        // for (let i = 0; i < this.itemCount_; i++) {
        //     Mutator.reconnect(connections[i], this, 'ADD' + i);
        // }
    },
    /**
     * Store pointers to any connected child blocks.
     * @param {!Block} containerBlock Root block in mutator.
     * @this {Block}
     */
    // saveConnections: function (containerBlock) {
    //     let itemBlock = containerBlock.getInputTargetBlock('STACK');
    //     let i = 0;
    //     while (itemBlock) {
    //         const input = this.getInput('ADD' + i);
    //         itemBlock.valueConnection_ = input && input.connection.targetConnection;
    //         itemBlock =
    //             itemBlock.nextConnection && itemBlock.nextConnection.targetBlock();
    //         i++;
    //     }
    // },
    /**
     * Modify this block to have the correct number of inputs.
     * @private
     * @this {Block}
     */
    updateShape_: function () {
        // Add new inputs.
        for (let i = 0; i < this.valueCount_; i++) {
            if (!this.getInput('VALUE' + i)) {
                const input = this.appendValueInput('VALUE' + i).setAlign(Align.RIGHT);
            }
        }
        // Remove deleted inputs.
        for (let i = this.valueCount_; this.getInput('VALUE' + i); i++) {
            this.removeInput('VALUE' + i);
        }
    },
};
