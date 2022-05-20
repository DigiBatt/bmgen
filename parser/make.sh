#! /bin/bash

lex bts600.lex
yacc -d bts600.yacc
gcc lex.yy.c y.tab.c -o bts600
