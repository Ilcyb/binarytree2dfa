from stack import Stack

class NFA:

    def __init__(self):
        self.regexs = Stack()

    def split_regex(self, regex):
        

    def regex2nfa(self, regex):
        temp = Stack()
        for c in regex[::-1]:
            if c == '(':
                self.regexs.push(temp.brackets(temp.nums_of_element(')') - 1))       
