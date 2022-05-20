%{
#include "bts600.h"
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

void yyerror(program **retprogram, char *s)
{
  fprintf(stderr, "%s\n",s);
}
%}

%parse-param {program **retprogram}

%token FLOAT ID COMP ASSIGN MATHOP COMMENT WHITESPACE SEMICOLON KW_VALUE KW_LIMIT KW_ACTION KW_REGISTRATION KW_GOTO KW_ERR

%union
{
    float floatValue;
    char *stringValue;
    numvalue *numvaluevalue;
    value_expr *valueexprvalue;
    action *actionvalue;
    limit *limitvalue;
    registration *registrationvalue;
    args *argsvalue;
    stat *statvalue;
    program *programvalue;
}

%type <floatValue> FLOAT
%type <stringValue> ID
%type <stringValue> COMP
%type <stringValue> COMMENT
%type <numvaluevalue> numvalue
%type <valueexprvalue> value_expr
%type <actionvalue> action
%type <limitvalue> limit
%type <registrationvalue> registration
%type <argsvalue> args
%type <statvalue> stat
%type <programvalue> program
%type <stringValue> operator
%type <valueexprvalue> value

%start program

%%

program:    stat
            {
                program *x = malloc(sizeof(program));
                *retprogram = x;
                x->statvalue = malloc(sizeof(stat*));
                x->statvalue[0] = $1;
                x->statcount = 1;
                $$ = x;
            }
             |
            program stat
            {
                program *x = $1;
                x->statvalue = realloc(x->statvalue, sizeof(stat*) * (x->statcount + 1));
                x->statvalue[x->statcount] = $2;
                x->statcount++;
                $$ = x;
            }
             ;
         
stat:       COMMENT
            {
                stat *x = malloc(sizeof(stat));
                x->operatorvalue = $1;
                x->argsvalue = 0;
                $$ = x;
            }
             |
            operator args SEMICOLON
            {
                stat *x = malloc(sizeof(stat));
                x->operatorvalue = $1;
                x->argsvalue = $2;
                $$ = x;
            }
             ;

operator:   ID
            {
                $$ = $1;
            }
             ;
             
args:       value limit
            {
                args *x = malloc(sizeof(args));
                x->valueexprvalue = $1;
                x->limitvalue = $2;
                x->registrationvalue = 0;
                $$ = x;
            }
             |
            value
            {
                args *x = malloc(sizeof(args));
                x->valueexprvalue = $1;
                x->limitvalue = 0;
                x->registrationvalue = 0;
                $$ = x;
            }
             |
            limit
            {
                args *x = malloc(sizeof(args));
                x->valueexprvalue = 0;
                x->limitvalue = $1;
                x->registrationvalue = 0;
                $$ = x;
            }
             |
            registration
            {
                args *x = malloc(sizeof(args));
                x->valueexprvalue = 0;
                x->limitvalue = 0;
                x->registrationvalue = $1;
                $$ = x;
            }
            |
                                /* empty */
            {
                args *x = malloc(sizeof(args));
                x->valueexprvalue = 0;
                x->limitvalue = 0;
                x->registrationvalue = 0;
                $$ = x;
            }
             ;
             
value:      KW_VALUE value_expr
            {
                $$ = $2;
            }
             ;

value_expr: ID ASSIGN numvalue
            {
                value_expr *x = malloc(sizeof(value_expr));
                x->type = value_expr_assigntype;
                x->idvalue = $1;
                x->numvaluevalue = $3;
                $$ = x;
            }
             |
            numvalue
            {
                value_expr *x = malloc(sizeof(value_expr));
                x->type = value_expr_numvaluetype;
                x->numvaluevalue = $1;
                $$ = x;
            }
             |
            numvalue '*'
            {
                value_expr *x = malloc(sizeof(value_expr));
                x->type = value_expr_cycletype;
                x->numvaluevalue = $1;
                $$ = x;
            }
             ;

numvalue:   ID
            {
                numvalue *x = malloc(sizeof(numvalue));
                x->type = numvalue_idtype;
                x->idvalue = malloc(strlen($1) + 1);
                strcpy(x->idvalue, $1);
                $$ = x;
            }
             |
            FLOAT
            {
                numvalue *x = malloc(sizeof(numvalue));
                x->type = numvalue_floattype;
                x->floatvalue = $1;
                $$ = x;
            }
             |
            numvalue numvalue
            {
                numvalue *x = malloc(sizeof(numvalue));
                x->type = numvalue_multype;
                x->mulvalue[0] = $1;
                x->mulvalue[1] = $2;
                $$ = x;
            }
             ;
             
limit:      KW_LIMIT COMP numvalue
            {
                limit *x = malloc(sizeof(limit));
                x->operatorvalue = $2;
                x->numvaluevalue = $3;
                x->actionvalue = 0;
                $$ = x;
            }
             |
            KW_LIMIT COMP numvalue action
            {
                limit *x = malloc(sizeof(limit));
                x->operatorvalue = $2;
                x->numvaluevalue = $3;
                x->actionvalue = $4;
                $$ = x;
            }
             ;

action:     KW_ACTION KW_ERR FLOAT
            {
                action *x = malloc(sizeof(action));
                x->type = action_errtype;
                x->errvalue = $3;
                $$ = x;
            }
             |
            KW_ACTION KW_GOTO ID
            {
                action *x = malloc(sizeof(action));
                x->type = action_gototype;
                x->gotovalue = $3;
                $$ = x;
            }
             ;
             
registration:   KW_REGISTRATION numvalue
                {
                    registration *x = malloc(sizeof(registration));
                    x->numvaluevalue = $2;
                    $$ = x;
                }
                 ;
                 
%%

/*
int main()
{
    program *retprogram;
    return(yyparse(&retprogram));
}
*/