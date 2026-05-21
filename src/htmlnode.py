class HTMLNode:
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        raise NotImplementedError
    def props_to_html(self):
        if not self.props: return ""
        output = " "
        for item in self.props:
            output = output + item + '="'
            output = output + self.props[item] + '" '
        output = output[0:(len(output)-1)]
        return output
    def __repr__(self):
        output = ""
        output = output + "TAG: "
        if (self.tag != None): output = output + self.tag
        output = output + "\n"
        output = output + "VALUE: "
        if (self.value != None): output = output + self.value
        output = output + "\n"
        output = output + "CHILDREN: "
        if (self.children != None):
            for item in self.children:
                output = output + print(item) + "\n"
        output = output + "\n"
        output = output + "PROPS: "
        if (self.tag != None): output = output + self.props_to_html()
        output = output + "\n"
        return output
    
class LeafNode(HTMLNode):    
    def __init__(self,tag,value,props=None):
        children = None
        super().__init__(tag,value,children,props)
    def to_html(self):
        if self.value is None: raise ValueError("Leaf has no value")
        if self.tag is None: return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    def __repr__(self):
        output = ""
        output = output + "TAG: "
        if (self.tag != None): output = output + self.tag
        output = output + "\n"
        output = output + "VALUE: "
        if (self.value != None): output = output + self.value
        output = output + "\n"
        output = output + "PROPS: "
        if (self.tag != None): output = output + self.props_to_html()
        output = output + "\n"
        return output

class ParentNode(HTMLNode):    
    def __init__(self,tag,children,props=None):
        value = ""
        super().__init__(tag,value,children,props)
    def to_html(self):
        if self.tag is None: raise ValueError("Parent has no tag")
        if self.children is None: raise ValueError("Parent has no children")
        output = f"<{self.tag}>"
        for child in self.children:
            output = output + child.to_html()
        output = output + f"</{self.tag}>"
        return output
    def __repr__(self):
        output = ""
        output = output + "TAG: "
        if (self.tag != None): output = output + self.tag
        output = output + "\n"
        output = output + "PROPS: "
        if (self.tag != None): output = output + self.props_to_html()
        output = output + "\n"
        return output
