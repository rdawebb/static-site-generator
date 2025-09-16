# import the necessary modules
import unittest
from markdown_blocks import markdown_to_blocks, BlockType, block_to_block_type

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

# run the tests if this script is executed
if __name__ == "__main__":
    unittest.main()