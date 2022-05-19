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
                "name": "COUNT",
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
        "output": "Number",
        "colour": 65,
        "tooltip": "",
        "helpUrl": ""
    },
    {
        "type": "assignment",
        "message0": "%1 = %2",
        "args0": [
            {
                "type": "input_value",
                "name": "LHS",
                "check": "Number"
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
    }
]);