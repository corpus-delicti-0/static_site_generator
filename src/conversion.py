from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode
from blocks import markdown_to_blocks, block_to_block_type, BlockType
from delimiter import text_to_textnodes

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.PLAIN:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise Exception("Unknown type") 

def parse_inline(text):
    nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in nodes]

def markdown_to_html_node(markdown):
    blocks_array = markdown_to_blocks(markdown)
    children = []
    for block in blocks_array:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            children.append(ParentNode("p", parse_inline(" ".join(block.split('\n')))))
        elif block_type == BlockType.HEADING:
            depth = len(block.split(" ", 1)[0])
            children.append(ParentNode(f"h{depth}", parse_inline(block[depth+1:])))
        elif block_type == BlockType.CODE:
            children.append(ParentNode("pre", [LeafNode("code", block[3:-3])]))
        elif block_type == BlockType.QUOTE:
            children.append(ParentNode(
                "blockquote",
                parse_inline("\n".join([line[1:].strip() for line in block.split("\n")]))))
        elif block_type == BlockType.UNORDERED_LIST:
            children.append(ParentNode(
                "ul",
                [ParentNode("li", parse_inline(line.strip()[2:].strip())) for line in block.split("\n")]))
        elif block_type == BlockType.ORDERED_LIST:
            children.append(ParentNode(
                "ol",
                [ParentNode("li", parse_inline(line.strip()[2:].strip())) for line in block.split("\n")]))
    return ParentNode("div", children)

    
