class Order:
    """
    邮票序列类。
    """

    def __init__(self, arr: list, style='A'):
        if style == 'A':
            self._address = list(arr)
            self._folding = Order.convert(arr)
        elif style == 'O':
            self._folding = list(arr)
            self._address = Order.convert(arr)
        else:
            raise ValueError("Invalid style argument:%s" % style)
        self._is_fold = self.judger()

    @property
    def folding(self):
        return self._folding

    @property
    def address(self):
        return self._address

    @property
    def is_fold(self):
        return self._is_fold

    def __repr__(self):
        out_text = [str(x) for x in self.folding]
        out_text = ", ".join(out_text) + "\n"
        if self.is_fold:
            out_text += "可折叠"
        else:
            out_text += "不可折叠"
        return out_text

    def __len__(self):
        return len(self._folding)

    def __eq__(self, other):
        if other.folding == self.folding:
            return True
        return False

    @staticmethod
    def convert(arr):
        """
        生成折痕数组对应的地址数组
        """
        new_arr = list(arr)
        for i, _ in enumerate(arr):
            new_arr[arr[i]-1] = i + 1
        return new_arr

    def segment(self) -> 'tuple':
        """
        将地址分割为奇序列和偶序列，以方便验证是否可折，即检验其充要条件。
        e.g. input: [1, 2, 3, 4, 5, 6]
             output: [(1, 2), (3, 4), (5, 6)]
                     [(2, 3), (4, 5)]
             input: [1, 2]
             output: [(1, 2)]
                     []
        :return:
        """
        # 如果长度是奇数：
        if len(self) % 2 != 0:
            # 这里的切片设置需要对分割过程有一定的总结，最好在纸上推导一下。
            odd_list = [(x, y) for x, y in zip(self.address[:-2:2],
                                               self.address[1:-1:2])]
            even_list = [(x, y) for x, y in zip(self.address[1:-1:2],
                                                self.address[2::2])]
        else:
            odd_list = [(x, y) for x, y in zip(self.address[:-1:2],
                                               self.address[1::2])]
            even_list = [(x, y) for x, y in zip(self.address[1:-2:2],
                                                self.address[2:-1:2])]
        return odd_list, even_list

    def judger(self) -> bool:
        """
        检验整个Order是否为可折叠Order，即判断奇序列和偶序列是否满足条件
        :return:
        """
        odd_list, even_list = self.segment()
        return self.judge_list(odd_list) and self.judge_list(even_list)

    @staticmethod
    def judge_list(l: list) -> bool:
        """
        判断一个由数对组成的序列是否符合可折充要条件，如
        [(1, 2), (3, 4), (5, 6)]
        如果符合，则返回True；不符合，返回False
        :return:
        """
        for i, _ in enumerate(l):
            if not Order._judge_single_list(l[i:]):
                return False
        return True

    @staticmethod
    def _judge_single_list(l: list) -> bool:
        """
        判断一个序列的第一个tuple和剩余的tuple是否符合可折充要条件，
        :param l:
        :return:
        """
        if len(l) < 2:
            return True
        target = l[0]
        for x in l[1:]:
            if not Order._compare_tuple(target, x):
                return False
        return True

    @staticmethod
    def _compare_tuple(t1, t2: tuple) -> bool:
        """
        比较两对坐标，如果是可折对，则输出True;如果不可折，则输出False
        :return:
        """
        # 将需要比较的数字先排序，然后看它们来源于哪个tuple，根据逻辑值输出结果
        all_num = sorted(t1 + t2)
        # 排序后的数组为4个元素，只要保证第一个和第三个来自于不同的tuple即可
        # [1, 2, 7, 8] 中，1, 7 不可以是同一来源，即若t1 = (1, 7), t2 =
        # (2, 8)，则输出 False，表示不可折。
        try:
            return (all_num[0] in t1) ^ (all_num[2] in t1)
        except IndexError:
            return True

    def plus(self, key: 'function') -> 'List[Order]':
        """
        增加一折，返回所有可折的Order
        :return:
        """
        # 输出当前Order增加一折后的所有可折Order，存放在list output_orders中
        output_orders = []
        # 要插入的数字是当前长度加一
        insert_num = len(self) + 1
        new_address = self.address.copy()
        # 插入数字
        new_address.insert(0, insert_num)
        new_order = Order(new_address)
        if new_order.is_fold and key(new_address):
            output_orders.append(new_order)
        # 用交换来表示插入，所有都做一次判断
        for i, _ in enumerate(new_address[:-1]):
            new_address[i], new_address[i+1] = new_address[i+1], new_address[i]
            new_order = Order(new_address)
            if new_order.is_fold and key(new_address):
                output_orders.append(new_order)
        return output_orders