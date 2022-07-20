program =
	_ lines:(line _)* { return lines.map(x => x[0]); }
    
line =
    statement:statement _ ";" { return statement; }
    / cycle
    / while
    / for
    / comment
    / label

statement =
    assignment
    / limit_global
    / registration_global
    / function
    / math

cycle =
	"cycle" _ "(" _ count:INT _ ")" _ "{" program:program "}" { return {'type': 'cycle', 'count': count, 'program': program}; }

while =
	"while" _ "(" _ condition:limit_condition _ ")" _ "{" _ program:program _ "}" { return {'type': 'while', 'condition': condition, 'program': program}; }

for =
	"for" _ "(" _ init_statement:statement _ ";" _ condition:limit_condition _ ";" _ loop_statement:statement _ ")" _ "{" _ program:program _ "}" { return {'type': 'for', 'init_statement': init_statement, 'condition': condition, 'loop_statement': loop_statement, 'program': program}; }

limit_global =
	lim:limit { lim.type = 'limit_global'; return lim; }
    
limit =
	"limit" _ "(" condition:limit_condition action:(_ "," _ limit_action)? ")" { return {'type': 'limit', 'condition': condition, 'action': action ? action[3] : null}; }
    
limit_action =
	error
    / goto
    
error =
	"error" _ "(" errnum:INT ")" { return {'type': 'error', 'errnum': errnum}; }
    
goto =
	"goto" _ "(" label:ID ")" { return {'type': 'goto', 'label': label}; }

registration_global =
	reg:registration { reg.type = 'registration_global'; return reg; }

registration =
	"registration" _ "(" args:regargslist ")" { return {'type': 'registration', 'args': args}; }
    
function =
	name:ID _ "(" args:argslist ")" { return {'type': 'function', 'name': name, 'args': args}; }
    
argslist =
	x0:arg? x:(_ "," _ arg)* { return x0 ? [x0, ...(x.map(elem => elem[3]))] : [] }
    
regargslist =
	x0:regarg? x:(_ "," _ regarg)* { return x0 ? [x0, ...(x.map(elem => elem[3]))] : []  }

limit_condition =
	limit_and
	/ comparison
    / time
    
limit_and =
	lhs:(comparison / time) _ "&" _ rhs:limit_condition { return {'type': 'limit_and', 'lhs': lhs, 'rhs': rhs}; }

arg =
	setvalue
    / setvalue_equal
    / comparison
    / time
    / limit
    / registration
    / error
    / numvalue
    
regarg =
	regname
    / comparison
    / time
    / setvalue

assignment =
	lhs:(array_access / variable) _ "=" _ rhs:(numvalue / array_init) { return {'type': 'assignment', 'lhs': lhs, 'rhs': rhs}; }
    
setvalue =
	value:numvalue _ channel:channel { return {'type': 'setvalue', 'channel': channel, 'value': value}; }
    
setvalue_equal =
	channel:channel _ "=" _ value:numvalue { return {'type': 'setvalue_equal', 'channel': channel, 'value': value}; }
    
comparison =
	lhs:channel _ operator:COMPARE _ rhs:numvalue { return {'type': 'comparison', 'lhs': lhs, 'rhs': rhs, 'operator': operator}; }
    
comment =
	"//" " "? text:$([^\n]*) { return {'type': 'comment', 'text': text}; }
	
time =
	value:FLOAT _ unit:TIMEUNIT { return {'type': 'time', 'value': value, 'unit': unit}; }
    
numvalue =
    array_access
    / channel
    / number
    
variable =
	name:ID { return {'type': 'variable', 'name': name}; }
    
channel =
	name:ID { return {'type': 'channel', 'name': name}; }
    
regname =
	name:ID { return {'type': 'regname', 'name': name}; }
    
number =
	value:FLOAT { return {'type': 'number', 'value': value}; }
    
label =
	_ ":" _ name:ID { return {'type': 'label', 'name': name}; }
    
math =
	lhs:numvalue _ operator:("+=" / "-=") _ rhs:numvalue { return {'type': 'math', 'lhs': lhs, 'rhs': rhs, 'operator': operator} }

array_init =
	"[" _ x0:FLOAT? x:(_ "," _ FLOAT)* _ "]" { return {'type': 'array_init', 'values': x0 ? [x0, ...(x.map(elem => elem[3]))] : []} }
    
array_access =
	array:ID _ "[" _ index:(variable / number) _ "]" { return {'type': 'array_access', 'array': array, 'index': index} }

TIMEUNIT = $("sec" / "min" / "h")
COMPARE = $(([><]"="?) / "=")
INT = $("-"?[0-9]+)
FLOAT = $("-"?[0-9]+("."[0-9]+)?)
ID = $([A-Za-z][A-Za-z0-9_]*)
_ = $([ \t\r\n]*)