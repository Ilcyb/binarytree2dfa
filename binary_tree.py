from enum import Enum

class NodeValue(Enum):
    order = '.'
    choose = '+'
    Iteration = '*'
    concurrent = '||'

    @classmethod
    def has_value(cls, value):
        return (any(value == item.value for item in cls))

    @classmethod
    def is_binary_operator(cls, value):
        values = [item.value for item in cls if item != cls.Iteration]
        return value in values

    @classmethod
    def is_unary_operator(cls, value):
        return not cls.is_binary_operator(value)

class BinaryTree:

    current_layer = 1
    this_layer_count = 0
    layer_table = dict()

    def __init__(self, node, layer=1):
        self.node = node
        self.left_tree = None
        self.right_tree = None
        self.layer = layer
        if self.layer > self.current_layer:
            self.current_layer = self.layer
            self.this_layer_count = 0
            self.layer_table[self.current_layer] = list()
        self.this_layer_count += 1
        self.position = self.this_layer_count
        self.layer_table[self.current_layer].append(self)

    def insert_left(self, left_tree):
        self.left_tree = BinaryTree(left_tree, layer=self.layer + 1)
        self.left_tree.father = self

    def insert_right(self, right_tree):
        self.right_tree = BinaryTree(right_tree, layer=self.layer + 1)
        self.right_tree.father = self

    def has_child(self):
        return self.left_tree != None or self.right_tree != None

    def num_of_child(self):
        if self.has_child():
            if self.left_tree != None and self.right_tree != None:
                return 2
            else:
                return 1
        return 0
    
    def validity(self):
        # 验证二叉树的非叶子结点是否为指定的值
        if self.has_child() and not NodeValue.has_value(self.node):
            return False
        # 验证以双目运算符为结点的子树是否有两个孩子结点
        if (NodeValue.is_binary_operator(self.node) and self.num_of_child() != 2):
            return False
        # 验证以单目运算符为结点的子树是否只有一个孩子结点
        if (NodeValue.is_unary_operator(self.node) and self.num_of_child() != 1):
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

    @classmethod
    def clean(cls):
        cls.current_layer = 1
        cls.this_layer_count = 0
        cls.layer_table = dict()