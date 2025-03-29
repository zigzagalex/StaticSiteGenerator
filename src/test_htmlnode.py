import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextType, TextNode
from main import text_node_to_html_node


class TestHtmlnode(unittest.TestCase):
    def test_eq(self):
        htmlnode = HTMLNode("p","test", children=[HTMLNode("p","test")])
        htmlnode2 = HTMLNode("p","test", children=[HTMLNode("p","test")])
        self.assertEqual(htmlnode.__repr__(), htmlnode2.__repr__())

    def test_neq(self):
        htmlnode = HTMLNode("a", "test", children=[HTMLNode("p", "test")])
        htmlnode2 = HTMLNode("p", "test", children=[HTMLNode("p", "test")])
        self.assertNotEqual(htmlnode.__repr__(), htmlnode2.__repr__())


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")


class TestParentNode(unittest.TestCase):
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

class TestTextToLeafNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

if __name__ == "__main__":
    unittest.main()