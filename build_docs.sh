cd "$(dirname $0)"
sphinx-apidoc -o ./sphinx/bmgen ./src
make -C ./sphinx html