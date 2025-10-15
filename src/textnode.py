from enum import Enum

class TextType(Enum):
    PLAIN = "text"
    BOLD = "**bold text**"
    ITALIC = "_italic text_"
    CODE = "`code text`"
    LINK = "[anchor text](url)"
    IMAGE = "![alt text](url)"

class TextNode:
    def __init__(self, text, text_type=TextType.PLAIN, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
