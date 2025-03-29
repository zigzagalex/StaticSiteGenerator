from textnode import *
from htmlnode import *


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


if __name__ == '__main__':
    testnode = TextNode('This is some anchor text', TextType.LINK,'https://www.boot.dev')
    print(testnode)