import re
from textnode import TextNode, TextType
from extract import extract_markdown_images, extract_markdown_links


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        # Only split nodes that are raw text
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        # Sanity check: even = valid pairing, odd = unbalanced
        if len(parts) % 2 == 0:
            raise ValueError(f"Unmatched delimiter `{delimiter}` in text: {node.text}")

        for i, part in enumerate(parts):
            if i % 2 == 0:
                # Even index → normal text
                if part:
                    new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                # Odd index → marked up text
                if part:
                    new_nodes.append(TextNode(part, text_type))

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        images = extract_markdown_images(text)
        if not images:
            new_nodes.append(node)
            continue

        pattern = r'!\[([^\]]+)\]\(([^)]+)\)'
        matches = list(re.finditer(pattern, text))

        last_index = 0
        for match in matches:
            start, end = match.span()
            alt_text, url = match.groups()

            # Add text before image
            if start > last_index:
                before = text[last_index:start]
                if before:
                    new_nodes.append(TextNode(before, TextType.TEXT))

            # Add image node
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            last_index = end

        # Add any trailing text
        if last_index < len(text):
            remaining = text[last_index:]
            new_nodes.append(TextNode(remaining, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        links = extract_markdown_links(text)
        if not links:
            new_nodes.append(node)
            continue

        pattern = r'(?<!!)\[([^\]]+)\]\(([^)]+)\)'
        matches = list(re.finditer(pattern, text))

        last_index = 0
        for match in matches:
            start, end = match.span()
            anchor_text, url = match.groups()

            # Add text before link
            if start > last_index:
                before = text[last_index:start]
                if before:
                    new_nodes.append(TextNode(before, TextType.TEXT))

            # Add link node
            new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
            last_index = end

        # Add any trailing text
        if last_index < len(text):
            remaining = text[last_index:]
            new_nodes.append(TextNode(remaining, TextType.TEXT))

    return new_nodes