cd "$(dirname $0)"
sphinx-apidoc -o ./sphinx/bmgen ./src
make -C ./sphinx html

mkdir -p ./src/bmgen/web/client/public/docs
cp -rT ./sphinx/_build/html ./src/bmgen/web/client/public/docs
cp -rT ./examples ./src/bmgen/web/client/public/examples