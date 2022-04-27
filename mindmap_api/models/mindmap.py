from mindmap_api.models.node import Node, NodeError
from mindmap_api.models.db import db
import json

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
    
    def add_node_to_path(self, path, node_name) -> Node:
        return self.find_node(path).add_child(node_name)

    def pretty_print(self) -> str:
        if self.root_node == None:
            return ''
        else:
            return self.root_node.pretty_print(0)

    def find_node(self, path) -> Node:
        path_list = path.split('/')
        node = self.root_node.return_node_from_path(path_list)
        return node

    def get_json(self):
        data = {}
        data['id'] = self.map_name
        
        return json.dumps(data)
