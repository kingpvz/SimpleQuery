from .commands import *
import re


REPLACINGS = [("\\n", "\n"), ("\\s", " "), ("\\t", "\t"), ("\\l", "{"), ("\\r", "}"), ("\\$sc.", ";")]
REPLACINGS.append(("\\b", "\\"))

def execute(cmd, vars):
    
    def replacevars(m):
        key = m.group(1)
        return str(vars.get(key, m.group(0)))
    
    def replaceescapes(m):
        for i in REPLACINGS:
            m = m.replace(i[0], i[1])
        m = m.replace("\\0","")
        return m

    x = cmd.strip()
    x = re.sub(r'\{(\w+)\}', replacevars, x)
    x = x.split()
    x[0] = x[0].lower()
    P, R = None, None
    
    match x[0]:
        case "var": P,R = declarevariable(x, vars)
        case "print": P,R = VAR.pr(x, vars, replaceescapes)
        case "del": P,R = VAR.delete(x, vars)
        case "variables": P,R = VAR.listall(x, vars)
        case "lit" | "str" | "string": P,R = VAR.literal(x, vars, replaceescapes)
        case "int": P,R = VAR.number(x, vars, False)
        case "float": P,R = VAR.number(x, vars, True)
        case "true" | "false": P,R = VAR.boolean(x, vars)
        case "concat": P,R = concatenate(x, vars)
        case "with": P,R = variableparameter(x, vars, replaceescapes)
        
        case "github": P,R = GITHUB.github(x, vars)
        case "web": P,R = WEB.web(x, vars)
        
        case _: raise SyntaxError("This command doesn't exist.")
    
    if P != None: print(P)
    if type(R) == type("str"):
        for i in REPLACINGS[::-1]:
            R = R.replace(i[1], i[0])
    return R

def declarevariable(x, vars):
    if len(x) < 4: raise SyntaxError("To declare a variable follow this syntax: 'var variable_name = COMMAND_WITH_RETURN'. Don't forget the spaces!")
    elif x[2] != "=":
        if x[2] == ":=":
            if not re.match(r'\w+', x[1]): raise ValueError("Variable name must only contain letters, numbers and underscores.")
            else: vars[x[1]] = " ".join(x[3:]); return None, None
        else: raise SyntaxError("To declare a variable follow this syntax: 'var variable_name = COMMAND_WITH_RETURN'. Don't forget the spaces!")
    elif not re.match(r'\w+', x[1]): raise ValueError("Variable name must only contain letters, numbers and underscores.")
    else: vars[x[1]] = execute(" ".join(x[3:]), vars); return None, None
    
def concatenate(x, vars, sep=""):
    if len(x) < 4 or len([i for i in x if i=="&"]) != 1: raise SyntaxError("concat command must follow this syntax: 'concat COMMAND1 & COMMAND2'.")
    else: r1, r2 = execute(" ".join(x[1:x.index("&")]), vars), execute(" ".join(x[x.index("&")+1:]), vars); return None, str(r1)+sep+str(r2)
                                                            
def variableparameter(x, vars, fn):
    if len(x) < 3: raise SyntaxError("with command must follow this syntax: 'with *parameter* COMMAND'")
    elif x[2] == "concat": return concatenate(x[2:], vars, sep=fn(x[1]))