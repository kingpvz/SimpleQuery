from os import replace
from threading import local
from xml.dom import SyntaxErr
from .commands import *
import re

LOCALNAME = ""

REPLACINGS = [("\\n", "\n"), ("\\s", " "), ("\\t", "\t"), ("\\l", "{"), ("\\r", "}"), ("\\$sc.", ";"), ("\\et.", "&")]
REPLACINGS.append(("\\b", "\\"))

def execute(cmd, vars, fns):
    
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
        case "var": P,R = declarevariable(x, vars, fns)
        case "print": P,R = VAR.pr(x, vars, replaceescapes)
        case "del": P,R = VAR.delete(x, vars)
        case "variables": P,R = VAR.listall(x, vars)
        case "lit" | "str" | "string": P,R = VAR.literal(x, vars, replaceescapes)
        case "int": P,R = VAR.number(x, vars, False)
        case "float": P,R = VAR.number(x, vars, True)
        case "true" | "false": P,R = VAR.boolean(x, vars)
        case "concat": P,R = concatenate(x, vars, fns)
        case "with": P,R = variableparameter(x, vars, fns, replaceescapes)
        case "call": P,R = callfn(x, vars, fns, replaceescapes)
        
        case "github": P,R = GITHUB.github(x, vars)
        case "web": P,R = WEB.web(x, vars)
        
        case _: raise SyntaxError("This command doesn't exist.")
    
    if P != None: print(P)
    if type(R) == type("str"):
        for i in REPLACINGS[::-1]:
            R = R.replace(i[1], i[0])
    return R

def declarevariable(x, vars, fns):
    if len(x) < 4: raise SyntaxError("To declare a variable follow this syntax: 'var variable_name = COMMAND_WITH_RETURN'. Don't forget the spaces!")
    elif x[2] != "=":
        if x[2] == ":=":
            if not re.match(r'\w+', x[1]): raise ValueError("Variable name must only contain letters, numbers and underscores.")
            else: vars[LOCALNAME+x[1]] = " ".join(x[3:]); return None, None
        else: raise SyntaxError("To declare a variable follow this syntax: 'var variable_name = COMMAND_WITH_RETURN'. Don't forget the spaces!")
    elif not re.match(r'\w+', x[1]): raise ValueError("Variable name must only contain letters, numbers and underscores.")
    else: vars[LOCALNAME+x[1]] = execute(" ".join(x[3:]), vars, fns); return None, None
    
def concatenate(x, vars, fns, sep=""):
    if len(x) < 4 or len([i for i in x if i=="&"]) != 1: raise SyntaxError("concat command must follow this syntax: 'concat COMMAND1 & COMMAND2'.")
    else: r1, r2 = execute(" ".join(x[1:x.index("&")]), vars, fns), execute(" ".join(x[x.index("&")+1:]), vars, fns); return None, str(r1)+sep+str(r2)
                                                            
def variableparameter(x, vars, fns, fn):
    if len(x) < 3: raise SyntaxError("with command must follow this syntax: 'with *parameter* COMMAND'")
    elif x[2] == "concat": return concatenate(x[2:], vars, fns, sep=fn(x[1]))

def callfn(x, vars, fns, fn):
    global LOCALNAME
    if len(x) < 2: raise SyntaxError("No function to call was provided.")
    elif x[1] not in fns: raise SyntaxError("This function doesn't exist.")
    else:
        LOCALNAME = "LOCAL__"+x[1]+"__"
        RET = None
        for i in fns[x[1]]:
            if i.split()[0].lower() != "return":
                execute(i.replace("{", "{"+LOCALNAME), vars, fns)
            else:
                RET = execute(i[7:], vars, fns)
        if type(RET) == type("str"): RET = fn(RET)
        LOCALNAME = ""
        return None, RET