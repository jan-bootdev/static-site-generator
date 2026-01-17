import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("a", "Klick here!", None, {"href":"test.com"})
        self.assertEqual(node.props_to_html(), " href=\"test.com\"")
    def test_eq_2(self):
        node = HTMLNode("img", None, None, {"src":"image.jpg", "size":"300px"})
        self.assertEqual(node.props_to_html(), " src=\"image.jpg\" size=\"300px\"")
    def test_eq_3(self):
        node_child = HTMLNode("div", None, None, {"class":"help-content-container-child"})
        node = HTMLNode("div", None, node_child, {"class":"help-content-container"})
        self.assertEqual(node.props_to_html(), " class=\"help-content-container\"")


if __name__ == "__main__":
    unittest.main()