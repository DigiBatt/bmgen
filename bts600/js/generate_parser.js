'use strict';

let grammar_file = process.argv[2];

const fs = require('fs');
const peg = require('pegjs');

let grammar = fs.readFileSync(grammar_file).toString();
const parser = peg.generate(grammar, { "output": "source", "format": "globals", "exportVar": "BMGenParser" });
console.log(parser);
