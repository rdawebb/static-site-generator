# import the necessary modules
import unittest
from split_nodes import split_nodes_delimiter
from textnode import TextNode, TextType

# define the test case class
class TestSplitNodes(unittest.TestCase):
    # test splitting by bold delimiter
    def test_split_bold(self):
        old_nodes = [TextNode("This is **bold** text", TextType.PLAIN)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.PLAIN)
        ]
        self.assertEqual(new_nodes, expected_nodes)

    # test splitting by italic delimiter
    def test_split_italic(self):
        old_nodes = [TextNode("This is _italic_ text", TextType.PLAIN)]
        new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
        expected_nodes = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.PLAIN)
        ]
        self.assertEqual(new_nodes, expected_nodes)

    # test splitting by code delimiter
    def test_split_code(self):
        old_nodes = [TextNode("This is `code` text", TextType.PLAIN)]
        new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.PLAIN)
        ]
        self.assertEqual(new_nodes, expected_nodes)

    # test splitting when delimiter not found
    def test_delimiter_not_found(self):
        old_nodes = [TextNode("This is plain text", TextType.PLAIN)]
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        # check that the exception message is correct
        self.assertTrue("Delimiter '**' not found in text: This is plain text" in str(context.exception))

    # test nodes with non-plain text type
    def test_non_plain_text_type(self):
        old_nodes = [TextNode("This is bold text", TextType.BOLD)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes, old_nodes)
        