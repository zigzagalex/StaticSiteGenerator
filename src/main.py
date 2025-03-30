from textnode import TextNode, TextType



if __name__ == '__main__':
    testnode = TextNode('This is some anchor text', TextType.LINK,'https://www.boot.dev')
    print(testnode)