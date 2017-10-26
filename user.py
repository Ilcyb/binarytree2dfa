from os import environ

import MySQLdb

from binary_tree import BinaryTree, NodeValue


class RollBackException(Exception):
    def __init__(self):
        super().__init__()


class User:
    def __init__(self):
        self.trees = list()

    def build_a_binary_tree(self):
        while (True):
            try:
                total_layer = int(input('请输入要构建的二叉树的层数:'))
            except ValueError:
                print('请输入正确的层数')
            else:
                if total_layer <= 0:
                    print('请输入正确的层数')
                else:
                    break
        root_node = input('请输入根节点')
        tree = BinaryTree(root_node)
        for layer in range(1, total_layer):
            for position in range(len(BinaryTree.layer_table[layer])):
                temp_tree = BinaryTree.layer_table[layer][position]
                if NodeValue.has_value(temp_tree.node):
                    sub_left_tree = input('请输入第%s层第%s个结点(%s)的左子树，若没有则输入回车' %
                                        (layer, position + 1, temp_tree.node))
                    sub_right_tree = input('请输入第%s层第%s个结点(%s)的右子树，若没有则输入回车' %
                                        (layer, position + 1, temp_tree.node))
                    if sub_left_tree != '':
                        temp_tree.insert_left(sub_left_tree)
                    if sub_right_tree != '':
                        temp_tree.insert_right(sub_right_tree)
                else:
                    pass
        if tree.validity():
            print('二叉树构建成功')
            BinaryTree.clean()
            return tree
        else:
            print('你构建的二叉树不符合规则，构建失败')
            BinaryTree.clean()
            return False

    def display_all_concurrent_node(self, tree):
        self.trees = tree.get_concurrent_node(self.trees)

    def enter_regular_exp(self):
        print('请给构建的二叉树的每一个并发子树都输入一个正则表达式')
        for tree in self.trees:
            tree.regex = input('请输入第%s层,第%s位的子树(%s)对应的正则表达式' %
                               (tree.layer, tree.position, tree.node))
