from models.db import db

class Node(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    node_name = db.Column(db.String(80), unique=False, nullable=False)

    parent_node_id = db.Column( db.ForeignKey('node.id'), nullable=True)
    parent_node = db.relationship('Node', lazy="select", remote_side=[id])

    def return_node_from_path(self, path_list, is_root_node=False):
        # If the path is empty, this node is the correct one
        if len(path_list) == 0 or path_list[0] == '':
            return self
        else:
            searched_node = path_list[0]
            child_node = Node.query.filter(Node.parent_node_id == self.id, Node.node_name == searched_node).first()

            if child_node is None:
                raise NodeError('Could not find child node with name ' + searched_node, self)
            path_list.pop(0)
            return child_node.return_node_from_path(path_list)

class NodeError(Exception):
    def __init__(self, message, node):
        self.node = node
        self.message = message
        super().__init__(self.message)
    
#    def __str__(self):
#        return #TODO 