import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")
        node = HTMLNode(props={"href": "www.hhdhf.gov"})
        self.assertEqual(node.props_to_html(), ' href="www.hhdhf.gov"')
        node = HTMLNode(props={"href": "www.hhdhf.gov", "hhhh": "lastofus"})
        self.assertEqual(node.props_to_html(), ' href="www.hhdhf.gov" hhhh="lastofus"')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        node = LeafNode(None, "Value here")
        self.assertEqual(node.to_html(), "Value here")
        err = None
        try:
            node = LeafNode("p", None)
            node.to_html()
        except ValueError as e:
            err = e
        self.assertIsNotNone(err)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )        

    def test_to_html_with_multiple_children(self):
        node = ParentNode("div", [
                              LeafNode("b", "Lane"),
                              LeafNode("i", "please"),
                              LeafNode("u", "stop"),
                          ])
        self.assertEqual(
            node.to_html(), "<div><b>Lane</b><i>please</i><u>stop</u></div>"
        )

    def test_to_html_with_no_children(self):
        err = None
        try:
            node = ParentNode("u", None)
            node.to_html()
        except ValueError as e:
            err = e
        self.assertIsNotNone(err)

    def test_to_html_with_no_tag(self):
        err = None
        try:
            node = ParentNode(None, [])
            node.to_html()
        except ValueError as e:
            err = e
        self.assertIsNotNone(err)

if __name__ == "__main__":
    unittest.main()
