from typing import List, Dict, Optional

class HTMLNode(object):
    def __init__(self,
                 tag: Optional[str]=None,
                 value: Optional[str]=None,
                 children: Optional[List]=None,
                 props: Optional[Dict] = None):
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
