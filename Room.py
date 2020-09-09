from Suite import Suite


class Room:
    """
    房间类，包含 X 型房间和 Y 型房间。
    """

    def __init__(self, width: int, height: int, mode=False):
        self._width = width
        self._height = height
        self._control_points = []
        self._routines = []
        self._orders = []
        self._begin_end_mode = mode
        self._suite_x = Suite(self._width, self._height, self._begin_end_mode)
        self._suite_y = Suite(self._height, self._width, self._begin_end_mode)

    @property
    def orders(self):
        return self.orders

    @property
    def routines(self):
        return self._routines

    @property
    def control_points(self):
        return self._control_points

    @property
    def begin_end_mode(self):
        return self._begin_end_mode

    @begin_end_mode.setter
    def begin_end_mode(self, mode):
        self._begin_end_mode = mode

    @control_points.setter
    def control_points(self, control_points_list: list):
        """
        控制点应当为索引坐标，不是实际坐标。这里没有检查，但应该注意
        :param control_points_list: 控制点坐标列表
        :return:
        """
        self._control_points = list(control_points_list)

    def random(self):
        """
        随机生成一条路径
        :return: 输出随机生成的路径
        """
        # TODO X Y 型需不需要都考虑
        # 先确定是否为起终点模式
        self._suite_x.begin_end_mode = self.begin_end_mode
        # 将控制点坐标传给 X 房间
        self._suite_x.control_points = self.control_points
        return self._suite_x.random()

    def run(self):
        """
        开始运行
        :return:
        """
        self._suite_x.begin_end_mode = self.begin_end_mode
        self._suite_y.begin_end_mode = self.begin_end_mode
        # 将控制点坐标输给 X 房间
        self._suite_x.control_points = self.control_points
        # 进行计算，结果保存在 X 房间类中，还未提取
        self._suite_x.run()
        # 控制点转换并传递到 Y 房间
        self._suite_y.control_points = self._rotate_points(self.control_points)
        # 继续进行计算
        self._suite_y.run()
        # 提取计算结果，保存到 orders 和 routines 中
        self._merge()

    def _rotate_points(self, cp) -> list:
        """
        将 X 型控制点转换为 Y 型控制点坐标
        :return:
        """
        new_cp = list(cp)
        for i, (x, y) in enumerate(new_cp):
            new_cp[i] = (y, x)
        return new_cp

    def _merge(self):
        """
        将 X 型房间和 Y 型房间的结果合并，保存到自身中
        :return:
        """
        [self._orders.append(x) for x in self._suite_x.orders]
        [self._orders.append(x) for x in self._suite_y.orders]
        [self._routines.append(x) for x in self._suite_x.routines]
        for x in self._suite_y.routines:
            self._routines.append(self._rotate_points(x))

if __name__ == '__main__':
    r = Room(10, 10)
    r.control_points = [(3, 1), (4, 10), (3, 5), (4, 6), (6, 9), (5, 2)]
    r.run()
    # print(r.routines)