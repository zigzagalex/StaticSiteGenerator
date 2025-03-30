import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown: str) -> list[str]:
    raw_blocks = markdown.split("\n\n")

    blocks = []
    for block in raw_blocks:
        # Clean each line inside the block
        cleaned_lines = [line.strip() for line in block.strip().split("\n")]
        cleaned_block = "\n".join(cleaned_lines)
        if cleaned_block:
            blocks.append(cleaned_block)

    return blocks


def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")

    # CODE block: starts and ends with ```
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    # HEADING: first line starts with 1–6 # followed by a space
    if re.match(r"^#{1,6} ", lines[0]):
        return BlockType.HEADING

    # QUOTE: every line starts with >
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # UNORDERED LIST: every line starts with "- "
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # ORDERED LIST: lines start with incrementing 1. 2. 3. etc.
    if all(re.match(rf"^{i+1}\. ", line) for i, line in enumerate(lines)):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH