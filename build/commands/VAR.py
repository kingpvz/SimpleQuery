import re

def declare(x, vars):
    if len(x) < 4: raise SyntaxError("To declare a variable follow this syntax: 'var name = value'. Don't forget the spaces!")
    elif x[2] != "=": raise SyntaxError("To declare a variable follow this syntax: 'var name = value'. Don't forget the spaces!")
    elif not re.match(r'\w+', x[1]): raise ValueError("Variable name must only contain letters, numbers and underscores.")
    else: vars[x[1]] = " ".join(x[3:])



def pr(x, vars, fn):
    if len(x) < 2: raise SyntaxError("Please provide a value to print.")
    else: print(fn(" ".join(x[1:])))



def delete(x, vars):
    if len(x) == 2:
        if x[1] in vars: del vars[x[1]]
        else: raise ValueError("This variable doesn't exist.")
    else: raise SyntaxError("To delete a variable follow this syntax: 'del variable_name'")
   


def listall(x, vars):
    if len(x) == 1:
        for k,v in vars.items():
            print(k, "=", v)
        if len(vars.items()) == 0:
            print("There are no saved variables.")
    else: raise SyntaxError("Unexpected parameter provided.")