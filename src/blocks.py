from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    if re.match(r"#{1,6} ", block) is not None:
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    lines = block.split('\n')
    if sum([line.startswith('>') for line in lines]) == len(lines):
        return BlockType.QUOTE
    if sum([line.startswith('- ') for line in lines]) == len(lines):
        return BlockType.UNORDERED_LIST
    if sum([re.match(r"\d+\. ", line) is not None for line in lines]) == len(lines):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    markdown = markdown.strip()
    blocks = []
    element = ""
    is_codeblock = False
    for line in markdown.split("\n"):
        if element == "" and line.startswith("```"):
            is_codeblock = True
            element += "```"
            continue
        if element != "" and line.endswith("```"):
            if is_codeblock:
                is_codeblock = False
                element += line[:-3] + "```" if len(line.strip()) > 3 else "```"
                blocks.append(element)
                element = ""
                continue
            if line.strip() != "```":
                raise Exception("Invalid beginning of a code block")
            blocks.append(element)
            element = "```"
            is_codeblock = True
        if is_codeblock:
            element += line + "\n"
            continue
        line = line.strip()
        if line == "":
            if element != "":
                blocks.append(element)
                element = ""
            continue
        if element != "":
            element += "\n"
        element += line
    if is_codeblock:
        raise Exception("Unterminated code block")
    if element != "":
        blocks.append(element)
    return blocks 
