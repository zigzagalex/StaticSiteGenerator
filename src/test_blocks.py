import unittest
from blocks import BlockType, block_to_block_type, markdown_to_blocks


class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Deep Heading"), BlockType.HEADING)
        self.assertNotEqual(block_to_block_type("####### Too Deep"), BlockType.HEADING)

    def test_code(self):
        code_block = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(code_block), BlockType.CODE)

    def test_quote(self):
        quote_block = "> Quote line 1\n> Quote line 2"
        self.assertEqual(block_to_block_type(quote_block), BlockType.QUOTE)

    def test_unordered_list(self):
        ul_block = "- item one\n- item two\n- item three"
        self.assertEqual(block_to_block_type(ul_block), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        ol_block = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(ol_block), BlockType.ORDERED_LIST)

    def test_ordered_list_wrong_numbers(self):
        broken_ol = "1. first\n3. wrong"
        self.assertEqual(block_to_block_type(broken_ol), BlockType.PARAGRAPH)

    def test_paragraph(self):
        para = "Just a plain old paragraph.\nWith multiple lines.\nNothing fancy."
        self.assertEqual(block_to_block_type(para), BlockType.PARAGRAPH)

    def test_markdown_to_block(self):
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

if __name__ == "__main__":
    unittest.main()