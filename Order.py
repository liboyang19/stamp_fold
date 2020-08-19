class Order:
    """
    邮票序列类。
    """

    def __init__(self, folding: list):
        self._folding = list(folding)
        self._address = self.folding_to_address()
        self._n = len(self._folding)
        self._is_fold = self._judger()

    @property
    def folding(self):
        return self._folding

    @property
    def address(self):
        return self._address

    @property
    def n(self):
        return self._n

    @property
    def is_fold(self):
        return self._is_fold

    def __len__(self):
        return self.n

    # TODO: 还需要进一步调整
    def folding_to_address(self):
        """
        生成折痕数组对应的地址数组
        """
        addr = list(self.folding)
        for i, _ in enumerate(self.folding):
            addr[self.folding[i]-1] = i + 1
        return addr

    def _judger(self) -> bool:
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
        if self.n % 2 != 0:
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
        return self._judge_list(odd_list) and self._judge_list(even_list)

    def _judge_list(self, l: list) -> bool:
        """
        判断一个由数对组成的序列是否符合可折充要条件，如
        [(1, 2), (3, 4), (5, 6)]
        如果符合，则返回True；不符合，返回False
        :return:
        """
        for i, _ in enumerate(l):
            if not self._judge_single_list(l[i:]):
                return False
        return True

    def _judge_single_list(self, l: list) -> bool:
        """
        判断一个序列的第一个tuple和剩余的tuple是否符合可折充要条件，
        :param l:
        :return:
        """
        if len(l) < 2:
            return True
        target = l[0]
        for x in l[1:]:
            if not self._compare_tuple(target, x):
                return False
        return True

    def _compare_tuple(self, t1, t2: tuple) -> bool:
        """
        比较两对坐标，如果是可折对，则输出True;如果不可折，则输出False
        :return:
        """
        # 将需要比较的数字先排序，然后看它们来源于哪个tuple，根据逻辑值输出结果
        all_num = sorted(t1 + t2)
        # 排序后的数组为4个元素，只要保证第一个和第三个来自于不同的tuple即可
        # [1, 2, 7, 8] 中，1, 7 不可以是同一来源，即若t1 = (1, 7), t2 =
        # (2, 8)，则输出 False，表示不可折。
        # TODO 小心IndexError
        try:
            return (all_num[0] in t1) ^ (all_num[2] in t1)
        except IndexError:
            return True

    def plus(self) -> 'Order':
        """
        增加一折，返回所有可折的Order
        :return:
        """
        pass
