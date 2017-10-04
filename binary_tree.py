from enum import Enum

class NodeValue(Enum):
    order = '.'
    choose = '+'
    Iteration = '*'
    concurrent = '||'

    @classmethod
    def has_value(cls, value):
        return (any(value == item.value for item in cls))

class BinaryTree:

    def __init__(self, node):
        self.node = node
        self.left_tree = None
        self.right_tree = None
        self.layer = 1

    def insert_left(self, left_tree):
        self.left_tree = left_tree
        self.left_tree.father = self
        self.left_tree.layer = self.layer + 1

    def insert_right(self, right_tree):
        self.right_tree = right_tree
        self.right_tree.father = self
        self.right_tree.layer = self.layer + 1
    
    def validity(self):
        if (self.left_tree != None or self.right_tree != None) and not NodeValue.has_value(self.node):
            return False
        return True

    def get_concurrent_node(self, result_set):
        if self.node == NodeValue.concurrent:
            result_set.append(self)
        if(self.left_tree != None):
            result_set = self.get_concurrent_node(self.left_tree, result_set)
        if(self.right_tree != None):
            result_set = self.get_concurrent_node(self.right_tree, result_set)
        return result_set