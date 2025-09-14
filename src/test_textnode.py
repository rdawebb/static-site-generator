# import the necessary modules
import unittest
from textnode import TextNode, TextType, text_node_to_html_node

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

class TestTextNodeToHTMLNode(unittest.TestCase):
    # test text node to html node conversion for plain text
    def test_plain(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    # test text node to html node conversion for bold text
    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

    # test text node to html node conversion for italic text
    def test_italic(self):
        node = TextNode("This is italic", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic")

    # test text node to html node conversion for code text
    def test_code(self):
        node = TextNode("print('Hello, world!')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('Hello, world!')")

    # test text node to html node conversion for link
    def test_link(self):
        node = TextNode("This is a link", TextType.LINK, "http://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href": "http://example.com"})

    # test text node to html node conversion for image
    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "http://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "http://example.com/image.png", "alt": "This is an image"})

    # test text node to html node conversion for unknown type
    def test_unknown_type(self):
        node = TextNode("This is unknown", "UNKNOWN_TYPE")
        with self.assertRaises(Exception):
            text_node_to_html_node(node) # expect Exception

# run the tests
if __name__ == "__main__":
    unittest.main()