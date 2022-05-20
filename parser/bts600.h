typedef struct _numvalue {
  enum {
    numvalue_idtype,
    numvalue_floattype,
    numvalue_multype,
  } type;
  union {
    char *idvalue;
    double floatvalue;
    struct _numvalue *mulvalue[2];
  };
} numvalue;

typedef struct {
  enum {
    value_expr_assigntype,
    value_expr_numvaluetype,
    value_expr_cycletype,
  } type;
  char *idvalue;
  numvalue *numvaluevalue;
} value_expr;

typedef struct {
  enum {
    action_errtype,
    action_gototype,
  } type;
  union {
    int errvalue;
    char *gotovalue;
  };
} action;

typedef struct {
  char *operatorvalue;
  numvalue *numvaluevalue;
  action *actionvalue;
} limit;

typedef struct {
  numvalue *numvaluevalue;
} registration;

typedef struct {
  value_expr *valueexprvalue;
  limit *limitvalue;
  registration *registrationvalue;
} args;

typedef struct {
  char *operatorvalue;
  args *argsvalue;
} stat;

typedef struct {
  stat **statvalue;
  int statcount;
} program;