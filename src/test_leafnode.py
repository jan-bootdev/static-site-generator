import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_leaf_to_html_2(self):
        node = LeafNode("p", "Hello, world!", {"class":"highlight"})
        self.assertEqual(node.to_html(), "<p class=\"highlight\">Hello, world!</p>")        