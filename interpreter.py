import build.fn as FN
from pathlib import Path
import re
from random import randint as rnd
import sys

with open("build/info.txt") as f:
    INFO = f.readlines()

LN = 0

CONTEXT = True
CURRENT_FUNCTION = []
VARIABLESTORAGE = {}
FUNCTIONS = {}

def CONTEXT_BREAK():
    sys.exit("AN ERROR OCCURED")

def CONTEXT_EXECUTE(x):
    global LN, CONTEXT, CURRENT_FUNCTION
    if x.split()[0].lower() != "fn" and CONTEXT:
        LN += 1
        try: FN.execute(x, VARIABLESTORAGE, FUNCTIONS)
        except SyntaxError as e: print(f"Syntax Error at line {LN}: {e}"); CONTEXT_BREAK()
        except ValueError as e: print(f"Value Error at line {LN}: {e}"); CONTEXT_BREAK()
        except Exception as e: print(f"Unknown Error at line {LN}: {e}"); CONTEXT_BREAK()
        except: print(f"Line {LN} raised an unknown error."); CONTEXT_BREAK()
    else:
        CONTEXT = False
        if re.match(r"^\.{1,}$", x):
            CONTEXT = True
            FUNCTIONS[CURRENT_FUNCTION[0].split()[1]] = CURRENT_FUNCTION[1:]
            CURRENT_FUNCTION = []
        else:
            CURRENT_FUNCTION.append(x)


print(f"SimpleQuery Interpreter {INFO[0]}For more information see {INFO[2]}\n")
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
        print("Error, file doesn't exist, or is not a SimpleQuery script.\n")