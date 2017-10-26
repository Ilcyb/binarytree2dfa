class Stack:

    def __init__(self):
        self._list_ = list()

    def is_empty(self):
        return len(self._list_) == 0

    def size(self):
        return len(self._list_)

    def have(self, element):
        return element in self._list_

    def push(self, element):
        self._list_.append(element)

    def pop(self):
        return self._list_.pop()

    def top(self):
        return self._list_[len(self._list_) - 1]

    def nums_of_element(self, element):
        count = int()
        for i in self._list_:
            if i == element:
                count += 1
        return count

    def pop_all(self):
        result = str()
        while True:
            result = self.pop() + result
            if self.is_empty():
                break
        return result

    # 有错误
    def pop_until(self, element):
        if self.have(element):
            while True:
                if self.pop() == element:
                    break
        else:
            raise ValueError('栈中没有此元素:', element)

    # 有错误
    def copy_until(self, element):
        if self.have(element):
            result = str()
            for e in self._list_.reverse():
                result += e
                if e == element:
                    break
        else:
            raise ValueError('栈中没有此元素:', element)

    def brackets(self, nums):
        result = str()
        for e in self._list_.reverse():
            result += e
            if e == ')':
                if nums == 0:
                    return result
                else:
                    nums -= 1
        if nums > 0:
            raise ValueError('栈中没有', nums, '个右括号')
