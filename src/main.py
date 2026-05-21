import os
import shutil

from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive
from textnode import TextType, TextNode

print("hello world")

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"

def main():
    Piece1 = "This is a test."
    Piece2 = TextType.TEXT
    Piece3 = "https://fraudulentsite.com"
    Test_Obj = TextNode(Piece1,Piece2,Piece3)
    print(Test_Obj)

    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    print("Generating content...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_public)


main()
