#include "bts600.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *strarray_to_str(int size, char **in)
{
    int *len = malloc(sizeof(int) * size);
    int total_len = 0;
    for (int i = 0; i < size; i++)
    {
        if (in[i] == 0)
        {
            len[i] = 0;
        }
        else
        {
            len[i] = strlen(in[i]);
            total_len += len[i];
        }
    }
    char *out = malloc(sizeof(char) * (total_len + 1));
    total_len = 0;
    for (int i = 0; i < size; i++)
    {
        if (len[i] > 0)
        {
            strcpy(out + total_len, in[i]);
            total_len += len[i];
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
    stringparts[0] = "{'type': '";
    switch (x->type)
    {
    case numvalue_idtype:
        stringparts[1] = "variable";
        stringparts[2] = "', 'name': '";
        stringparts[3] = x->idvalue;
        stringparts[4] = "'}";
        break;
    case numvalue_floattype:
        stringparts[1] = "number";
        stringparts[2] = "', 'value': ";
        stringparts[3] = malloc(sizeof(char) * 10);
        snprintf(stringparts[3], 10, "%f", x->floatvalue);
        stringparts[4] = "}";
        break;
    case numvalue_multype:
        stringparts[1] = "multiplication";
        stringparts[2] = "', 'lhs': ";
        stringparts[3] = numvalue_to_json(x->mulvalue[0]);
        stringparts[4] = ", 'rhs': ";
        stringparts[5] = numvalue_to_json(x->mulvalue[0]);
        stringparts[6] = "}";
        break;
    }
    char *out = strarray_to_str(arraysize, stringparts);
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
    stringparts[0] = "{'type': '";
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
    stringparts[2] = "', 'value': ";
    stringparts[3] = numvalue_to_json(x->numvaluevalue);
    if (x->type == value_expr_assigntype)
    {
        stringparts[4] = ", 'target': '";
        stringparts[5] = x->idvalue;
        stringparts[6] = "}";
    }
    else
    {
        stringparts[4] = "}";
    }
    char *out = strarray_to_str(arraysize, stringparts);
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
        stringparts[0] = "{'type': 'error', 'number': ";
        stringparts[1] = malloc(sizeof(char) * 10);
        snprintf(stringparts[1], 10, "%i", x->errvalue);
        stringparts[2] = "}";
        break;
    case action_gototype:
        stringparts[0] = "{'type': 'goto', 'label': '";
        stringparts[1] = x->gotovalue;
        stringparts[2] = "'}";
        break;
    }
    char *out = strarray_to_str(3, stringparts);
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
    stringparts[0] = "{'operator': '";
    stringparts[1] = x->operatorvalue;
    stringparts[2] = "', 'value': ";
    stringparts[3] = numvalue_to_json(x->numvaluevalue);
    stringparts[4] = ", 'action': ";
    stringparts[5] = action_to_json(x->actionvalue);
    stringparts[6] = "}";
    char *out = strarray_to_str(7, stringparts);
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
    stringparts[0] = "{'value': ";
    stringparts[1] = numvalue_to_json(x->numvaluevalue);
    stringparts[2] = "}";
    char *out = strarray_to_str(3, stringparts);
    free(stringparts[1]);
    return out;
}

char *valuelist_to_json(valuelist *x)
{
    if (x == 0)
    {
        return strdup("[]");
    }
    int size = x->valueexprcount + 2;
    char **stringparts = malloc(sizeof(char *) * size);
    stringparts[0] = "[";
    for (int i = 0; i < x->valueexprcount; i++)
    {
        stringparts[i + 1] = valueexpr_to_json(x->valueexprvalue[i]);
    }
    stringparts[size - 1] = "]";
    char *out = strarray_to_str(size, stringparts);
    for (int i = 0; i < x->valueexprcount; i++)
    {
        free(stringparts[i + 1]);
    }
    return out;
}

char *limitlist_to_json(limitlist *x)
{
    if (x == 0)
    {
        return strdup("[]");
    }
    int size = x->limitcount + 2;
    char **stringparts = malloc(sizeof(char *) * size);
    stringparts[0] = "[";
    for (int i = 0; i < x->limitcount; i++)
    {
        stringparts[i + 1] = limit_to_json(x->limitvalue[i]);
    }
    stringparts[size - 1] = "]";
    char *out = strarray_to_str(size, stringparts);
    for (int i = 0; i < x->limitcount; i++)
    {
        free(stringparts[i + 1]);
    }
    return out;
}

char *args_to_json(args *x)
{
    if (x == 0)
    {
        return strdup("{}");
    }
    char **stringparts = malloc(sizeof(char *) * 7);
    stringparts[0] = "{'value': ";
    stringparts[1] = valuelist_to_json(x->valuelistvalue);
    stringparts[2] = ", 'limit': ";
    stringparts[3] = limitlist_to_json(x->limitlistvalue);
    stringparts[4] = ", 'registration': ";
    stringparts[5] = registration_to_json(x->registrationvalue);
    stringparts[6] = "}";
    char *out = strarray_to_str(7, stringparts);
    free(stringparts[1]);
    free(stringparts[3]);
    free(stringparts[5]);
    return out;
}

char *stat_to_json(stat *x)
{
    char **stringparts = malloc(sizeof(char *) * 5);
    stringparts[0] = "{'operator': '";
    stringparts[1] = x->operatorvalue;
    stringparts[2] = "', 'args': ";
    stringparts[3] = args_to_json(x->argsvalue);
    stringparts[4] = "}";
    char *out = strarray_to_str(5, stringparts);
    free(stringparts[1]);
    free(stringparts[3]);
    return out;
}

char *program_to_json(program *x)
{
    const char *pre = "{'statements': [";
    const char *post = "]}";
    char **stringparts = malloc(sizeof(char *) * (x->statcount + 2));
    stringparts[0] = pre;
    for (int i = 0; i < x->statcount; i++)
    {
        stringparts[i + 1] = stat_to_json(x->statvalue[i]);
    }
    stringparts[x->statcount + 1] = post;
    char *out = strarray_to_str(x->statcount + 2, stringparts);
    for (int i = 0; i < x->statcount; i++)
    {
        free(stringparts[i + 1]);
    }
    return out;
}

int main()
{
    program *p;
    int retvalue = yyparse(&p);
    if (retvalue == 1)
    {
        printf("Syntax error");
        return 1;
    }
    if (retvalue == 2)
    {
        printf("Out of memory");
        return 2;
    }
    char *json = program_to_json(p);
    puts(json);
    free(json);
    return 0;
}