import re
from typing import List
from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode, HTMLNode
from blocks import markdown_to_blocks, block_to_block_type, BlockType
from split import split_nodes_image, split_nodes_link, split_nodes_delimiter


def text_to_text_node(text: str) -> List[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    return nodes


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)

    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)

    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)

    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)

    elif text_node.text_type == TextType.LINK:
        if not text_node.url:
            raise ValueError("LINK TextNode must have a URL")
        return LeafNode("a", text_node.text, props={"href": text_node.url})

    elif text_node.text_type == TextType.IMAGE:
        if not text_node.url:
            raise ValueError("IMAGE TextNode must have a URL")
        return LeafNode("img", "", props={"src": text_node.url, "alt": text_node.text})

    else:
        raise ValueError(f"Unsupported text type: {text_node.text_type}")


def text_to_children(text: str) -> List[HTMLNode]:
    nodes = text_to_text_node(text)
    html_nodes = [text_node_to_html_node(node) for node in nodes]
    return html_nodes


def markdown_to_html_node(markdown_text):
    blocks = markdown_to_blocks(markdown_text)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            level = block.count("#", 0, block.find(" "))
            content = block[level + 1:].strip()
            child_nodes = text_to_children(content)
            children.append(ParentNode(f"h{level}", child_nodes))


        elif block_type == BlockType.PARAGRAPH:
            flat_text = " ".join(line.strip() for line in block.splitlines())
            child_nodes = text_to_children(flat_text)
            children.append(ParentNode("p", child_nodes))

        elif block_type == BlockType.CODE:
            # Strip ``` and wrap content as-is, no inline parsing
            code_text = "\n".join(block.split("\n")[1:-1]) + "\n"
            children.append(ParentNode("pre", [LeafNode("code", code_text)]))

        elif block_type == BlockType.QUOTE:
            # Remove leading > and process as paragraph
            lines = [line.lstrip("> ").strip() for line in block.split("\n")]
            quote_text = " ".join(lines)
            child_nodes = text_to_children(quote_text)
            children.append(ParentNode("blockquote", child_nodes))

        elif block_type == BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            list_items = []
            for line in lines:
                text = line.lstrip("- ").strip()
                child_nodes = text_to_children(text)
                list_items.append(ParentNode("li", child_nodes))
            children.append(ParentNode("ul", list_items))

        elif block_type == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            list_items = []
            for line in lines:
                # Strip number + ". " from start
                content = re.sub(r"^\d+\. ", "", line).strip()
                child_nodes = text_to_children(content)
                list_items.append(ParentNode("li", child_nodes))
            children.append(ParentNode("ol", list_items))

        else:
            raise Exception(f"Unhandled block type: {block_type}")

    return ParentNode("div", children)


