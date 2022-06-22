program =
	_ statements:(statement _)* { return statements.map(x => x[0]); }
    
statement =
    x:assignment ";" { return x; }
    / x:function ";" { return x; }
    / cycle
    / comment
    
cycle =
	"cycle" _ "(" _ count:numvalue _ ")" _ "{" program:program "}" { return {'type': 'cycle', 'count': count, 'program': program}; }
    
limit =
	"limit" _ "(" args:argslist ")" { return {'type': 'limit', 'args': args}; }
    
error =
	"error" _ "(" args:argslist ")" { return {'type': 'error', 'args': args}; }
    
function =
	name:ID _ "(" args:argslist ")" { return {'type': 'function', 'name': name, 'args': args}; }
    
argslist =
	x0:arg? x:(_ "," _ arg)* { return x ? [x0, ...(x.map(elem => elem[3]))] : x0  }
    
arg =
	assignment
    / comparison
    / time
    / limit
    / error
    / numvalue

assignment =
	lhs:ID _ "=" _ rhs:numvalue { return {'type': 'assignment', 'lhs': lhs, 'rhs': rhs}; }
    
comparison =
	lhs:numvalue _ operator:COMPARE _ rhs:numvalue { return {'type': 'comparison', 'lhs': lhs, 'rhs': rhs, 'operator': operator}; }
    
comment =
	"//" text:$([^\n]*) { return {'type': 'comment', 'text': text}; }
	
time =
	value:numvalue _ unit:TIMEUNIT { return {'type': 'time', 'value': value, 'unit': unit}; }
    
numvalue =
	ID
    / FLOAT

TIMEUNIT = $("sec" / "min" / "h")
COMPARE = $([><]"="?)
INT = $("-"?[0-9]+)
FLOAT = $("-"?[0-9]+(.[0-9]+)?)
ID = $([A-Za-z][A-Za-z0-9]*)
_ = $([ \t\r\n]*)