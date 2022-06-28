#! /bin/bash

node parser/generate_parser.js parser/bmgen.pegjs > parser/bmgen_parser.js

cat << EOF > custom/toolbox/toolbox.js
goog.module("BMGen3000.Toolbox");
const parser = new DOMParser();
var toolbox = parser.parseFromString(\`
EOF

cat custom/blockly_developer_tools/bmgen_toolbox.xml >> custom/toolbox/toolbox.js

cat << EOF >> custom/toolbox/toolbox.js
\`, 'application/xml');
exports = { toolbox };
EOF

./node_modules/.bin/closure-make-deps -f bmgen3000.js -r bts600/ -r custom/ -r parser --closure-path blockly/closure/goog/ > deps.js