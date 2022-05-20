#! /bin/bash

lex bts600.lex
yacc -d bts600.yacc
gcc -ggdb lex.yy.c y.tab.c bts600_to_json.c -o bts600_to_json
