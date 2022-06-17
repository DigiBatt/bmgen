#include "bts600.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *strarray_to_str(int size, char **in, char *sep)
{
    int *len = malloc(sizeof(int) * size);
    int total_len = 0;
    for (int i = 0; i < size; i++)
    {
        len[i] = strlen(in[i]);
        total_len += len[i];
    }
    int sep_len = 0;
    if (sep)
    {
        sep_len = strlen(sep);
        total_len += sep_len * (size - 1);
    }
    char *out = malloc(sizeof(char) * (total_len + 1));
    total_len = 0;
    for (int i = 0; i < size; i++)
    {
        strcpy(out + total_len, in[i]);
        total_len += len[i];
        if (sep && i < (size - 1))
        {
            strcpy(out + total_len, sep);
            total_len += sep_len;
        }
    }
    return out;
}

char *numvalue_to_json(numvalue *x)
{
    int arraysize = 5;
    if (x->type == numvalue_multype)
    {
        arraysize = 7;
    }
    char **stringparts = malloc(sizeof(char *) * arraysize);
    stringparts[0] = "{\"type\": \"";
    switch (x->type)
    {
    case numvalue_idtype:
        stringparts[1] = "variable";
        stringparts[2] = "\", \"name\": \"";
        stringparts[3] = x->idvalue;
        stringparts[4] = "\"}";
        break;
    case numvalue_floattype:
        stringparts[1] = "number";
        stringparts[2] = "\", \"value\": ";
        stringparts[3] = malloc(sizeof(char) * 10);
        snprintf(stringparts[3], 10, "%f", x->floatvalue);
        stringparts[4] = "}";
        break;
    case numvalue_multype:
        stringparts[1] = "multiplication";
        stringparts[2] = "\", \"lhs\": ";
        stringparts[3] = numvalue_to_json(x->mulvalue[0]);
        stringparts[4] = ", \"rhs\": ";
        stringparts[5] = numvalue_to_json(x->mulvalue[1]);
        stringparts[6] = "}";
        break;
    }
    char *out = strarray_to_str(arraysize, stringparts, 0);
    if (x->type == numvalue_floattype)
    {
        free(stringparts[3]);
    }
    else if (x->type == numvalue_multype)
    {
        free(stringparts[3]);
        free(stringparts[5]);
    }
    return out;
}

char *valueexpr_to_json(value_expr *x)
{
    if (x == 0)
    {
        return strdup("{}");
    }
    int arraysize = 5;
    if (x->type == value_expr_assigntype)
    {
        arraysize = 7;
    }
    char **stringparts = malloc(sizeof(char *) * arraysize);
    stringparts[0] = "{\"type\": \"";
    switch (x->type)
    {
    case value_expr_assigntype:
        stringparts[1] = "assignment";
        break;
    case value_expr_numvaluetype:
        stringparts[1] = "numeric";
        break;
    case value_expr_cycletype:
        stringparts[1] = "cycles";
        break;
    }
    stringparts[2] = "\", \"value\": ";
    stringparts[3] = numvalue_to_json(x->numvaluevalue);
    if (x->type == value_expr_assigntype)
    {
        stringparts[4] = ", \"target\": \"";
        stringparts[5] = x->idvalue;
        stringparts[6] = "\"}";
    }
    else
    {
        stringparts[4] = "}";
    }
    char *out = strarray_to_str(arraysize, stringparts, 0);
    free(stringparts[3]);
    if (x->type == value_expr_assigntype)
    {
        free(stringparts[5]);
    }
    return out;
}

char *action_to_json(action *x)
{
    if (x == 0)
    {
        return strdup("{}");
    }
    char **stringparts = malloc(sizeof(char *) * 3);
    switch (x->type)
    {
    case action_errtype:
        stringparts[0] = "{\"type\": \"error\", \"number\": ";
        stringparts[1] = malloc(sizeof(char) * 10);
        snprintf(stringparts[1], 10, "%i", x->errvalue);
        stringparts[2] = "}";
        break;
    case action_gototype:
        stringparts[0] = "{\"type\": \"goto\", \"label\": \"";
        stringparts[1] = x->gotovalue;
        stringparts[2] = "\"}";
        break;
    }
    char *out = strarray_to_str(3, stringparts, 0);
    if (x->type == action_errtype)
    {
        free(stringparts[1]);
    }
    return out;
}

char *limit_to_json(limit *x)
{
    if (x == 0)
    {
        return strdup("{}");
    }
    char **stringparts = malloc(sizeof(char *) * 7);
    stringparts[0] = "{\"operator\": \"";
    stringparts[1] = x->operatorvalue;
    stringparts[2] = "\", \"value\": ";
    stringparts[3] = numvalue_to_json(x->numvaluevalue);
    stringparts[4] = ", \"action\": ";
    stringparts[5] = action_to_json(x->actionvalue);
    stringparts[6] = "}";
    char *out = strarray_to_str(7, stringparts, 0);
    free(stringparts[3]);
    free(stringparts[5]);
    return out;
}

char *registration_to_json(registration *x)
{
    if (x == 0)
    {
        return strdup("{}");
    }
    char **stringparts = malloc(sizeof(char *) * 3);
    stringparts[0] = "{\"value\": ";
    stringparts[1] = numvalue_to_json(x->numvaluevalue);
    stringparts[2] = "}";
    char *out = strarray_to_str(3, stringparts, 0);
    free(stringparts[1]);
    return out;
}

char *valuelist_to_text(valuelist *x)
{
    if (x == 0)
    {
        return strdup("[]");
    }
    int size = x->valueexprcount;
    char **stringparts = malloc(sizeof(char *) * size);
    for (int i = 0; i < x->valueexprcount; i++)
    {
        stringparts[i] = valueexpr_to_json(x->valueexprvalue[i]);
    }
    char *array = strarray_to_str(size, stringparts, ", ");
    for (int i = 0; i < x->valueexprcount; i++)
    {
        free(stringparts[i]);
    }
    char *allparts[] = {"[", array, "]"};
    char *out = strarray_to_str(3, allparts, 0);
    free(allparts[1]);
    return out;
}

char *limitlist_to_json(limitlist *x)
{
    if (x == 0)
    {
        return strdup("[]");
    }
    int size = x->limitcount;
    char **stringparts = malloc(sizeof(char *) * size);
    for (int i = 0; i < x->limitcount; i++)
    {
        stringparts[i] = limit_to_json(x->limitvalue[i]);
    }
    char *array = strarray_to_str(size, stringparts, ", ");
    for (int i = 0; i < x->limitcount; i++)
    {
        free(stringparts[i]);
    }
    char *allparts[] = {"[", array, "]"};
    char *out = strarray_to_str(3, allparts, 0);
    free(allparts[1]);
    return out;
}

char *args_to_text(args *x)
{
    if (x == 0)
    {
        return strdup("{}");
    }
    char **stringparts = malloc(sizeof(char *) * 7);
    stringparts[0] = "{\"value\": ";
    stringparts[1] = valuelist_to_text(x->valuelistvalue);
    stringparts[2] = ", \"limit\": ";
    stringparts[3] = limitlist_to_json(x->limitlistvalue);
    stringparts[4] = ", \"registration\": ";
    stringparts[5] = registration_to_json(x->registrationvalue);
    stringparts[6] = "}";
    char *out = strarray_to_str(7, stringparts, 0);
    free(stringparts[1]);
    free(stringparts[3]);
    free(stringparts[5]);
    return out;
}

char *line_to_text(line *x)
{
    char **stringparts = malloc(sizeof(char *) * 5);
    stringparts[0] = "{\"operator\": \"";
    stringparts[1] = x->statvalue.operatorvalue;
    stringparts[2] = "\", \"args\": ";
    stringparts[3] = args_to_text(x->statvalue.argsvalue);
    stringparts[4] = "}";
    char *out = strarray_to_str(5, stringparts, 0);
    free(stringparts[1]);
    free(stringparts[3]);
    return out;
}

char *program_to_text(program *x)
{
    char **stringparts = malloc(sizeof(char *) * (x->linecount));
    for (int i = 0; i < x->linecount; i++)
    {
        stringparts[i] = line_to_text(x->linevalue[i]);
    }
    char *joined = strarray_to_str(x->linecount, stringparts, "\n");
    for (int i = 0; i < x->linecount; i++)
    {
        free(stringparts[i]);
    }
    return joined;
}

int main()
{
    program *p;
    int retvalue = yyparse(&p);
    if (retvalue == 1)
    {
        fprintf(stderr, "Syntax error");
        return 1;
    }
    if (retvalue == 2)
    {
        fprintf(stderr, "Out of memory");
        return 2;
    }
    char *text = program_to_text(p);
    puts(text);
    free(text);
    return 0;
}