from stack import Stack
from DFA import DFA


class NFA:
    @staticmethod
    def insert_into_dict(key, functions, count):
        if key in functions:
            functions[key].append(count)
        else:
            functions[key] = list((count,))

    def __init__(self, expression, functions, father=None, edge=list()):
        self._name_ = 'N(' + expression + ')'
        self._expression_ = expression
        self._stack_ = Stack()
        self.functions = functions
        self.father = father
        self.is_iteration_flag = False
        self.edge = edge
        self.states = list()

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
            self.edge.append(self._expression_)
            self.final = count
            return count
        # 当表达式是迭代时的处理
        if self._expression_[-1:] == '*':
            key = (count, 'ε')
            count += 1
            NFA.insert_into_dict(key, self.functions, count)
            self.is_iteration_flag = True
            self._expression_ = self._expression_[:-1]  # 去掉*

        for c in range(len(self._expression_)):
            current_char = self._expression_[c]
            if not self._stack_.have('(') and current_char != '(':
                if current_char == '*':
                    pass
                # 当表达式含有选择时的处理
                elif current_char == '|':
                    left_expression = self._expression_[:c]
                    right_expression = self._expression_[c + 1:]
                    left_n = NFA(left_expression,
                                 self.functions, self, self.edge)
                    count = left_n.parse(count + 1)
                    right_n = NFA(right_expression,
                                  self.functions, self, self.edge)
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
                        n1 = NFA(current_char, self.functions, self, self.edge)
                        count = n1.parse(count)
            else:
                if current_char == ')' and self._stack_.nums_of_element('(') - self._stack_.nums_of_element(')') == 1:
                    expr = self._stack_.pop_all()[1:]  # 去掉这层括号
                    if not pass_flag:
                        n2 = NFA(expr, self.functions, self, self.edge)
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

    def generate_state_list(self):
        return [i for i in range(self.begin, self.final + 1)]

    def remove_duplicates_edge(self):
        return set(self.edge)

    def get_result(self):
        return self.functions

    def nfa2dfa(self):
        pending_list = list()  # 待处理列表
        processed_list = list()  # 已处理列表
        pending_list.append(list(self.closure([self.begin])))
        dfa_list_functions = dict()
        dfa_functions = dict()
        while pending_list:
            p = pending_list[0]
            for e in self.remove_duplicates_edge():
                temp = list(self.closure(list(self.move(p, e))))
                if len(temp) != 0:
                    key = (tuple(p), e)
                    dfa_list_functions[key] = temp
                if (temp not in pending_list) and (temp not in processed_list) and (len(temp) != 0):
                    pending_list.append(temp)
            processed_list.append(p)
            pending_list.remove(p)
        count = 0
        begin_list = list()
        final_list = list()
        begin_state = None
        final_state = list()
        list_count_map = dict()
        states = list()
        for p in processed_list:
            if self.begin in p:
                begin_list = tuple(p)
                begin_state = count
                list_count_map[begin_list] = begin_state
                states.append(begin_state)
            elif self.final in p:
                final_list = tuple(p)
                final_state.append(count)
                list_count_map[final_list] = count
                states.append(count)
            else:
                list_count_map[tuple(p)] = count
                states.append(count)
            count += 1
        for k, v in dfa_list_functions.items():
            key = (list_count_map[k[0]], k[1])
            dfa_functions[key] = list_count_map[tuple(v)]
        the_dfa = DFA(states, self.remove_duplicates_edge(),
                      dfa_functions, [begin_state], final_state, 1)
        return the_dfa

    # states中的状态通过edge边可以到达的状态
    def move(self, states, edge):
        result = list()
        for state in states:
            if (state, edge) in self.functions:
                result.extend(self.functions[(state, edge)])
        return set(result)

    # states中的状态通过任意个‘ε’可以到达的状态
    def closure(self, states):
        result = list()
        result.extend(states)
        for state in result:
            if (state, 'ε') in self.functions:
                temp_list = self.functions[(state, 'ε')]
                result.extend([i for i in temp_list if i not in result])
        return set(result)


if __name__ == '__main__':
    result = dict()
    n = NFA('((a|b)|(c*))abb(e|f)(k*)', result)
    n.parse()
    result = n.get_result()
    print(result)
    the_dfa = n.nfa2dfa()
