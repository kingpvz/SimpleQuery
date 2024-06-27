def pr(x, vars, fn):
    if len(x) < 2: raise SyntaxError("Please provide a value to print.")
    else: print(fn(" ".join(x[1:]))); return None


def delete(x, vars):
    if len(x) == 2:
        if x[1] in vars: del vars[x[1]]; return None, None
        else: raise ValueError("This variable doesn't exist.")
    else: raise SyntaxError("To delete a variable follow this syntax: 'del variable_name'")
   

def listall(x, vars):
    if len(x) == 1:
        s = "\n"
        for k,v in vars.items():
            s+=k+" = "+str(v)+"\n"
        if len(vars.items()) == 0:
            s = "There are no saved variables."
        return s
    else: raise SyntaxError("Unexpected parameter provided.")
    

def literal(x, vars, fn):
    if not len(x) == 1: return fn(" ".join(x[1:]))
    else: return None
    

def number(x, vars, isdecimal):
    if len(x) != 2: raise SyntaxError("Please provide a number to return.")
    else:
        try:
            if isdecimal: m = float(x[1].replace(",","."))
            else: m = int(x[1].replace(",","."))
        except ValueError: raise ValueError("Provided parameter is not a number.")
        else: return m
        

def boolean(x, vars):
    if len(x) != 1: raise SyntaxError("Unexpected parameter provided.")
    else:
        if x[0] == "true": return True
        elif x[0] == "false": return False
        else: raise SyntaxError("How did you do this")