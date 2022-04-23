from mindmap.node import Node

class MindMap:
    def __init__(self, map_id):
        self._map_id = map_id
        self._root = Node('root')
    
    def add_node_to_path(path, node):
        if path == '/':
            self._root.add_child(node)
        else:
            return # TODO