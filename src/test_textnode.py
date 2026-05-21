import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)
    def test_eq_w_url(self):
        node1 = TextNode("This is a text node", TextType.BOLD,"http://911prankcall.com")
        node2 = TextNode("This is a text node", TextType.BOLD,"http://911prankcall.com")
        self.assertEqual(node1, node2)
    def test_text_diff(self):
        node1 = TextNode("This is right.",TextType.BOLD)
        node2 = TextNode("This is wrong.",TextType.BOLD)
        self.assertNotEqual(node1, node2)
    def test_type_diff(self):
        node1 = TextNode("This is right.",TextType.ITALIC)
        node2 = TextNode("This is right.",TextType.BOLD)
        self.assertNotEqual(node1, node2)

if __name__ == "__main__":
    unittest.main()