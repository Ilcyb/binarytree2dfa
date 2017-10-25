from stack import Stack

class NFA:

    @staticmethod
    def insert_into_dict(key, functions, count):
        if key in functions:
            functions[key].append(count)
        else:
            functions[key] = list((count,))

    def __init__(self, expression, functions, father):
        self._name_ = 'N(' + expression + ')'
        self._expression_ = expression
        self._stack_ = Stack()
        self.functions = functions
        self.father = father
        self.is_iteration_flag = False

    # 判断表达式中是否存在一个不在括号中的 '|'
    def have_independent_choose(self):
        temp_stack = Stack()
        for c in range(len(self._expression_)):
            current_char = self._expression_[c]
            if current_char == '|' and temp_stack.is_empty():
                return True
            elif current_char == '(':
                temp_stack.push(c)
            elif current_char == ')':
                temp_stack.pop()
        return False

    def parse(self, count=0):
        self.begin = count
        pass_flag = self.have_independent_choose()
        # 当表达式是单字符串时的处理
        if len(self._expression_) == 1:
            key = (count, self._expression_)
            count += 1
            NFA.insert_into_dict(key, self.functions, count)
            self.final = count
            return count
        # 当表达式是迭代时的处理
        if self._expression_[-1:] == '*':
            key = (count, 'ε')
            count += 1
            NFA.insert_into_dict(key, self.functions, count)
            self.is_iteration_flag = True
            self._expression_ = self._expression_[:-1] # 去掉*
        
        for c in range(len(self._expression_)):
            current_char = self._expression_[c]
            if not self._stack_.have('(') and current_char != '(':
                if  current_char == '*':
                    pass
                # 当表达式含有选择时的处理
                elif current_char == '|':
                    left_expression = self._expression_[:c]
                    right_expression = self._expression_[c+1:]
                    left_n = NFA(left_expression, self.functions, self)
                    count = left_n.parse(count + 1)
                    right_n = NFA(right_expression, self.functions, self)
                    count = right_n.parse(count + 1)
                    key = (self.begin, 'ε')
                    NFA.insert_into_dict(key, self.functions, left_n.begin)
                    key = (self.begin, 'ε')
                    NFA.insert_into_dict(key, self.functions, right_n.begin)
                    count += 1
                    key = (left_n.final, 'ε')
                    NFA.insert_into_dict(key, self.functions, count)
                    key = (right_n.final, 'ε')
                    NFA.insert_into_dict(key, self.functions, count)
                else:
                    if not pass_flag:
                        n1 = NFA(current_char, self.functions, self)
                        count = n1.parse(count)
            else:
                if current_char == ')' and self._stack_.nums_of_element('(') - self._stack_.nums_of_element(')') == 1:
                    expr = self._stack_.pop_all()[1:] # 去掉这层括号
                    if not pass_flag:
                        n2 = NFA(expr, self.functions, self)
                        count = n2.parse(count)
                else:
                    self._stack_.push(current_char)
        if self.is_iteration_flag:
            key = (count, 'ε')
            NFA.insert_into_dict(key, self.functions, self.begin + 1)
            key = (count, 'ε')
            count += 1
            NFA.insert_into_dict(key, self.functions, count)
            key = (self.begin, 'ε')
            NFA.insert_into_dict(key, self.functions, count)
        self.final = count
        return count

    def get_result(self):
        return self.functions
        

if __name__ == '__main__':
    result = dict()
    n = NFA('((a|b)|(c*))',result,None)
    n.parse()
    result = n.get_result()
    print(result)
