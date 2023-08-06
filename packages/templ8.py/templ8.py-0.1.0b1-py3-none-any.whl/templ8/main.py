import sys
import templ8.blessing
from templ8.divine import divine
from templ8.radio import radio
from templ8.genesis import genesis
from templ8.blessing import makedir

DEITY_PATH = "d8y"
DEF_BASEHTML_PATH = "basehtml"
DEF_REPLACE_PATH = "repl8ce"

DEF_INPUT = "input"
DEF_OUTPUT = "output"


def help():
    print(templ8.blessing.TEMPL8_ASCII + "\n\n")
    print("  help             Display this list.")
    print("  genesis [name]   Create a new templ8 project in a folder named [name].")
    print("  divine           Assemble a templ8 site.")
    print("  radio            Assemble a templ8 blog.")
    print("")


def main():
    if len(sys.argv) <= 1:
        help()
    elif sys.argv[1] == "help":
        help()
    elif sys.argv[1] == "divine":
        divine()
    elif sys.argv[1] == "radio":
        radio()
    elif sys.argv[1] == "genesis":
        if len(sys.argv) >= 3:
            genesis(sys.argv[2])
        else:
            raise Exception("Unexpected number of arguments")
    else:
        raise Exception("Unknown command")
    
