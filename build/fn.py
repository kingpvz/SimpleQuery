from .commands import *
import re


REPLACINGS = [("\\n", "\n"), ("\\s", " "), ("\\t", "\t"), ("\\$lc;", "{"), ("\\$rc;", "}"), ("\\bs;", "\\")]

def execute(cmd, vars):
    
    def replacevars(m):
        key = m.group(1)
        return vars.get(key, m.group(0))
    
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
        case "github": P,R = GITHUB.github(x, vars)
        case "var": P,R = VAR.declare(x, vars)
        case "print": P,R = VAR.pr(x, vars, replaceescapes)
        case "del": P,R = VAR.delete(x, vars)
        case "variables": P,R = VAR.listall(x, vars)
        case "web": P,R = WEB.web(x, vars)
        case "save": savetovariable(x, vars)
        case _: raise SyntaxError("This command doesn't exist.")
    
    if P != None: print(P)
    if type(R) == type("str"):
        for i in REPLACINGS[::-1]:
            R = R.replace(i[1], i[0])
    return R

def savetovariable(x, vars):
    if len(x) < 4: raise SyntaxError("The save commands needs to follow this syntax: 'save COMMAND to/as/in variable_name'")
    else:
        if x[-2] not in {"to", "as", "in"}: raise SyntaxError("The save commands needs to follow this syntax: 'save COMMAND to/as/in variable_name'")
        else:
            vars[x[-1]] = execute(" ".join(x[1:-2]), vars)