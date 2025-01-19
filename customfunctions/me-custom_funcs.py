from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes =[]
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text
        while True:
            matches = extract_markdown_images(remaining_text)
            if not matches:
                break

            alt_text, image_url = matches[0]
            split_section = remaining_text.split(f"![{alt_text}]({image_url})", 1)

            if split_section[0]:
                new_nodes.append(TextNode(split_section[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, image_url))

            remaining_text = split_section[1] if len(split_section) > 1 else ""

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text
        while True:
            matches = extract_markdown_links(remaining_text)
            if not matches:
                break

            anchor_text, link_url = matches[0]
            split_section = remaining_text.split(f"[{anchor_text}]({link_url})", 1)

            if split_section[0]:
                new_nodes.append(TextNode(split_section[0], TextType.TEXT))
            new_nodes.append(TextNode(anchor_text, TextType.LINK, link_url))

            remaining_text = split_section[1] if len(split_section) > 1 else ""

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)      
    return (matches)
    
def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return (matches)

def text_to_textnodes(text):
    # Start with a single TextNode of type TEXT
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Process each type of markdown in sequence
    nodes = split_nodes_image(nodes)  # Extract images
    nodes = split_nodes_link(nodes)  # Extract links
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)  # Extract bold text
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)  # Extract italic text
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)  # Extract code blocks
    
    return nodes



def markdown_to_blocks(markdown):
    """
    Convert a raw Markdown string into a list of block strings.
    """
    # Normalize newlines and split into lines
    lines = markdown.splitlines()

    # Combine lines into blocks using newline-separated logic
    blocks = []
    current_block = []
    for line in lines:
        stripped_line = line.strip()
        if stripped_line == "":
            # If the line is empty, save the current block and reset
            if current_block:
                blocks.append(" ".join(current_block))
                current_block = []
        else:
            current_block.append(stripped_line)
    
    # Add the final block if it exists
    if current_block:
        blocks.append(" ".join(current_block))

    # Filter out any empty blocks (unlikely but safe check)
    blocks = [block for block in blocks if block]

    return blocks



def block_to_block_type(block):
    """
    Determine the type of a markdown block.

    Args:
        block (str): A block of markdown text.

    Returns:
        str: The type of markdown block: 'paragraph', 'heading', 'code', 'quote',
             'unordered_list', or 'ordered_list'.
    """
    lines = block.splitlines()

    # Check for code block
    if lines[0].startswith("```") and lines[-1].startswith("```"):
        return "code"

    # Check for heading
    if block.startswith("#") and block.lstrip("#").startswith(" "):
        return "heading"

    # Check for quote block
    if all(line.startswith(">") for line in lines):
        return "quote"

    # Check for unordered list block
    if all(line.startswith(("* ", "- ")) for line in lines):
        return "unordered_list"

    # Check for ordered list block
    if all(
        line.split(".")[0].isdigit() and line.split(".")[1].startswith(" ")
        for line in lines
    ):
        # Validate incremental order
        numbers = [int(line.split(".")[0]) for line in lines]
        if numbers == list(range(1, len(lines) + 1)):
            return "ordered_list"

    # If none of the above, it's a paragraph
    return "paragraph"
