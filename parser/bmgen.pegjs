program =
	_ statements:(statement _)* { return statements.map(x => x[0]); }
    
statement =
    x:assignment { return x; }
    / x:limit_global { return x; }
    / x:function { return x; }
    / cycle
    / comment
    
cycle =
	"cycle" _ "(" _ count:INT _ ")" _ "{" program:program "}" { return {'type': 'cycle', 'count': count, 'program': program}; }
    
limit_global =
	"limit" _ "(" args:argslist ")" _ ";" { return {'type': 'limit_global', 'args': args}; }
    
limit =
	"limit" _ "(" args:argslist ")" { return {'type': 'limit', 'args': args}; }
    
error =
	"error" _ "(" errnum:INT ")" { return {'type': 'error', 'errnum': errnum}; }
    
function =
	name:ID _ "(" args:argslist ")" _ ";" { return {'type': 'function', 'name': name, 'args': args}; }
    
argslist =
	x0:arg? x:(_ "," _ arg)* { return x ? [x0, ...(x.map(elem => elem[3]))] : x0  }
    
arg =
	setvalue
    / comparison
    / time
    / limit
    / error
    / numvalue

assignment =
	lhs:variable _ "=" _ rhs:numvalue _ ";" { return {'type': 'assignment', 'lhs': lhs, 'rhs': rhs}; }
    
setvalue =
	lhs:channel _ "=" _ rhs:numvalue { return {'type': 'setvalue', 'lhs': lhs, 'rhs': rhs}; }
    
comparison =
	lhs:channel _ operator:COMPARE _ rhs:numvalue { return {'type': 'comparison', 'lhs': lhs, 'rhs': rhs, 'operator': operator}; }
    
comment =
	"//" text:$([^\n]*) { return {'type': 'comment', 'text': text}; }
	
time =
	value:numvalue _ unit:TIMEUNIT { return {'type': 'time', 'value': value, 'unit': unit}; }
    
numvalue =
	variable
    / number
    
variable =
	name:ID { return {'type': 'variable', 'name': name}; }
    
channel =
	name:ID { return {'type': 'channel', 'name': name}; }
    
number =
	value:FLOAT { return {'type': 'number', 'value': value}; }

TIMEUNIT = $("sec" / "min" / "h")
COMPARE = $([><]"="?)
INT = $("-"?[0-9]+)
FLOAT = $("-"?[0-9]+(.[0-9]+)?)
ID = $([A-Za-z][A-Za-z0-9]*)
_ = $([ \t\r\n]*)