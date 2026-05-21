from textnode import TextType, TextNode
from split_nodes_delimiter import split_nodes_delimiter
from split_nodes_delimiter import split_nodes_image, split_nodes_link

def text_to_textnodes(text):
    node_list = [TextNode(text=text,text_type=TextType.TEXT)]
    node_list = split_nodes_delimiter(node_list,"**",TextType.BOLD)
    node_list = split_nodes_delimiter(node_list,"_",TextType.ITALIC)
    node_list = split_nodes_delimiter(node_list,"`",TextType.CODE)
    node_list = split_nodes_image(node_list)
    node_list = split_nodes_link(node_list)
    return node_list
    
