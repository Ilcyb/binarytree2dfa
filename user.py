from os import environ

import MySQLdb

from binary_tree import BinaryTree


class RollBackException(Exception):
    def __init__(self):
        super().__init__()


class User:
    def __init__(self, username, grade, id):
        self.username = username
        self.grade = grade
        self.trees = list()
        self.saveToDB = True
        self.user_db_id = id

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
                sub_left_tree = input('请输入第%s层第%s个结点(%s)的左子树，若没有则输入回车' %
                                      (layer, position + 1, temp_tree.node))
                sub_right_tree = input('请输入第%s层第%s个结点(%s)的右子树，若没有则输入回车' %
                                       (layer, position + 1, temp_tree.node))
                if sub_left_tree != '':
                    temp_tree.insert_left(sub_left_tree)
                if sub_right_tree != '':
                    temp_tree.insert_right(sub_right_tree)
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

    def save(self, tree):
        try:
            conn = MySQLdb.connect(host='139.199.228.34', user=environ.get('mysql_username'),
                                   passwd=environ.get('mysql_password'), db='dfa')
            cur = conn.cursor()
            # 开启事务
            cur.execute('begin')
            root_id = self.save_to_db(tree, cur)
            if root_id == False:
                return False
            else:
                cur.execute('''insert into user_tree(tree_id,user_id) 
                                values(%s,%s)''' % (root_id, self.user_db_id))
        except MySQLdb.Error as e:
            print('将二叉树存储进数据库时发生错误:%s' % (e,))
            print('此次存储将撤销，数据将回滚')
            cur.execute('rollback')
            return False
        except RollBackException:
            return False
        else:
            cur.execute('commit')
            print('存储成功，二叉树ID:%s', (root_id,))
        finally:
            cur.close()
            conn.close()

    def save_to_db(self, tree, cur):
        if tree.left_tree != None:
            left_tree_id = self.save_to_db(tree.left_tree, cur)
        if tree.right_tree != None:
            right_tree_id = self.save_to_db(tree.right_tree, cur)
        try:
            cur.execute('''insert into tree(node,left_tree,right_tree,regex) 
                          values(%s,%s,%s,%s)''', (tree.node,
                                                   left_tree_id if 'left_tree_id' in dir() else None,
                                                   right_tree_id if 'right_tree_id' in dir() else None,
                                                   tree.regex if hasattr(tree, 'regex') else None))
            cur.execute('select LAST_INSERT_ID()')
            return cur.fetchone()[0]
        except MySQLdb.Error as e:
            print('在将第%s层第%s位的子树(%s)存储进数据库时发生错误:%s'
                  % (tree.layer, tree.position, tree.node, e))
            # TODO:如果异常发生，是否需要回滚已存储的数据
            print('此次存储将撤销，数据将回滚')
            cur.execute('rollback')
            raise RollBackException

    @staticmethod
    def verification(username, password):
        try:
            # conn = MySQLdb.connect(host='139,199,228.34',user=environ.get('mysql_username'),passwd=environ.get('mysql_password'),db='dfa')
            conn = MySQLdb.connect(host='139.199.228.34', user=environ.get('mysql_username'),
                                   passwd=environ.get('mysql_password'), db='dfa')
            cur = conn.cursor()
            cur.execute('select * from user where username=%s and password=%s', (username, password))
            result = cur.fetchone()
            if result == None:
                print('账号密码错误，登陆失败')
                return False
            print('登陆成功')
            return User(username, result[3], result[0])
        except MySQLdb.Error as e:
            print("发生了一些错误：", e)
            print("请重新登录")
            return False
        finally:
            cur.close()
            conn.close()


if __name__ == '__main__':
    hyb = User.verification('hyb', 'hyb')
    tree = hyb.build_a_binary_tree()
    # hyb.display_all_concurrent_node(tree)
    # hyb.enter_regular_exp()
    # hyb.save(tree)
    tree.show()
