from enum import Enum
from binarytree import Node, show, _set_left, _set_right


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


class BinaryTree(Node):

    current_layer = 1
    this_layer_count = 0
    layer_table = {1: []}

    def __init__(self, node, layer=1):
        super().__init__(node)  # 适配BinaryTree第三方库
        self.node = node
        self.left_tree = None
        self.right_tree = None
        self.layer = layer
        if self.layer > BinaryTree.current_layer:
            BinaryTree.current_layer = self.layer
            BinaryTree.this_layer_count = 0
            BinaryTree.layer_table[BinaryTree.current_layer] = list()
        BinaryTree.this_layer_count += 1
        self.position = BinaryTree.this_layer_count
        BinaryTree.layer_table[BinaryTree.current_layer].append(self)

    def insert_left(self, left_tree):
        self.left_tree = BinaryTree(left_tree, layer=self.layer + 1)
        _set_left(self, self.left_tree)  # 适配BinaryTree第三方库
        self.left_tree.father = self

    def insert_right(self, right_tree):
        self.right_tree = BinaryTree(right_tree, layer=self.layer + 1)
        _set_right(self, self.right_tree)  # 适配BinaryTree第三方库
        self.right_tree.father = self

    def has_child(self):
        return self.left_tree != None or self.right_tree != None

    def has_left_child(self):
        return self.left_tree != None

    def has_right_child(self):
        return self.right_tree != None

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
        if self.node == NodeValue.concurrent.value:
            result_set.append(self)
        if(self.left_tree != None):
            result_set = self.left_tree.get_concurrent_node(result_set)
        if(self.right_tree != None):
            result_set = self.right_tree.get_concurrent_node(result_set)
        return result_set

    def gen_regex(self, regex_str):
        if self.has_left_child():
            if self.node == NodeValue.choose.value:
                regex_str += '('
            if self.node == NodeValue.Iteration.value:
                regex_str += '('
            regex_str = self.left_tree.gen_regex(regex_str)
        if self.node == NodeValue.order.value:  # 顺序
            regex_str = self.right_tree.gen_regex(regex_str)
        if self.node == NodeValue.choose.value:  # 选择
            regex_str = regex_str + '|'
            regex_str = self.right_tree.gen_regex(regex_str)
            regex_str = regex_str + ')'
        if self.node == NodeValue.Iteration.value:  # 迭代
            if self.has_left_child():
                regex_str = regex_str + '*)'
            else:
                regex_str = regex_str + '('
                regex_str = self.right_tree.gen_regex(regex_str)
                regex_str = regex_str + '*)'
        if not NodeValue.has_value(self.node):
            regex_str += self.node
        return regex_str

    def show(self):
        show(self)

    @classmethod
    def clean(cls):
        cls.current_layer = 1
        cls.this_layer_count = 0
        cls.layer_table = {1: []}
