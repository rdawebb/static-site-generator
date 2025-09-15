# import the necessary modules
import unittest
from split_nodes import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
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

    # test splitting with bold and italic delimiters
    def test_split_bold_and_italic(self):
        old_nodes = [TextNode("**bold** and _italic_", TextType.PLAIN)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    # test splitting with two bold sections
    def test_split_two_bold_sections(self):
        old_nodes = [TextNode("This is **bold** and **more bold** text", TextType.PLAIN)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.PLAIN),
            TextNode("more bold", TextType.BOLD),
            TextNode(" text", TextType.PLAIN)
        ]
        self.assertEqual(new_nodes, expected_nodes)

    # test splitting with unmatched delimiters
    def test_unmatched_delimiters(self):
        old_nodes = [TextNode("This is **bold text", TextType.PLAIN)]
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        # check that the exception message is correct
        self.assertTrue("Invalid markdown - unmatched delimiter '**' in text: This is **bold text" in str(context.exception))

    # test splitting with empty text
    def test_empty_text(self):
        old_nodes = [TextNode("", TextType.PLAIN)]
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        # check that the exception message is correct
        self.assertTrue("Node text is empty" in str(context.exception))

    # test splitting with empty delimiter
    def test_empty_delimiter(self):
        old_nodes = [TextNode("This is bold text", TextType.PLAIN)]
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter(old_nodes, "", TextType.BOLD)
        # check that the exception message is correct
        self.assertTrue("Delimiter cannot be empty" in str(context.exception))

    # test splitting with no delimiters present
    def test_no_delimiters(self):
        old_nodes = [TextNode("This is plain text", TextType.PLAIN)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes, old_nodes)

    # test nodes with non-plain text type
    def test_non_plain_text_type(self):
        old_nodes = [TextNode("This is bold text", TextType.BOLD)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes, old_nodes)

    # test extracting markdown image links
    def test_extract_markdown_images(self):
        text = "Here is an image ![alt text](http://example.com/image.png) in the text."
        images = extract_markdown_images(text)
        expected_images = [("alt text", "http://example.com/image.png")]
        self.assertEqual(images, expected_images)

    # test extracting markdown links
    def test_extract_markdown_links(self):
        text = "Here is a link [example](http://example.com) in the text."
        links = extract_markdown_links(text)
        expected_links = [("example", "http://example.com")]
        self.assertEqual(links, expected_links)

    # test splitting nodes to extract images
    def test_split_nodes_image(self):
        old_nodes = [TextNode("Here is an image: ![Alt text](http://example.com/image.png)", TextType.PLAIN)]
        new_nodes = split_nodes_image(old_nodes)
        expected_nodes = [
            TextNode("Here is an image: ", TextType.PLAIN),
            TextNode("Alt text", TextType.IMAGE, "http://example.com/image.png")
        ]
        self.assertEqual(new_nodes, expected_nodes)

    # test splitting nodes with multiple images
    def test_split_nodes_multiple_images(self):
        old_nodes = [TextNode("Image one: ![Alt1](http://example.com/img1.png) and Image two: ![Alt2](http://example.com/img2.png)", TextType.PLAIN)]
        new_nodes = split_nodes_image(old_nodes)
        expected_nodes = [
            TextNode("Image one: ", TextType.PLAIN),
            TextNode("Alt1", TextType.IMAGE, "http://example.com/img1.png"),
            TextNode(" and Image two: ", TextType.PLAIN),
            TextNode("Alt2", TextType.IMAGE, "http://example.com/img2.png")
        ]
        self.assertEqual(new_nodes, expected_nodes)

    # test splitting nodes with no images
    def test_split_nodes_no_images(self):
        old_nodes = [TextNode("This is plain text with no images.", TextType.PLAIN)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertEqual(new_nodes, old_nodes)

    # test splitting nodes with non-plain text type for images
    def test_split_nodes_image_non_plain(self):
        old_nodes = [TextNode("![Alt text](http://example.com/image.png)", TextType.IMAGE, "http://example.com/image.png")]
        new_nodes = split_nodes_image(old_nodes)
        self.assertEqual(new_nodes, old_nodes)

    # test splitting nodes to extract links
    def test_split_nodes_link(self):
        old_nodes = [TextNode("Here is a link: [example](http://example.com)", TextType.PLAIN)]
        new_nodes = split_nodes_link(old_nodes)
        expected_nodes = [
            TextNode("Here is a link: ", TextType.PLAIN),
            TextNode("example", TextType.LINK, "http://example.com")
        ]
        self.assertEqual(new_nodes, expected_nodes)

    # test splitting nodes with multiple links
    def test_split_nodes_multiple_links(self):
        old_nodes = [TextNode("Link one: [One](http://example.com/one) and Link two: [Two](http://example.com/two)", TextType.PLAIN)]
        new_nodes = split_nodes_link(old_nodes)
        expected_nodes = [
            TextNode("Link one: ", TextType.PLAIN),
            TextNode("One", TextType.LINK, "http://example.com/one"),
            TextNode(" and Link two: ", TextType.PLAIN),
            TextNode("Two", TextType.LINK, "http://example.com/two")
        ]
        self.assertEqual(new_nodes, expected_nodes)

    # test splitting nodes with no links
    def test_split_nodes_no_links(self):
        old_nodes = [TextNode("This is plain text with no links.", TextType.PLAIN)]
        new_nodes = split_nodes_link(old_nodes)
        self.assertEqual(new_nodes, old_nodes)

    # test splitting nodes with non-plain text type for links
    def test_split_nodes_link_non_plain(self):
        old_nodes = [TextNode("example", TextType.LINK, "http://example.com")]
        new_nodes = split_nodes_link(old_nodes)
        self.assertEqual(new_nodes, old_nodes)

    # test converting complex text to text nodes
    def test_text_to_textnodes(self):
        complex_text = "This is **bold**, this is _italic_, this is `code`, this is a [link](http://example.com), and here is an image: ![Alt text](http://example.com/image.png)"
        new_nodes = text_to_textnodes(complex_text)
        expected_nodes = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(", this is ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(", this is ", TextType.PLAIN),
            TextNode("code", TextType.CODE),
            TextNode(", this is a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "http://example.com"),
            TextNode(", and here is an image: ", TextType.PLAIN),
            TextNode("Alt text", TextType.IMAGE, "http://example.com/image.png")
        ]
        self.assertEqual(new_nodes, expected_nodes)

# run the tests if this script is executed
if __name__ == '__main__':
    unittest.main()