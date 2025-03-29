from typing import List, Dict, Optional


class HTMLNode(object):
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        children: Optional[List] = None,
        props: Optional[Dict] = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ""
        return " " + " ".join(f'{key}="{value}"' for key, value in self.props.items())

    def __repr__(self):
        return (
            f"HTMLNode(tag={self.tag!r}, value={self.value!r}, "
            f"children={self.children!r}, props={self.props!r})"
        )


class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: Optional[Dict] = None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("value cannot be None")
        if self.tag is None:
            return str(self.value)
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: List, props: Optional[Dict] = None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("No tag for parent node")
        elif self.children is None:
            raise ValueError("No children for parent node")
        # Recursively generate HTML for all child nodes
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}>{children_html}</{self.tag}>"