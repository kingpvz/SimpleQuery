import build.fn as FN

VARIABLESTORAGE = {}
with open("build/info.txt") as f:
    INFO = f.readlines()

print(f"SimpleQuery Console {INFO[0]}For documentation see {INFO[1]}\n")
while True:
    x = input(">  ")
    try: FN.execute(x, VARIABLESTORAGE, {})
    except SyntaxError as e: print("Syntax Error:", e)
    except ValueError as e: print("Value Error:", e)
    except Exception as e: print("Fatal Error:", e)
    except: print("Provided command raised an unknown error.")