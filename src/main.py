import sys
from functions import *

def main():
    base_path = "/"
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    copy_dir("./static", "./docs")
    generate_pages_recursive("./content/", "./template.html", "./docs/", base_path)
    
main()