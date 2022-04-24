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

            child_node = self.get_child_by_name(searched_node)
            if child_node is None:
                raise NodeError('Could not find child node with name ' + searched_node, self)
            path_list.pop(0)
            return child_node.return_node_from_path(path_list)

    def get_child_by_name(self, name):
        node = Node.query.filter(Node.parent_node_id == self.id, Node.node_name == name).first()
        return node

    def get_all_children(self):
        children = Node.query.filter(Node.parent_node_id == self.id).all()
        return children

    def pretty_print(self, indentation_level):
        children = self.get_all_children()
        indentation_str = ' ' * indentation_level * 4
        if len(children) == 0:
            print(indentation_str + self.node_name)
        else:
            print(indentation_str + self.node_name + "/")
        for child in children:
            child.pretty_print(indentation_level + 1)


class NodeError(Exception):
    def __init__(self, message, node):
        self.node = node
        self.message = message
        super().__init__(self.message)
    
#    def __str__(self):
#        return #TODO 