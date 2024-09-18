from os import replace
from threading import local
from xml.dom import SyntaxErr
from .commands import *
import re

LOCALNAME = ""
CURRENTFN = ""

REPLACINGS = [("\\n", "\n"), ("\\s", " "), ("\\t", "\t"), ("\\l", "{"), ("\\r", "}"), ("\\$sc.", ";"), ("\\$et.", "&")]
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
    R = None

    match x[0]:
        case "var": R = declarevariable(x, vars, fns)
        case "print": R = VAR.pr(x, vars, replaceescapes)
        case "printf": R = functionprint(x,vars,fns,replaceescapes)
        case "del": R = VAR.delete(x, vars)
        case "variables": R = VAR.listall(x, vars)
        case "lit" | "str" | "string": R = VAR.literal(x, vars, replaceescapes)
        case "int": R = VAR.number(x, vars, False)
        case "float": R = VAR.number(x, vars, True)
        case "true" | "false": R = VAR.boolean(x, vars)
        case "concat": R = concatenate(x, vars, fns, replaceescapes)
        case "with": R = variableparameter(x, vars, fns, replaceescapes)
        case "call": R = callfn(x, vars, fns, replaceescapes)
        case "scope": R = changescope(x, vars, fns)
        
        case "github": R = GITHUB.github(x, vars)
        case "web": R = WEB.web(x, vars)
        
        case _: raise SyntaxError("This command doesn't exist.")
    
    if type(R) == type("str"):
        for i in REPLACINGS[::-1]:
            R = R.replace(i[1], i[0])
    return R

def declarevariable(x, vars, fns):
    if len(x) < 4: raise SyntaxError("To declare a variable follow this syntax: 'var variable_name = COMMAND_WITH_RETURN'. Don't forget the spaces!")
    elif x[2] != "=":
        if x[2] == ":=":
            if not re.match(r'^\w+$', x[1]): raise ValueError("Variable name must only contain letters, numbers and underscores.")
            else: vars[LOCALNAME+x[1]] = " ".join(x[3:]); return None
        else: raise SyntaxError("To declare a variable follow this syntax: 'var variable_name = COMMAND_WITH_RETURN'. Don't forget the spaces!")
    elif not re.match(r'^\w+$', x[1]): raise ValueError("Variable name must only contain letters, numbers and underscores.")
    else: vars[LOCALNAME+x[1]] = execute(" ".join(x[3:]), vars, fns); return None
    
def concatenate(x, vars, fns, fn, sep=""):
    if len(x) < 4 or len([i for i in x if i=="&"]) != 1: raise SyntaxError("concat command must follow this syntax: 'concat COMMAND1 & COMMAND2'.")
    else: r1, r2 = execute(" ".join(x[1:x.index("&")]), vars, fns), execute(" ".join(x[x.index("&")+1:]), vars, fns); return fn(str(r1))+sep+fn(str(r2))
                                                            
def variableparameter(x, vars, fns, fn):
    if len(x) < 3: raise SyntaxError("with command must follow this syntax: 'with *parameter* COMMAND'")
    elif x[2] == "concat": return concatenate(x[2:], vars, fns, fn, sep=fn(x[1]))

def callfn(x, vars, fns, fn):
    global LOCALNAME, CURRENTFN
    if len(x) < 2: raise SyntaxError("No function to call was provided.")
    elif x[1] not in fns: raise SyntaxError("This function doesn't exist.")
    else:
        LOCALNAME = "LOCAL__"+x[1]+"__"
        CURRENTFN = x[1]
        RET = None
        for i in fns[x[1]]:
            if i.split()[0].lower() != "return":
                execute(i.replace("{", "{"+LOCALNAME), vars, fns)
            else:
                RET = execute(i[7:].replace("{", "{"+LOCALNAME), vars, fns)
        if type(RET) == type("str"): RET = fn(RET)
        LOCALNAME = ""
        CURRENTFN = ""
        return RET
    
def changescope(x, vars, fns):
    global LOCALNAME, CURRENTFN
    if len(x)>3: raise SyntaxError("scope command takes up to 2 parameters.")
    elif len(x) == 1:
        if LOCALNAME == "": return "GLOBAL__"
        else: return LOCALNAME
    elif len(x) == 2:
        if x[1].lower() == "global": LOCALNAME = ""
        elif x[1].lower() == "local": LOCALNAME = "LOCAL__"+CURRENTFN+"__"
        elif x[1].lower() == "fn": raise SyntaxError("Function scope needs to follow this syntax: 'scope fn *function_name*'")
        elif x[1].lower() == "custom": raise SyntaxError("Custom scope needs to follow this syntax: 'scope custom *key*'")
        else: raise SyntaxError("Provided scope doesn't exist.")
    else:
        if x[1].lower() == "fn":
            if x[2] in fns: LOCALNAME = "LOCAL__"+x[2]+"__"
            else: raise ValueError("Provided function name doesn't exist, or, its scope is unaccessible.")
        elif x[1].lower() == "custom":
            LOCALNAME = "LOCAL__CUSTOM__"+x[2]+"__"
        else: raise SyntaxError("Custom scope tag "+x[1]+" doesn't exist.")
        
def functionprint(x, vars,fns,fn):
    if len(x)==1: raise SyntaxError("Please provide a value to print.")
    else:
        res = execute(" ".join(x[1:]),vars,fns)
        a = fn(res) if type(res)==type("lol") else fn(str(res))
        print(a)