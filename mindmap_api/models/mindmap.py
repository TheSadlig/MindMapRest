from models.node import Node, NodeError
from models.db import db

class MindMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    map_name = db.Column(db.String(80), unique=True, nullable=False)

    root_node_id = db.Column(db.ForeignKey('node.id'), nullable=True)
    # We are better off eager-loading the root node
    root_node = db.relationship(Node, lazy="joined", innerjoin=False)

    def create_root_node(self):
        new_node = Node(node_name='root')
        self.root_node = new_node
        return new_node
    
    def add_node_to_path(self, path, node_name):
        new_node = Node(node_name=node_name)
        db.session.add(new_node)
        db.session.flush()

        parent_node = self.find_node(path)
        new_node.parent_node = parent_node
        db.session.commit()    

    def pretty_print(self) -> str:
        if self.root_node == None:
            return ''
        else:
            return self.root_node.pretty_print(0)

    def find_node(self, path) -> Node:
        path_list = path.split('/')
        node = self.root_node.return_node_from_path(path_list)
        return node
