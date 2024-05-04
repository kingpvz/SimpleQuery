import webbrowser

def github(x, vars):
    if len(x) == 1:
        print("""
Welcome to the GitHub module of SimpleQuery!
This is an all-in-one module to help you launch GitHub from SQ!

Commands:
github rep USER REPOSITORY : Open USER's REPOSITORY
github page USER : Open USER's GitHub Pages page
""")
    else:
        match x[1].lower():
            case "rep":
                if len(x) == 4:
                    webbrowser.open("https://github.com/"+x[2]+"/"+x[3], new = 2)
                else:
                    raise SyntaxError("GitHub rep requires exactly two parameters (user, repository).")
            case "page":
                if len(x) == 3:
                    webbrowser.open(x[2]+".github.io",new=2)
                else:
                    raise SyntaxError("Github page requires exactly one parameter (user)")
            case _: print("Unknown GitHub command.")