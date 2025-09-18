# import the necessary modules
import unittest
from markdown_blocks import markdown_to_blocks, BlockType, block_to_block_type, markdown_to_html_node
from generate_content import extract_title

# define the test case class
class TestMarkdownBlocks(unittest.TestCase):
    # test converting markdown to blocks
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    # test converting markdown with multiple newlines to blocks
    def test_markdown_to_blocks_multiple_newlines(self):
        md = """
This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    # test determining block types
    def test_block_to_block_type(self):
        # test headings
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#### Heading 4"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("##### Heading 5"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        
        # test code block
        self.assertEqual(
            block_to_block_type("```\nThis is a code block\n```"),
            BlockType.CODE,
        )
        
        # test quote block
        self.assertEqual(
            block_to_block_type("> This is a quote\n> spanning two lines"),
            BlockType.QUOTE,
        )
        
        # test ordered list block
        self.assertEqual(
            block_to_block_type("1. First item\n2. Second item\n3. Third item"),
            BlockType.ORDERED_LIST,
        )
        
        # test unordered list block
        self.assertEqual(
            block_to_block_type("- Item 1\n- Item 2\n- Item 3"),
            BlockType.UNORDERED_LIST,
        )
        
        # test paragraph block
        self.assertEqual(
            block_to_block_type("This is a simple paragraph."),
            BlockType.PARAGRAPH,
        )

    # test converting paragraph block to HTMLNode
    def test_paragraph_to_html(self):
        markdown = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    # test multiple paragraphs to HTMLNodes
    def test_multiple_paragraphs(self):
        markdown = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    # test headings to HTMLNodes
    def test_headings(self):
        markdown = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    # test code block to HTMLNodes
    def test_code(self):
        markdown = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )

    # test quote block to HTMLNodes
    def test_blockquote(self):
        markdown = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    # test ordered and unordered lists to HTMLNodes
    def test_lists(self):
        markdown = """
- This is an unordered list
- with items
- and more items

1. This is an ordered list
2. with items
3. and more items

"""

        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is an unordered list</li><li>with items</li><li>and more items</li></ul><ol><li>This is an ordered list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    # test invalid block type raises error
    def test_invalid_block_type(self):
        markdown = """
This is a paragraph
```
This is an invalid code block
"""
        with self.assertRaises(ValueError):
            markdown_to_html_node(markdown)

    # test extracting title from markdown
    def test_extract_title(self):
        markdown = """
# My Document Title

Some paragraph text here.
````
More text.
````
> A quote here.
- A list item.
"""
        title = extract_title(markdown)
        self.assertEqual(title, "My Document Title")


    # test extracting title when no heading present
    def test_extract_title_no_heading(self):
        markdown = """
This document has no title.

Some paragraph text here.
````
More text.
````
> A quote here.
- A list item.
"""
        with self.assertRaises(Exception):
            extract_title(markdown)


# run the tests if this script is executed
if __name__ == "__main__":
    unittest.main()