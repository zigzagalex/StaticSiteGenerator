import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode('This is some anchor text', TextType.LINK,'https://www.boot.dev')
        node2 = TextNode('This is some anchor text', TextType.LINK,'https://www.boot.dev')
        self.assertEqual(node.__repr__(), node2.__repr__())


if __name__ == "__main__":
    unittest.main()