from user import User
from nfa import NFA
from binary_tree import BinaryTree
from DFA import my_output

if __name__ == '__main__':
    new_user = User()

    new_tree = BinaryTree('||')

    new_tree.insert_left('.')
    new_tree.insert_right('g')
    new_tree.left_tree.insert_left('*')
    new_tree.left_tree.insert_right('+')
    new_tree.left_tree.left_tree.insert_left('+')
    new_tree.left_tree.right_tree.insert_left('.')
    new_tree.left_tree.right_tree.insert_right('e')
    new_tree.left_tree.left_tree.left_tree.insert_left('k')
    new_tree.left_tree.left_tree.left_tree.insert_right('p')
    new_tree.left_tree.right_tree.left_tree.insert_left('a')
    new_tree.left_tree.right_tree.left_tree.insert_right('+')
    new_tree.left_tree.right_tree.left_tree.right_tree.insert_left('b')
    new_tree.left_tree.right_tree.left_tree.right_tree.insert_right('*')
    new_tree.left_tree.right_tree.left_tree.right_tree.right_tree.insert_right('f')

    # while True:
    #     new_tree = new_user.build_a_binary_tree()
    #     if new_tree:
    #         break
    concurrent_trees = list()
    concurrent_trees = new_tree.get_concurrent_node(concurrent_trees)
    if len(concurrent_trees) == 0:
        print("该二叉树没有并发结点，程序无法继续运行")
        exit()
    for tree_index in range(len(concurrent_trees)):
        print('\t\t', tree_index + 1)
        concurrent_trees[tree_index].show()
    while True:
        while True:
            try:
                tree_index = int(my_output("请选择要生成正则表达式的二叉树"))
            except ValueError:
                print("请输入正确的序号")
            else:
                if tree_index <= 0 or tree_index > len(concurrent_trees):
                    print("请输入正确的序号")
                else:
                    break
        choose_tree = concurrent_trees[tree_index - 1]
        while True:
            try:
                left_right = int(my_output("请选择由该树的左子树生成正则表达式还是从右子树生成正则表达式(左0右1): "))
            except ValueError:
                print("请输入正确的选择(左0右1)")
            else:
                if left_right != 0 and left_right != 1:
                    print("请输入正确的选择(左0右1)")
                else:
                    break
        generated_dfa_tree = choose_tree.left_tree if left_right == 0 else choose_tree.right_tree
        if generated_dfa_tree.get_concurrent_node(list()):
            print("所选择的子树中还有并发(||)子树，请重新选择")
        else:
            break
    generated_dfa_tree.show()
    regex = generated_dfa_tree.gen_regex('')
    print("该二叉树生成的正则表达式为", regex)
    change_regex_flag = my_output("是否需要修改正则表达式(Y/N)? ")
    if change_regex_flag == 'Y' or change_regex_flag == 'y':
        print("用户手动输入的正则表达式必须符合以下规则:",
              "1.若有|符号，必须放在括号中，如(a|b)",
              "2.若有*符号，则将要迭代的符号与*放在同一括号中，如(a*)", end='\n')
        regex = my_output("请输入要修改的正则表达式: ")
    generated_nfa = NFA(regex, dict())
    generated_nfa.parse()
    generated_dfa = generated_nfa.nfa2dfa()
    word = generated_dfa.loop()
    choose_tree.show()
    print("该树的%s子树生成的确定性自动机在输入字符串%s的情况下会进入陷阱状态，该树有错误"
          % ("左" if left_right == 0 else "右", word))
