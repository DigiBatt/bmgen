%{
#include "bts600.h"
#include "y.tab.h"
%}

%option noyywrap

KW_VALUE (?i:VALUE)
KW_LIMIT (?i:LIMIT)
KW_ACTION (?i:ACTION)
KW_REGISTRATION (?i:REGISTRATION)
KW_GOTO (?i:GOTO)
KW_ERR (?i:ERR)
DIGIT [0-9]
FLOAT -?{DIGIT}(.{DIGIT}+)?
ID [A-Za-z][A-Za-z0-9]*
COMP [><]=?
ASSIGN =
MATHMUL [*]
COMMENT ^[ \t]*!.*
WHITESPACE [ \t\r\n]*

%%

{COMMENT}     {
                yylval.stringValue = strdup(yytext);
                return(COMMENT);
              }

{KW_VALUE}    {
                return(KW_VALUE);
              }

{KW_LIMIT}    {
                return(KW_LIMIT);
              }

{KW_ACTION}   {
                return(KW_ACTION);
              }

{KW_GOTO}     {
                return(KW_GOTO);
              }

{KW_ERR}      {
                return(KW_ERR);
              }

{KW_REGISTRATION}    {
                        return(KW_REGISTRATION);
                      }

{FLOAT}       {
                yylval.floatValue = atof(yytext);
                return(FLOAT);
              }

{ID}          {
                yylval.stringValue = strdup(yytext);
                return(ID);
              }

{COMP}        {
                yylval.stringValue = strdup(yytext);
                return(COMP);
              }

{ASSIGN}      {
                return(ASSIGN);
              }

{MATHMUL}     {
                return(MATHMUL);
              }
              
[;]           {
                return(SEMICOLON);
              }

{WHITESPACE}  {}

%%