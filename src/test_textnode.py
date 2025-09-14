# import the necessary modules
import unittest
from textnode import TextNode, TextType

# define the test case class
class TestTextNode(unittest.TestCase):
    # test representation
    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(repr(node), "TextNode(This is a text node, TextType.BOLD, None)")
    
    # test equal case
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    # test with different text
    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    # test different type
    def test_different_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    # test with different text and type
    def test_different_text_and_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    # test when url is None
    def test_url_none(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node, node2)

    # test with URL
    def test_with_url(self):
        node = TextNode("This is a link", TextType.LINK, "http://example.com")
        self.assertEqual(repr(node), "TextNode(This is a link, TextType.LINK, http://example.com)")

    # test with different URL
    def test_with_different_url(self):
        node = TextNode("This is a link", TextType.LINK, "http://example.com")
        node2 = TextNode("This is a link", TextType.LINK, "http://different.com")
        self.assertNotEqual(node, node2)

    # test with image
    def test_with_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "http://example.com/image.png")
        self.assertEqual(repr(node), "TextNode(This is an image, TextType.IMAGE, http://example.com/image.png)")

# run the tests
if __name__ == "__main__":
    unittest.main()