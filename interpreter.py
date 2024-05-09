import build.fn as FN
from pathlib import Path
import re
from random import randint as rnd
import sys

STATEMENTS = {"if"}
CONTEXTS = ["dummy"]
CONTEXT = 0
CONTEXT_CODEBLOCK = []

LN = 0

VARIABLESTORAGE = {}

def CONTEXT_BREAK():
    sys.exit("AN ERROR OCCURED")

def CONTEXT_EXECUTE(x):
    global CONTEXT, CONTEXT_CODEBLOCK, CONTEXTS, LN
    if x.split()[0].lower() not in STATEMENTS and CONTEXT == 0:
        LN += 1
        try: FN.execute(x, VARIABLESTORAGE)
        except SyntaxError as e: print(f"Syntax Error at line {LN}: {e}"); CONTEXT_BREAK()
        except ValueError as e: print(f"Value Error at line {LN}: {e}"); CONTEXT_BREAK()
        except Exception as e: print(f"Unknown Error at line {LN}: {e}"); CONTEXT_BREAK()
        except: print(f"Line {LN} raised an unknown error."); CONTEXT_BREAK()
    else:
        if re.match(r"^\.{1,}$", x): CONTEXT-=x.count(".")
        if CONTEXT < 0: print("Closed a code block that doesn't exist."); CONTEXT_BREAK()
        if CONTEXT >= 0:
            if x.split()[0].lower() in STATEMENTS: CONTEXT+= 1; CONTEXTS.insert(0, x)
            CONTEXT_CODEBLOCK.append(x)
            if CONTEXT == 0:
                for x in CONTEXT_CODEBLOCK:
                    if x.split()[0].lower() in STATEMENTS:
                        CONTEXTS.pop(0)
                    if CONTEXTS[0].split()[0].lower() == "if":
                        if FN.execute(CONTEXTS[0][2:], vars) and x.split()[0].lower() not in STATEMENTS:
                            CONTEXT_EXECUTE(x)
                        else:
                            pass
                CONTEXT_CODEBLOCK = []; CONTEXTS = ["dummy"]


print("SimpleQuery Interpreter alpha1.0.0\n")
while True:
    FL = input("Please input the path to a .sq file to execute: ")
    if not FL.endswith(".sq"): FL += ".sq"
    my_file = Path(FL)
    if my_file.is_file():
        
        with open(FL, "r") as FILE:
            print("\n\n\n")

            FL_x = "\n".join(FILE.readlines())
            CODEST = rnd(1000, 1000000)
            FL_x = FL_x.replace("\\\n\n", f">>REVOKE:SPLIT<<:>>RESTWITHCODE:{CODEST}<<")
            FL_x = re.split(r"[;\n]+", FL_x)
            FL_x = [i.strip().replace(f">>REVOKE:SPLIT<<:>>RESTWITHCODE:{CODEST}<<"," ") for i in FL_x if i != ""]

            for FL_i in FL_x:
                CONTEXT_EXECUTE(FL_i)

            print("\n\n\n")
            input("Press enter to close the interpreter.")
        break
    else:
        print("Error, file doesn't exist, or is not a SimpleQuery script.")