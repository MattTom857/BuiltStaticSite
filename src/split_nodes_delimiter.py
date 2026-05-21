from textnode import TextType, TextNode, text_node_to_html_node
from extract_markdown import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    master_nodes = []
    for old_node in old_nodes:
        new_nodes = split_node_delimiter(old_node,delimiter,text_type)
        master_nodes.extend(new_nodes)
    return master_nodes

def split_node_delimiter(old_node,delimiter,text_type):
    if (old_node.text_type != TextType.TEXT):
        return [old_node]
    if (text_type == TextType.TEXT): return [old_node]
    d_count = old_node.text.count(delimiter)
    if (d_count == 0): return[old_node]
    if (d_count < 2):
        raise Exception("Need two delimiters to section off text")
    if (d_count % 2 == 1):
        raise Exception("Odd number of delimiters means you're missing one")
    
    pieces = old_node.text.split(delimiter)
    new_nodes = []
    for i1, piece in enumerate(pieces):
        if (piece == ""):
            continue
        node_type = TextType.TEXT if i1 % 2 == 0 else text_type
        new_nodes.append(TextNode(text=piece,text_type=node_type))
    return new_nodes

def split_nodes_image(old_nodes):
    master_nodes = []
    for old_node in old_nodes:
        new_nodes = split_node_image(old_node)
        master_nodes.extend(new_nodes)
    return master_nodes

def split_node_image(old_node):
    if (old_node.text_type != TextType.TEXT):
        return [old_node]
    found_images = extract_markdown_images(old_node.text)
    if not found_images: return [old_node]

    node_list = []
    remaining_text = old_node.text
    for image in found_images:
        target_text = f"![{image[0]}]({image[1]})"
        split_text = remaining_text.split(target_text,1)
        if (split_text[0] != ""):
            node_list.append(TextNode(text=split_text[0],
                                      text_type=TextType.TEXT))
        node_list.append(TextNode(text=image[0],
                                  text_type=TextType.IMAGE,
                                  url=image[1]))
        remaining_text = split_text[1]
    if (remaining_text != ""):
        node_list.append(TextNode(text=remaining_text,
                                  text_type=TextType.TEXT))
    return node_list

def split_nodes_link(old_nodes):
    master_nodes = []
    for old_node in old_nodes:
        new_nodes = split_node_link(old_node)
        master_nodes.extend(new_nodes)
    return master_nodes

def split_node_link(old_node):
    if (old_node.text_type != TextType.TEXT):
        return [old_node]
    found_links = extract_markdown_links(old_node.text)
    if not found_links: return [old_node]

    node_list = []
    remaining_text = old_node.text
    for link in found_links:
        target_text = f"[{link[0]}]({link[1]})"
        split_text = remaining_text.split(target_text,1)
        if (split_text[0] != ""):
            node_list.append(TextNode(text=split_text[0],
                                      text_type=TextType.TEXT))
        node_list.append(TextNode(text=link[0],
                                  text_type=TextType.LINK,
                                  url=link[1]))
        remaining_text = split_text[1]
    if (remaining_text != ""):
        node_list.append(TextNode(text=remaining_text,
                                  text_type=TextType.TEXT))
    return node_list


