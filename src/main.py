import os
import shutil
from textnode import TextNode, TextType
from generate_page import generate_pages_recursive

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))

def main():
    copy_static("static", "public")
    paths = ["content", "template.html", "public"]
    generate_pages_recursive(*[os.path.join(ROOT_PATH, p) for p in paths])

# copies content from a static directory to public directory
def copy_static(source, target):
    source_path = os.path.join(ROOT_PATH, source)
    target_path = os.path.join(ROOT_PATH, target)
    if os.path.exists(target_path):
        print(f"Removing {target}")
        shutil.rmtree(target_path)
    recursive_copy(source_path, target_path)

def recursive_copy(source, target, depth=0):
    indent = "  " * depth
    print(f"{indent}Creating {target}")
    os.mkdir(target, mode=0o750)
    for name in os.listdir(source):
        source_path = os.path.join(source, name)
        if os.path.isfile(source_path):
            print(f"{indent}File {source_path} -> {target}")
            shutil.copy(source_path, target)
        else:
            target_path = os.path.join(target, name)
            print(f"{indent}Directory {source_path} -> {target_path}")
            recursive_copy(source_path, target_path, depth + 1)

if __name__ == '__main__':
    main()
