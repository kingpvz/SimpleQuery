import re

def declare(x, vars):
    if len(x) < 4: raise SyntaxError("To declare a variable follow this syntax: 'var name = value'. Don't forget the spaces!")
    elif x[2] != "=": raise SyntaxError("To declare a variable follow this syntax: 'var name = value'. Don't forget the spaces!")
    elif not re.match(r'\w+', x[1]): raise ValueError("Variable name must only contain letters, numbers and underscores.")
    else: vars[x[1]] = " ".join(x[3:]); return None, None



def pr(x, vars, fn):
    if len(x) < 2: raise SyntaxError("Please provide a value to print.")
    else: return(fn(" ".join(x[1:]))), None



def delete(x, vars):
    if len(x) == 2:
        if x[1] in vars: del vars[x[1]]; return None, None
        else: raise ValueError("This variable doesn't exist.")
    else: raise SyntaxError("To delete a variable follow this syntax: 'del variable_name'")
   


def listall(x, vars):
    if len(x) == 1:
        s = "\n"
        for k,v in vars.items():
            s+=k+" = "+v+"\n"
        if len(vars.items()) == 0:
            s = "There are no saved variables."
        return s, s
    else: raise SyntaxError("Unexpected parameter provided.")