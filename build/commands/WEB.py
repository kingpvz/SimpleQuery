import webbrowser

def web(x, vars):
    if len(x) == 1:
        print("""
Welcome to the WEB module of SimpleQuery!
This is a simple module to open websites in your browser straight from SQ!

Commands:
web open URL : Open URL in the default web browser.
""")
    else:
        if x[1].lower() == "open":
            if len(x) == 3: webbrowser.open(x[2], new=2, autoraise=True); return None
            else: raise SyntaxError("Open command must have exactly one URL as a parameter.")
        else: print("Unknown WEB command.")