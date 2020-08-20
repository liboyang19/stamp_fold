import Suite


class Room:
    """
    房间类，包含 X 型房间和 Y 型房间。
    """

    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height
        self._control_points = []
        self._routines = []
        self._orders = []
        self._suite_x = Suite(self._width, self._height)
        self._suite_y = Suite(self._height, self._width)

    @property
    def orders(self):
        return self.orders

    @property
    def routines(self):
        return self._routines

    @property
    def control_points(self):
        return self._control_points

    @control_points.setter
    def control_points(self, control_points_list: list):
        """
        控制点应当为索引坐标，不是实际坐标。这里没有检查，但应该注意
        :param control_points_list: 控制点坐标列表
        :return:
        """
        self._control_points = list(control_points_list)

    def run(self):
        """
        开始运行
        :return:
        """
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
        for i, (x, y) in new_cp:
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
