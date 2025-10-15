from textnode import TextType, TextNode
from extract_links import extract_markdown_images, extract_markdown_links

def text_to_textnodes(text):
    nodes = [TextNode(text)]
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.PLAIN:
            parts = node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise Exception("Invalid Markdown Syntax")
            for i, part in enumerate(parts):
                if part == "":
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(part))
                else:
                    new_nodes.append(TextNode(part, text_type))
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.PLAIN:
            images = extract_markdown_images(node.text)
            remaining_text = node.text
            for alt, link in images:
                text, remaining_text = remaining_text.split(f"![{alt}]({link})", 1)
                if text != "":
                    new_nodes.append(TextNode(text))
                new_nodes.append(TextNode(alt, TextType.IMAGE, link))
            if remaining_text != "":
                new_nodes.append(TextNode(remaining_text))
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.PLAIN:
            links = extract_markdown_links(node.text)
            remaining_text = node.text
            for alt, link in links:
                text, remaining_text = remaining_text.split(f"[{alt}]({link})", 1)
                if text != "":
                    new_nodes.append(TextNode(text))
                new_nodes.append(TextNode(alt, TextType.LINK, link))
            if remaining_text != "":
                new_nodes.append(TextNode(remaining_text))
        else:
            new_nodes.append(node)
    return new_nodes
