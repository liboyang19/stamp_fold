class Stamp:
    """
    邮票类。解决折叠问题，规定折叠方向为横向右。
    """

    def __init__(self, n: int):
        self._n = n

    @property
    def n(self):
        return self._n

    def folding_to_address(self, folding: list):
        """
        生成折横数组对应的地址数组
        :param folding:
        :return:
        """
        addr = list(folding)
        for i, _ in enumerate(folding):
            addr[folding[i]-1] = i + 1
        return addr

    def is_fold(self):
        """
        是否可折
        :return:
        """
        pass

    def all_folding(self):
        """
        输出所有可折的排列
        :return:
        """

        pass

    def show(self):
        return self.folding_to_address([7, 2, 3, 6, 4, 5, 1])
