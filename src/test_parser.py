import unittest

from parser import *
from textnode import TextNode, TextType, text_node_to_html_node
from blocktype import BlockType

class TestParser(unittest.TestCase):
    def test_parser_1(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT, None)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
    TextNode("This is text with a ", TextType.TEXT),
    TextNode("bolded phrase", TextType.BOLD),
    TextNode(" in the middle", TextType.TEXT),
])
        
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"),("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_split_link(self):
        node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])

   

        self.assertListEqual(new_nodes, [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ])

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

    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

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
         
    def test_heading_h1(self):
        text = "# This is a heading"
        self.assertEqual(block_to_block_type(text), BlockType.HEADING)
    
    def test_heading_h2(self):
        text = "## Second level heading"
        self.assertEqual(block_to_block_type(text), BlockType.HEADING)
    
    def test_heading_h6(self):
        text = "###### Sixth level heading"
        self.assertEqual(block_to_block_type(text), BlockType.HEADING)
    
    def test_heading_with_no_space_is_not_heading(self):
        text = "#No space after hash"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)
    
    def test_heading_with_too_many_hashes(self):
        text = "####### Seven hashes"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)
    
    def test_code_block_single_line(self):
        text = "```code here```"
        self.assertEqual(block_to_block_type(text), BlockType.CODE)
    
    def test_code_block_multiline(self):
        text = """```
def hello():
    print("world")
````"""
        self.assertEqual(block_to_block_type(text), BlockType.CODE)
    
    def test_code_block_with_language(self):
        text = """```python
print("Hello")
```"""
        self.assertEqual(block_to_block_type(text), BlockType.CODE)
    
    def test_incomplete_code_block(self):
        text = "```code without closing"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)
    
    def test_quote_single_line(self):
        text = "> This is a quote"
        self.assertEqual(block_to_block_type(text), BlockType.QUOTE)
    
    def test_quote_multiline(self):
        text = """> First line of quote
> Second line of quote
> Third line of quote"""
        self.assertEqual(block_to_block_type(text), BlockType.QUOTE)
    
    def test_unordered_list_single_item(self):
        text = "- Single item"
        self.assertEqual(block_to_block_type(text), BlockType.ULIST)
    
    def test_unordered_list_multiple_items(self):
        text = """- First item
- Second item
- Third item"""
        self.assertEqual(block_to_block_type(text), BlockType.ULIST)
    
    def test_unordered_list_with_longer_content(self):
        text = """- This is a longer item with more text
- Another item here
- Final item"""
        self.assertEqual(block_to_block_type(text), BlockType.ULIST)
    
    def test_ordered_list_single_item(self):
        text = "1. First item"
        self.assertEqual(block_to_block_type(text), BlockType.OLIST)
    
    def test_ordered_list_multiple_items(self):
        text = """1. First item
2. Second item
3. Third item"""
        self.assertEqual(block_to_block_type(text), BlockType.OLIST)
    
    def test_ordered_list_must_start_with_1(self):
        text = """2. Starting with 2
3. Third item"""
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)
    
    def test_ordered_list_must_be_sequential(self):
        text = """1. First item
2. Second item
4. Skipped 3"""
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)
    
    def test_ordered_list_needs_space_after_dot(self):
        text = """1.No space
2.Also no space"""
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)
    
    def test_paragraph_plain_text(self):
        text = "This is just a paragraph of text."
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)
    
    def test_paragraph_multiline(self):
        text = """This is a paragraph
with multiple lines
but no special formatting"""
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)
    
    def test_paragraph_with_mixed_content(self):
        text = """Some text
- Not a complete list
More text"""
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)
    
    def test_empty_string(self):
        text = ""
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

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