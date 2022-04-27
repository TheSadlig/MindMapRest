from mindmap_api.models.db import db
import json

class Node(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    node_name = db.Column(db.String(80), unique=False, nullable=False)

    parent_node_id = db.Column( db.ForeignKey('node.id'), nullable=True)
    parent_node = db.relationship('Node', lazy="select", remote_side=[id])

    def return_node_from_path(self, path_list):
        # If the path is empty, this node is the correct one
        if len(path_list) == 0 or path_list[0] == '':
            return self
        else:
            searched_node = path_list[0]

            child_node = self.get_child_by_name(searched_node)
            if child_node == None:
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
            return indentation_str + self.node_name + '\n'

        res_str = ''
        for child in children:
            res_str += child.pretty_print(indentation_level + 1)
        return indentation_str + self.node_name + "/\n" + res_str

    def get_path(self):
        parent_node = self.parent_node
        # Writing the path from right to left
        path = self.node_name

        while parent_node != None and parent_node.parent_node != None:
            path = parent_node.node_name + '/' + path
            parent_node = parent_node.parent_node
        return path

    def get_json(self):
        data = {}
        data['path'] = self.get_path()
        
        children = self.get_all_children()
        data['text'] = []
        for child in children:
            data['text'].append(child.node_name) 
        return json.dumps(data)


class NodeError(Exception):
    def __init__(self, message, node):
        self.node = node
        self.message = message
        super().__init__(self.message)
    
#    def __str__(self):
#        return #TODO 