class Order:
    """
    邮票序列类。
    """

    def __init__(self, folding: list):
        self._folding = list(folding)
        self._address = self.folding_to_address()
        self._n = len(self._folding)
        self._odd_list = []
        self._even_list = []

    @property
    def folding(self):
        return self._folding

    @property
    def address(self):
        return self._address

    @property
    def n(self):
        return self.n

    #TODO: 还需要进一步调整
    def folding_to_address(self):
        """
        生成折痕数组对应的地址数组
        """
        addr = list(self.folding)
        for i, _ in enumerate(self.folding):
            addr[self.folding[i]-1] = i + 1
        return addr

    def segment(self, addr: list):
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
        if len(addr) % 2 != 0:
            # 这里的切片设置需要对分割过程有一定的总结，最好在纸上推导一下。
            odd_list = [(x, y) for x, y in zip(addr[:-2:2], addr[1:-1:2])]
            even_list = [(x, y) for x, y in zip(addr[1:-1:2], addr[2::2])]
        else:
            odd_list = [(x, y) for x, y in zip(addr[:-1:2], addr[1::2])]
            even_list = [(x, y) for x, y in zip(addr[1:-2:2], addr[2:-1:2])]

    def judge_list(self):

    def compare_tuple(self):
        """
        比较两对坐标
        :return:
        """
        pass

    def add_one(self):
