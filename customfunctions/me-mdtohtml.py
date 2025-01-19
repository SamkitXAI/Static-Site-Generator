from textnode import *
from leafnode import LeafNode
from parentnode import ParentNode
from custom_funcs import *

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)  # Split the markdown into blocks
    parent_node = ParentNode("div", [])  # The parent container for all blocks
    
    for block in blocks:
        block_type = block_to_block_type(block)  # Determine block type
        
        # Process based on block type
        if block_type == "paragraph":
            # For paragraph, wrap text in <p> tag
            children = text_to_children(block)  # Inline elements like bold, italics, links, etc.
            node = ParentNode("p", children)
        
        elif block_type == "heading":
            # For heading, wrap text in <h1> to <h6> based on the heading level
            level = block.count("#")  # Number of '#' indicates heading level
            children = text_to_children(block)
            node = ParentNode(f"h{level}", children)
        
        elif block_type == "quote":
            # For quote, wrap in <blockquote> tag
            children = text_to_children(block)
            node = ParentNode("blockquote", children)
        
        elif block_type == "unordered_list":
            # For unordered list, wrap in <ul> with <li> for each list item
            list_items = block.splitlines()
            children = [ParentNode("li", text_to_children(item)) for item in list_items]
            node = ParentNode("ul", children)
        
        elif block_type == "ordered_list":
            # For ordered list, wrap in <ol> with <li> for each list item
            list_items = block.splitlines()
            children = [ParentNode("li", text_to_children(item)) for item in list_items]
            node = ParentNode("ol", children)
        
        elif block_type == "code":
            # For code block, wrap in <pre><code> tags
            children = [LeafNode("code", block.strip())]  # Clean up the block for code content
            node = ParentNode("pre", [ParentNode("code", children)])
        
        # Add the created node to the parent node
        parent_node.children.append(node)

    return parent_node

def text_to_children(text):
    """Converts a block of text into a list of child HTML nodes (inline elements like bold, italics, links)."""
    nodes = text_to_textnodes(text)  # Use previously created function to process inline text elements
    return [text_node_to_html_node(node) for node in nodes]