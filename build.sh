cd "$(dirname $0)"
./build_docs.sh

cd "$(dirname $0)/src/bmgen/web/client"
npm install
npm run build
