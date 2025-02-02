from functions import *

def main():
    copy_dir("./static", "./public")
    generate_pages_recursive("./content/", "./template.html", "./public/")
    
main()