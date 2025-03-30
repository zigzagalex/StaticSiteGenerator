from textnode import *
from htmlnode import *
from typing import List
from split import *




if __name__ == '__main__':
    testnode = TextNode('This is some anchor text', TextType.LINK,'https://www.boot.dev')
    print(testnode)