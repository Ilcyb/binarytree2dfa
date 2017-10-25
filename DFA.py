class DFA:
    
    # DFA初始化来源：默认为0，用文件初始化，为1时用dfa的各属性初始化
    def __init__(self, states, alphabet, functions, start_state, accept_state, source=0):
        if source == 0:
        # 将状态文件中的状态集合读取至self.states中，状态文件中每个状态占一行
            self.states = list()
            with open(states, 'r') as f:
                for line in f:
                    self.states.append(line.rstrip())
            # 将符号表文件中的符号读取至self.alphabet中，符号表文件中每个符号占一行
            self.alphabet = list()
            with open(alphabet, 'r') as f:
                for line in f:
                    self.alphabet.append(line.rstrip())
            # 将状态转移文件中的状态转移函数读取至self.functions中，状态转移文件中每个函数占一行 如：(s1,w)=s2 s1状态接收w符号转移至s2状态
            self.functions = dict()
            with open(functions,'r') as f:
                for line in f:
                    flist = line.split('=')
                    key = (flist[0].split(',')[0][1:],flist[0].split(',')[1][:-1])   
                    self.functions[key] = flist[1].rstrip() #字典 key:(状态，符号) value:转移后的状态
            # 读取初始状态
            with open(start_state, 'r') as f:
                this_state = f.read().rstrip()
                if this_state not in self.states:
                    raise ValueError('状态集合中不包括初始状态，自动机初始化失败')
                self.start_state = this_state
            # 读取接受状态
            self.accept_state = list()
            with open(accept_state, 'r') as f:
                for line in f:
                    if line.rstrip() not in self.states:
                        raise ValueError('接受状态中有不属于状态合集中的状态，自动机初始化失败')                    
                    self.accept_state.append(line.rstrip())
        elif source == 1:
            self.states = states
            self.alphabet = alphabet
            self.functions = functions
            self.start_state = start_state
            self.accept_state = accept_state

        print('自动机已读取成功')
        self.display()

    def loop(self):
        while True:
            print('请输入字符串(i to insert)')
            word = input('>>> ')
            if word == 'i':
                while not self.insert_2():
                    pass
                print('自动机重新生成')
            else:
                self.parse(word)
    
    def parse(self, word):
        now_state = self.start_state
        alpha_list = list(word)
        if not set(alpha_list).issubset(set(self.alphabet)):
            print('字符串中有不属于符号表的字符,请重新输入')
            return 0
        for c in alpha_list:
            now_state = self.functions[now_state, c] if (now_state, c) in self.functions else now_state
        if now_state in self.accept_state:
            print('字符串' + word + '被状态' + now_state + '接受')
        else:
            print('字符串' + word + '没有被自动机接受，最终停在状态' + now_state)

    #插入结点有
    #1.一个结点引出另一个结点，互相转移条件围成环
    #2.在两个结点中插入结点
    #3.不插入结点，但在某结点上添加自转移条件
    #4.不插入结点，在两结点之间增加转移条件
    # def insert(self):
    #     front = my_output('请输入要插入结点的前驱结点(若没有，则键入回车)')
    #     if front != '':
    #         front_state_l = my_output('请输入前驱结点状态转移至要插入的结点状态所需要的条件(若没有，则键入回车)')
    #         front_state_r = my_output('请输入要插入的结点状态转移至前驱结点状态所需要的条件(若没有，则键入回车)')
    #     behind = my_output('请输入要插入结点的后继结点(若没有，则键入回车)')
    #     if behind != '':
    #         behind_state_r = my_output('请输入要插入结点状态转移至后继结点状态所需要的条件(若没有，则键入回车)')
    #         behind_state_l = my_output('请输入后继结点状态转移至要插入结点状态所需要的条件(若没有，则键入回车)')
    #     inserted = my_output('请输入要插入的结点状态(若没有则键入回车)')
    #     # 情况1 还有其他的输入能产生情况1
    #     if front == behind and inserted != '' and front != inserted and front != '':
    #         self.insert_cases(case_flag=1, front_state_l=front_state_l, behind_state_r=behind_state_r,
    #                          front=front, inserted=inserted)
    #     # 情况2
    #     elif front != behind and inserted != '' and front != inserted 
    #         and behind != inserted and front != '' and behind != '':
    #         self.insert_cases(case_flag=2, front=front, behind=behind, 
    #                             front_state_l=front_state_l, front_state_r=front_state_r,
    #                             behind_state_l=behind_state_l, behind_state_r=behind_state_r, inserted=inserted)
    #     # 情况3 输入：front和behind输入要添加自转移条件的结点，front_state_l输入自转移条件
    #     elif front == behind and inserted == '' and front != ':
    #         self.insert_cases(case_flag=3, front=front, front_state_l=front_state_l, inserted=inserted)
    #     # 情况4 输入：front和behind输入转移条件的两边，
    #     # front_state_l输入front到behind的转移条件,behind_state_r输入behind到front的转移条件
    #     elif front != behind and inserted == '' and front != '' and behind != '':
    #         self.insert_cases(case_flag=4, front=front, front_state_l=front_state_l,
    #          behind=behind, behind_state_r=behind_state_r, inserted=inserted)

    def insert_2(self):
        print('选择插入类型：',
                '1.在原有结点上向外延伸一个新的结点',
                '2.在原有的两个结点之间插入新的结点',
                '3.不插入新的结点，而是在原有的结点上增加自转移条件',
                '4.不插入新的结点，而是在原有的结点之间增加转移条件', sep='\n')
        case = input('>>> ')
        try:
            case = int(case)
            if case == 1:
                older = my_output('请输入原有结点')
                inserted = my_output('请输入要插入的结点')
                oti = my_output('请输入原有结点转移至新结点的条件(若没有则键入回车)')
                ito = my_output('请输入新结点转移至原有结点的条件(若没有则键入回车)')
                if older not in self.states:
                    print('你输入的原有结点不存在，插入失败')
                    return False
                if inserted in self.states:
                    print('你输入的新插入结点已存在，插入失败')
                    return False
                if oti == '' and ito == '':
                    print('原结点和新插入结点之间至少要有一条状态转移路线，插入失败')
                    return False
                self.states.append(inserted)
                if oti != '':
                    if oti not in self.alphabet:
                        self.alphabet.append(oti)
                    self.functions[(older, oti)] = inserted
                if ito != '':
                    if ito not in self.alphabet:
                        self.alphabet.append(ito)
                    self.functions[(inserted, ito)] = older
                is_accept = my_output('要插入的该结点是否为接受状态？(y/any key except y)')
                if is_accept == 'y':
                    self.accept_state.append(inserted)
                print('成功插入新状态结点',inserted)
                return True
            elif case == 2:
                older_1 = my_output('请输入原有结点1')
                older_2 = my_output('请输入原有结点2')
                inserted = my_output('请输入要插入的结点')
                o1ti = my_output('请输入结点1转移至新结点的条件(若没有则键入回车)')
                ito1 = my_output('请输入新结点转移至结点1的条件(若没有则键入回车)')
                o2ti = my_output('请输入结点2转移至新结点的条件(若没有则键入回车)')
                ito2 = my_output('请输入新结点转移至结点2的条件(若没有则键入回车)')
                if older_1 not in self.states or older_2 not in self.states:
                    print('你输入的原有结点不存在，插入失败')
                    return False
                if inserted in self.states:
                    print('你输入的新插入结点已存在，插入失败')
                    return False
                if o1ti == '' and ito1 == '' or o2ti == '' and ito2 == '':
                    print('两个原结点和新结点之间都至少要有一条状态转移路线，插入失败')
                    return False
                self.states.append(inserted)
                if o1ti != '':
                    if o1ti not in self.alphabet:
                        self.alphabet.append(o1ti)
                    self.functions[(older_1, o1ti)] = inserted
                if ito1 != '':
                    if ito1 not in self.alphabet:
                        self.alphabet.append(ito1)
                    self.functions[(inserted, ito1)] = older_1
                if o2ti != '':
                    if o2ti not in self.alphabet:
                        self.alphabet.append(o2ti)
                    self.functions[(older_2, o2ti)] = inserted
                if ito2 != '':
                    if ito2 not in self.alphabet:
                        self.alphabet.append(ito2)
                    self.functions[(inserted, ito2)] = older_2
                is_accept = my_output('要插入的该结点是否为接受状态？(y/any key except y)')
                if is_accept == 'y':
                    self.accept_state.append(inserted)
                print('成功插入新状态结点',inserted)
                return True
            elif case == 3:
                inserted = my_output('请输入要增加自转移条件的结点')
                condition = my_output('请输入要增加的自转移条件')
                if inserted == '':
                    print('结点为空，插入失败')
                    return False
                if condition == '':
                    print('自转移条件为空，插入失败')
                    return False
                if inserted not in self.states:
                    print('要添加自转移条件的结点不存在，插入失败')
                    return False
                if condition not in self.alphabet:
                    self.alphabet.append(condition)
                self.functions[(inserted, condition)] = inserted
                print('成功为状态' + inserted + '添加自转移条件' + condition)
                return True
            elif case == 4:
                state_1 = my_output('请输入要添加转移条件的结点1')
                state_2 = my_output('请输入要添加转移条件的结点2')
                condition_1t2 = my_output('请输入结点1转移至结点2的条件(若没有则键入回车)')
                condition_2t1 = my_output('请输入结点2转移至结点1的条件(若没有则键入回车)')
                if state_1 == '' or state_2 == '':
                    print('节点为空，插入失败')
                    return False
                if state_1 not in self.states or state_2 not in self.states:
                    print('结点不存在，插入失败')
                    return False
                if condition_1t2 == '' and condition_2t1 == '':
                    print('两个结点间至少要添加一个转移条件，插入失败')
                    return False
                if condition_1t2 != '' and condition_1t2 not in self.alphabet:
                    self.alphabet.append(condition_1t2)
                if condition_2t1 != '' and condition_2t1 not in self.alphabet:
                    self.alphabet.append(condition_2t1)
                self.functions[(state_1, condition_1t2)] = state_2
                self.functions[(state_2, condition_2t1)] = state_1
                print('成功在状态' + state_1 + '与' + state_2 + '之间插入转移状态')
                return True
            else:
                print('请选择正确的选项')
        except ValueError:
            print('请选择正确的选项')        

    # def insert_cases(self, case_flag, front=None, front_state_l=None, front_state_r=None,
    #                  behind=None, behind_state_l=None, behind_state_r=None, inserted=None):
    #     if case_flag == 1:
    #         if inserted in self.states:
    #             print('要插入的该结点已存在')
    #             return False
    #         is_accept = my_output('要插入的该结点是否为接受状态？(y/any key except y)')
    #         if is_accept == 'y':
    #             self.accept_state.append(inserted)
    #         self.functions[(inserted, behind_state_r)] = front
    #         self.functions[(front, front_state_l)] = inserted
    #         self.states.append(inserted)
    #     if case_flag == 2:
    #         if inserted in self.states:
    #             print('要插入的该结点已存在')
    #             return False
    #         is_accept = my_output('要插入的该结点是否为接受状态？(y/any key except y)')
    #         if is_accept == 'y':
    #             self.accept_state.append(inserted)
            

    def display(self):
        print('states:', self.states)
        print('alphabet:', self.alphabet)
        print('functions:', self.functions)
        print('start state:', self.start_state)
        print('accept states:', self.accept_state)

    
def my_output(content):
    print(content)
    temp = input('>>> ')
    return temp        

if __name__ == '__main__':
    d1 = DFA(r'C:\Ddisk\py\DFA\test1\states.txt',
            r'C:\Ddisk\py\DFA\test1\alphabet.txt',
            r'C:\Ddisk\py\DFA\test1\functions.txt',
            r'C:\Ddisk\py\DFA\test1\start_state.txt',
            r'C:\Ddisk\py\DFA\test1\accept_states.txt')
    d1.loop()