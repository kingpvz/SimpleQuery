import build.fn as FN

VARIABLESTORAGE = {}

while True:
    x = input(">  ")
    try: FN.execute(x, VARIABLESTORAGE)
    except SyntaxError as e: print("Syntax Error:", e)
    except ValueError as e: print("Value Error:", e)
    except: print("Provided command raised an unknown error.")