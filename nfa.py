from stack import Stack

class NFA:

    def __init__(self, expression, functions, father):
        self._name_ = 'N(' + expression + ')'
        self._expression_ = expression
        self._stack_ = Stack()
        self.functions = functions
        self.father = father
        self.is_iteration_flag = False

    def parse(self, count=0):
        self.begin = count
        if len(self._expression_) == 1:
            key = (count, self._expression_)
            count += 1
            self.functions[key] = count
            self.final = count
            return count
        if self._expression_[-1:] == '*':
            key = (count, 'ε')
            count += 1
            self.functions[key] = count
            self.is_iteration_flag = True
            self._expression_ = self._expression_[:-1] # 去掉*
        for c in self._expression_:
            if not self._stack_.have('(') and c != '(':
                key = (count, c)
                count += 1
                self.functions[key] = count
            else:
                if c == ')' and self._stack_.nums_of_element('(') - self._stack_.nums_of_element(')') == 1:
                    expr = self._stack_.pop_all()[1:]
                    n2 = NFA(expr, self.functions, self)
                    count = n2.parse(count)
                else:
                    self._stack_.push(c)
        if self.is_iteration_flag:
            key = (count, 'ε')
            self.functions[key] = self.begin + 1
            key = (count, 'ε')
            count += 1
            self.functions[key] = count
            key = (self.begin, 'ε')
            self.functions[key] = count
        self.final = count
        return count
        