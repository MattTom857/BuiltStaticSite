import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextType, TextNode, text_node_to_html_node
from split_nodes_delimiter import split_nodes_delimiter
from extract_markdown import extract_markdown_images, extract_markdown_links
from split_nodes_delimiter import split_nodes_image, split_nodes_link
from text_to_textnodes import text_to_textnodes
from blocks import markdown_to_blocks, BlockType, block_to_block_type
from markdown_to_html import markdown_to_html_node

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_two(self):
        tag1 = "p"
        value1 = "This is right."
        props1 = {"href":"https://website1.com",
                  "target":"_blank"}
        node1 = HTMLNode(tag=tag1,value=value1,props=props1)
        output1 = 'href="https://website1.com" target="_blank"'
        self.assertEqual(node1.props_to_html(),output1)
    def test_props_to_html_with_one(self):
        tag1 = "p"
        value1 = "This is right."
        props1 = {"href":"https://website1.com"}
        node1 = HTMLNode(tag=tag1,value=value1,props=props1)
        output1 = 'href="https://website1.com"'
        self.assertEqual(node1.props_to_html(),output1)
    def test_props_to_html_with_none(self):
        tag1 = "p"
        value1 = "This is right."
        props1 = {}
        node1 = HTMLNode(tag=tag1,value=value1,props=props1)
        output1 = ""
        self.assertEqual(node1.props_to_html(),output1)
    def test_props_to_html_with_blank(self):
        tag1 = "p"
        value1 = "This is right."
        node1 = HTMLNode(tag=tag1,value=value1)
        output1 = ''
        self.assertEqual(node1.props_to_html(),output1)
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_leaf_to_html_tag_blank(self):
        node = LeafNode("", "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag,None)
        self.assertEqual(html_node.value, "This is a text node")
    def test_bold(self):
        node = TextNode("This is a boldface node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag,"b")
        self.assertEqual(html_node.value, "This is a boldface node")
    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag,"i")
        self.assertEqual(html_node.value,"This is an italic node")
    def test_codeblock(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag,"code")
        self.assertEqual(html_node.value,"This is a code node")
    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK,
                        "https://IGoNowhere.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag,"a")
        self.assertEqual(html_node.value,"This is a link node")
        self.assertEqual(html_node.props["href"],"https://IGoNowhere.com")
    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE,
                        "https://IGoNowhere.com/NoGood.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag,"img")
        self.assertEqual(html_node.value,"")
        self.assertEqual(html_node.props["src"],"https://IGoNowhere.com/NoGood.jpg")
        self.assertEqual(html_node.props["alt"],"This is an image node")
    def test_split_start(self):
        nodes = [TextNode("**This** is bold at the beginning",TextType.TEXT)]
        split_nodes = split_nodes_delimiter(nodes,"**",TextType.BOLD)
        self.assertEqual(split_nodes[0].text,"This")
        self.assertEqual(split_nodes[0].text_type,TextType.BOLD)
        self.assertEqual(split_nodes[1].text," is bold at the beginning")
        self.assertEqual(split_nodes[1].text_type,TextType.TEXT)
    def test_split_middle(self):
        nodes = [TextNode("This is _italics_ in the middle",TextType.TEXT)]
        split_nodes = split_nodes_delimiter(nodes,"_",TextType.ITALIC)
        self.assertEqual(split_nodes[0].text,"This is ")
        self.assertEqual(split_nodes[0].text_type,TextType.TEXT)
        self.assertEqual(split_nodes[1].text,"italics")
        self.assertEqual(split_nodes[1].text_type,TextType.ITALIC)
        self.assertEqual(split_nodes[2].text," in the middle")
        self.assertEqual(split_nodes[2].text_type,TextType.TEXT)
    def test_split_end(self):
        nodes = [TextNode("This is code at the `end`",TextType.TEXT)]
        split_nodes = split_nodes_delimiter(nodes,"`",TextType.CODE)
        self.assertEqual(split_nodes[0].text,"This is code at the ")
        self.assertEqual(split_nodes[0].text_type,TextType.TEXT)
        self.assertEqual(split_nodes[1].text,"end")
        self.assertEqual(split_nodes[1].text_type,TextType.CODE)
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")],
                             matches)
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://www.doi.org/10.fraud)"
        )
        self.assertListEqual([("link","https://www.doi.org/10.fraud")],
                             matches)
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link1](https://doi.org/fraud1.pdf) and another [link2](https://doi.org/fraud2.pdf)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "https://doi.org/fraud1.pdf"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "https://doi.org/fraud2.pdf"),
            ],
            new_nodes,
        )
    def test_text_to_textnodes(self):
        test_text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        node_list = text_to_textnodes(test_text)
        self.assertEqual(node_list[0],
                             TextNode("This is ", TextType.TEXT))
        self.assertEqual(node_list[1],
                             TextNode("text", TextType.BOLD))
        self.assertEqual(node_list[2],
                             TextNode(" with an ", TextType.TEXT))
        self.assertEqual(node_list[3],
                             TextNode("italic", TextType.ITALIC))
        self.assertEqual(node_list[4],
                             TextNode(" word and a ", TextType.TEXT))
        self.assertEqual(node_list[5],
                             TextNode("code block", TextType.CODE))
        self.assertEqual(node_list[6],
                             TextNode(" and an ", TextType.TEXT))
        self.assertEqual(node_list[7],
                             TextNode("obi wan image", TextType.IMAGE,
                                      "https://i.imgur.com/fJRm4Vk.jpeg"))
        self.assertEqual(node_list[8],
                             TextNode(" and a ", TextType.TEXT))
        self.assertEqual(node_list[9],
                             TextNode("link", TextType.LINK, "https://boot.dev"))
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
    def test_block_to_block_type_headings(self):
        md = """
                # Heading1

                ## Heading2

                ### Heading3

                #### Heading4

                ##### Heading5

                ###### Heading6
            """
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks,
                         ["# Heading1","## Heading2","### Heading3",
                          "#### Heading4","##### Heading5","###### Heading6"])
        self.assertEqual(block_to_block_type(blocks[0]),BlockType.HEADING)
        self.assertEqual(block_to_block_type(blocks[1]),BlockType.HEADING)
        self.assertEqual(block_to_block_type(blocks[2]),BlockType.HEADING)
        self.assertEqual(block_to_block_type(blocks[3]),BlockType.HEADING)
        self.assertEqual(block_to_block_type(blocks[4]),BlockType.HEADING)
        self.assertEqual(block_to_block_type(blocks[5]),BlockType.HEADING)
    def test_block_to_block_type_code(self):
        code_text = "i1 = 5; while (i1 > 0) {\n"
        code_text = code_text + 'print("This sucks!")\n'
        code_text = code_text + 'i1 = i1 - 1;\n'
        code_text = code_text + '}\n'
        md = "```\n" + code_text + "```"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks,[md])
        self.assertEqual(block_to_block_type(blocks[0]),BlockType.CODE)
    def test_block_to_block_type_quote(self):
        md1 = "> This is line 1.\n"
        md1 = md1 + "> This is line 2.\n"
        md2 = md1 + "This is a bad line 3."
        md1 = md1 + "> This is a good line 3."
        blocks1 = markdown_to_blocks(md1)
        blocks2 = markdown_to_blocks(md2)
        self.assertEqual(block_to_block_type(blocks1[0]),
                         BlockType.QUOTE)
        self.assertEqual(block_to_block_type(blocks2[0]),
                         BlockType.PARAGRAPH)
    def test_block_to_block_type_unordered(self):
        md1 = "- This is line 1.\n"
        md1 = md1 + "- This is line 2.\n"
        md2 = md1 + "This is a bad line 3."
        md1 = md1 + "- This is a good line 3."
        blocks1 = markdown_to_blocks(md1)
        blocks2 = markdown_to_blocks(md2)
        self.assertEqual(block_to_block_type(blocks1[0]),
                         BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(blocks2[0]),
                         BlockType.PARAGRAPH)
    def test_block_to_block_type_ordered(self):
        md1 = "1. This is line 1.\n"
        md1 = md1 + "2. This is line 2.\n"
        md2 = md1 + "This is a bad line 3."
        md1 = md1 + "3. This is a good line 3."
        blocks1 = markdown_to_blocks(md1)
        blocks2 = markdown_to_blocks(md2)
        self.assertEqual(block_to_block_type(blocks1[0]),
                         BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type(blocks2[0]),
                         BlockType.PARAGRAPH)

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

if __name__ == "__main__":
    unittest.main()