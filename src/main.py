from textnode import *
import os
from shutil import rmtree, copy
from parser import *
from pathlib import Path
import sys

def main(basepath):
    static_copy(basepath)
#    textNode = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
#    print(textNode)


def static_copy(basepath):
    if (os.path.exists('./docs')): 
        rmtree('./docs')
    os.mkdir('./docs')
    copy_folder('./static', './docs')
    generate_pages_recursive(basepath, './content/', './template.html', './docs')

def extract_title(markdown):
    pattern = r"^#\s+(.+)$"

    match = re.match(pattern, markdown, re.MULTILINE)
    if match:
        return match.group(1)  
        
    raise Exception("no title")

def generate_pages_recursive(basepath, dir_path_content, template_path, dest_dir_path):
    for content in os.listdir(dir_path_content):

        if "." in content:
            name, ext = content.rsplit(".", 1)
        else:
            name, ext = content, ""

        content_from = dir_path_content + '/' + content
        content_to = dest_dir_path + '/' + content

        if not os.path.isfile(content_from):
            os.mkdir(content_to)
            generate_pages_recursive(basepath, content_from, template_path, content_to)
        elif(ext == 'md'):            
            content_to = dest_dir_path + '/' + name + ".html"
            generate_page(basepath, content_from, template_path, content_to)

 


def generate_page(basepath, from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    content = None
    template = None
    with open(from_path) as f:
        content = f.read()
    with open(template_path) as f:
        template = f.read()
    
    node = markdown_to_html_node(content)
    html = template.replace("{{ Title }}", extract_title(content)).replace("{{ Content }}", node.to_html())
 
    os.makedirs(Path(dest_path).parent, exist_ok=True)   

    html.replace('href="/',f'href="{basepath}')
    html.replace('src="/',f'src="{basepath}')

    with open(dest_path, 'w') as f:
        f.write(html)
    

def copy_folder(from_dir, to_dir):
    if (not os.path.exists(from_dir)):
        return
    for content in os.listdir(from_dir):
        content_from = from_dir + '/' + content
        content_to = to_dir + '/' + content
        if os.path.isfile(content_from):
            print("Copying ", content_from, content_to)
            copy(content_from, content_to)
        else:
            os.mkdir(content_to)
            copy_folder(content_from, content_to)
    return

basepath = sys.argv[0] if len(sys.argv) != 0 else "/"
main(basepath)