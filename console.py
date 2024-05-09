import build.fn as FN

VARIABLESTORAGE = {}

print("SimpleQuery Console alpha1.0.5\n")
while True:
    x = input(">  ")
    try: FN.execute(x, VARIABLESTORAGE)
    except SyntaxError as e: print("Syntax Error:", e)
    except ValueError as e: print("Value Error:", e)
    except Exception as e: print("Fatal Error:", e)
    except: print("Provided command raised an unknown error.")