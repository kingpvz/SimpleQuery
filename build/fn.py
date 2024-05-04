from .commands import *
import re


def execute(cmd, vars):
    
    def replacevars(m):
        key = m.group(1)
        return vars.get(key, m.group(0))
    
    def replaceescapes(m):
        m = m.replace("\\n", "\n").replace("\\s", " ").replace("\\t","    ").replace("\\0", "")
        return m

    x = cmd.strip()
    x = re.sub(r'\{(\w+)\}', replacevars, x)
    x = x.split()
    x[0] = x[0].lower()
    
    match x[0]:
        case "github": GITHUB.github(x, vars)
        case "var": VAR.declare(x, vars)
        case "print": VAR.pr(x, vars, replaceescapes)
        case "del": VAR.delete(x, vars)
        case "variables": VAR.listall(x, vars)
        case "web": WEB.web(x, vars)
        case _: raise SyntaxError("This command doesn't exist.")