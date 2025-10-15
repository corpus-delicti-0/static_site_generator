import unittest

from textnode import TextNode, TextType
from delimiter import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes

class TestDelimiter(unittest.TestCase):
    def test_empty(self):
        node = TextNode("", TextType.PLAIN)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [])
    def test_invalid(self):
        node = TextNode("this is a **test** for **invalid syntax", TextType.PLAIN)
        error = None
        try:
            split_nodes_delimiter([node], "**", TextType.BOLD)
        except Exception as e:
            error = e
        self.assertIsNotNone(error)
    def test_different_type(self):
        nodes = [
            TextNode("this is some **valid** shit", TextType.PLAIN),
            TextNode("this is something **that shouldn't be split", TextType.BOLD),
        ]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("this is some ", TextType.PLAIN),
            TextNode("valid", TextType.BOLD),
            TextNode(" shit", TextType.PLAIN),
            TextNode("this is something **that shouldn't be split", TextType.BOLD),
        ]
        self.assertEqual(result, expected)

class TestNodesImage(unittest.TestCase):
    def test_nothing_to_split(self):
        nodes = [
            TextNode("This shit has _no images_, just plain old boring markdown"),
        ]
        expected = [
            TextNode("This shit has _no images_, just plain old boring markdown"),
        ]
        self.assertEqual(split_nodes_image(nodes), expected)
    def test_single_node(self):
        nodes = [
            TextNode("This shit has two images: ![he's never gonna give you up](https://example.com/rick_astley.jpg) and ![also never gonna let you down](https://example.com/rick_astley.png). COOL"),
        ]
        expected = [
            TextNode("This shit has two images: "),
            TextNode("he's never gonna give you up", TextType.IMAGE, "https://example.com/rick_astley.jpg"),
            TextNode(" and "),
            TextNode("also never gonna let you down", TextType.IMAGE, "https://example.com/rick_astley.png"),
            TextNode(". COOL"),
        ]
        self.assertEqual(split_nodes_image(nodes), expected)
    def test_multiple_nodes(self):
        nodes = [
            TextNode("This one has an image: ![Pikachu looking surprised](https://example.com/surprised_pikachu.png)"),
            TextNode("This one has another two: ![Copyrighted material](https://nintendo.com/something_illegal.png)![Copyrighted material](https://nintendo.com/something_illegal.png)"),
            TextNode("This one has a link: [probably the best tits you've ever seen dude](https://doiki.ru)"),
            TextNode("This one is boring."),
        ]
        expected = [
            TextNode("This one has an image: "),
            TextNode("Pikachu looking surprised", TextType.IMAGE, "https://example.com/surprised_pikachu.png"),
            TextNode("This one has another two: "),
            TextNode("Copyrighted material", TextType.IMAGE, "https://nintendo.com/something_illegal.png"),
            TextNode("Copyrighted material", TextType.IMAGE, "https://nintendo.com/something_illegal.png"),
            TextNode("This one has a link: [probably the best tits you've ever seen dude](https://doiki.ru)"),
            TextNode("This one is boring."),
        ]
        self.assertEqual(split_nodes_image(nodes), expected)

class TestNodesLink(unittest.TestCase):
    def test_nothing_to_split(self):
        nodes = [
            TextNode("This shit has _no images_, just plain old boring markdown"),
        ]
        expected = [
            TextNode("This shit has _no images_, just plain old boring markdown"),
        ]
        self.assertEqual(split_nodes_link(nodes), expected)
    def test_single_node(self):
        nodes = [
            TextNode("This shit has two links: [he's never gonna give you up](https://example.com/rick_astley.jpg) and [also never gonna let you down](https://example.com/rick_astley.png). COOL"),
        ]
        expected = [
            TextNode("This shit has two links: "),
            TextNode("he's never gonna give you up", TextType.LINK, "https://example.com/rick_astley.jpg"),
            TextNode(" and "),
            TextNode("also never gonna let you down", TextType.LINK, "https://example.com/rick_astley.png"),
            TextNode(". COOL"),
        ]
        self.assertEqual(split_nodes_link(nodes), expected)
    def test_multiple_nodes(self):
        nodes = [
            TextNode("This one has an image: ![Pikachu looking surprised](https://example.com/surprised_pikachu.png)"),
            TextNode("This one has another two: ![Copyrighted material](https://nintendo.com/something_illegal.png)![Copyrighted material](https://nintendo.com/something_illegal.png)"),
            TextNode("This one has a link: [hot milfs in your area would like to know your social security number](https://doiki.ru)"),
            TextNode("This one has a better link: [used garage doors for sale](https://doiki.ru)"),
            TextNode("This one is boring."),
        ]
        expected = [
            TextNode("This one has an image: ![Pikachu looking surprised](https://example.com/surprised_pikachu.png)"),
            TextNode("This one has another two: ![Copyrighted material](https://nintendo.com/something_illegal.png)![Copyrighted material](https://nintendo.com/something_illegal.png)"),
            TextNode("This one has a link: "),
            TextNode("hot milfs in your area would like to know your social security number", TextType.LINK, "https://doiki.ru"),
            TextNode("This one has a better link: "),
            TextNode("used garage doors for sale", TextType.LINK, "https://doiki.ru"),
            TextNode("This one is boring."),
        ]
        self.assertEqual(split_nodes_link(nodes), expected)

class TestTextToNodes(unittest.TestCase):
    def test_everything(self):
        text = "This is **text** with an _italic_ word and a `code block ** _` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.PLAIN),
            TextNode("code block ** _", TextType.CODE),
            TextNode(" and an ", TextType.PLAIN),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(text_to_textnodes(text), expected)
