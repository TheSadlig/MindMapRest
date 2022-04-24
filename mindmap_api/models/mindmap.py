from models.node import Node, NodeError
from models.db import db

class MindMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    map_name = db.Column(db.String(80), unique=True, nullable=False)

    root_node_id = db.Column(db.ForeignKey('node.id'), nullable=True)
    # We are better off eager-loading the root node
    root_node = db.relationship(Node, lazy="joined", innerjoin=False)
    
    def add_node_to_path(self, path, node_name):
        new_node = Node(node_name=node_name)
        db.session.add(new_node)
        db.session.flush()
        if path == '/':
            self.root_node = new_node
        else:
            if self.root_node is None:
                raise NodeError('Impossible to insert a anywhere but on `/` when there is no root node.', None)
            path_list = path.split('/')

            if path[0] != self.root_node.node_name:
                raise NodeError('The path does not correspond to the root node', self.root_node)
            
            path_list.pop(0)
            
            if len(path_list) == 0 or path_list[0] == '':
                new_node.parent_node = self.root_node
            else:
                parent_node = self.root_node.return_node_from_path(path_list)
                new_node.parent_node = parent_node
        db.session.commit()        
