#! /bin/bash

# generate parser
node generate/generate_parser.js parser/bmgen.pegjs > parser/bmgen_parser.js

# generate toolbox module
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

# generate blocks module
cat << EOF > custom/blocks.js
goog.module("BMGen3000.Blocks");

EOF

cat custom/blockly_developer_tools/bmgen_blocks.js >> custom/blocks.js

# generate dependencies for closure compiler
./node_modules/.bin/closure-make-deps -f bmgen3000.js -r bts600/ -r custom/ -r parser --closure-path blockly/closure/goog/ > deps.js

# make compressed version
mkdir -p ./public
mkdir -p ./public/blockly
mkdir -p ./public/blockly/msg/js

cp ./blockly/blockly_compressed.js ./public/blockly/
cp ./blockly/javascript_compressed.js ./public/blockly/
cp ./blockly/blocks_compressed.js ./public/blockly/
cp ./blockly/msg/js/en.js ./public/blockly/msg/js/
cp ./index.html ./public/

find ./custom/ ./bts600/ ./parser/ -name '*.js' | xargs google-closure-compiler --entry_point goog:BMGen3000 --js_output_file public/main.js bmgen3000.js