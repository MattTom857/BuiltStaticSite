from enum import Enum

def markdown_to_blocks(markdown):
    Stage1 = markdown.split("\n\n")
    Stage2 = []
    for block in Stage1:
        block = block.strip()
        if (block != ""):
            Stage2.append(block)
    return Stage2

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    if (block.startswith(("# ","## ","### ",
                          "#### ","##### ","###### "))):
        return BlockType.HEADING
    if (block[0:4] == "```\n"):
        if (block[-4:] == "\n```"): return BlockType.CODE

    is_quote = False
    is_unordered = False
    is_ordered = False
    lines = block.split("\n")
    if (lines[0][0:1] == ">"):
        is_quote = True
        for line in lines:
            if (line[0] != ">"):
                is_quote = False
                break
    if (lines[0][0:2] == "- "):
        is_unordered = True
        for line in lines:
            if (line[0:2] != "- "):
                is_unordered = False
                break
    if (lines[0][0:3] == "1. "):
        is_ordered = True
        i1 = 1
        for line in lines:
            if not (line.startswith(f"{i1}. ")):
                is_ordered = False
                break
            i1 = i1 + 1
    if (is_quote == True): return BlockType.QUOTE
    if (is_unordered == True): return BlockType.UNORDERED_LIST
    if (is_ordered == True): return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
