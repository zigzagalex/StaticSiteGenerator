import unittest

from htmlnode import HTMLNode


class TestHtmlnode(unittest.TestCase):
    def test_eq(self):
        htmlnode = HTMLNode("p","test", children=[HTMLNode("p","test")])
        htmlnode2 = HTMLNode("p","test", children=[HTMLNode("p","test")])
        self.assertEqual(htmlnode.__repr__(), htmlnode2.__repr__())

    def test_neq(self):
        htmlnode = HTMLNode("a", "test", children=[HTMLNode("p", "test")])
        htmlnode2 = HTMLNode("p", "test", children=[HTMLNode("p", "test")])
        self.assertNotEqual(htmlnode.__repr__(), htmlnode2.__repr__())


if __name__ == "__main__":
    unittest.main()