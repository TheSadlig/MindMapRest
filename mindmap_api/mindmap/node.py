class Node:
    def __init__(self, node_name):
        self._node_name = node_name
        self._parent_node = None
        self._children = []
    
    def add_child(self, child_node):
        if child_node.parent == None:
            self._children.append(child_node)
            child_node.parent = self
        else:
            raise NodeAdditionError("Could not add child: the child already has a parent", self, child_node)
    
    @property
    def parent(self):
        return self._parent_node 
    
    @parent.setter
    def parent(self, node):
        self._parent_node = node

class NodeAdditionError(Exception):
    def __init__(self, parent_node, child_node):
        self._parent_node = parent_node
        self._child_node = child_node
    
    def __str__(self):
        return #TODO 