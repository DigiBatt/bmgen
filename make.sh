#! /bin/bash

node bts600/js/generate_parser.js parser/bmgen.pegjs > parser/bmgen_parser.js

cat << EOF > custom/toolbox/toolbox.js
const parser = new DOMParser();
var toolbox = parser.parseFromString(\`
EOF

cat custom/blockly_developer_tools/bmgen_toolbox.xml >> custom/toolbox/toolbox.js

cat << EOF >> custom/toolbox/toolbox.js
\`, 'application/xml');
EOF