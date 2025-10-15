from blocks import markdown_to_blocks
from conversion import markdown_to_html_node
import os

def extract_title(markdown):
    for block in markdown_to_blocks(markdown):
        if block.startswith("# "):
            return block[2:].strip()
    raise Exception("There is no header!")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_content = None
    with open(from_path, 'r') as f:
        markdown_content = f.read()
    template_content = None
    with open(template_path, 'r') as f:
        template_content = f.read()
    page_content = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)
    html_page = template_content.replace("{{ Title }}", title).replace("{{ Content }}", page_content)
    os.makedirs(os.path.dirname(dest_path), mode = 0o750, exist_ok=True)
    with open(dest_path, 'w') as f:
        f.write(html_page)
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for name in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, name)
        dest_path = os.path.join(dest_dir_path, name)
        if os.path.isfile(source_path):
            if source_path.endswith(".md"):
                generate_page(source_path, template_path, dest_path[:-2] + 'html')
        else:
            os.mkdir(dest_path, mode=0o750)
            generate_pages_recursive(source_path, template_path, dest_path)
            
