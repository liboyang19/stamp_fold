from Suite import Suite
import random


class Room:
    """
    房间类，包含 X 型房间和 Y 型房间。
    """

    def __init__(self, width: int, height: int, mode=False, suite_type='X/Y mode'):
        self._width = width
        self._height = height
        self._control_points = []
        self._routines = []
        self._orders = []
        self._suite_type = suite_type
        self._begin_end_mode = mode
        self._suite_x = Suite(self._width, self._height, self._begin_end_mode)
        self._suite_y = Suite(self._height, self._width, self._begin_end_mode)
        self._random_routine = []
        self._random_order = []

    @property
    def random_routine(self):
        return self._random_routine

    @property
    def random_order(self):
        return self._random_order

    @property
    def suite_type(self):
        return self._suite_type

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

    @suite_type.setter
    def suite_type(self, suite_type):
        self._suite_type = suite_type

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
        运行random按钮
        :return:
        """
        self._pre_run()
        if self.suite_type == 'X mode':
            # 进行计算，结果保存在 X 房间类中，还未提取
            self._suite_x.random()
        elif self.suite_type == 'Y mode':
            # 进行计算，结果保存在 Y 房间类中，还未提取
            self._suite_y.random()
        elif self.suite_type == 'X/Y mode':
            self._suite_x.random()
            self._suite_y.random()
        else:
            raise ValueError("房间类型参数错误: %s" % self.suite_type)
        temp_routine = self._suite_x.random_routine + self._suite_y.random_routine
        temp_order = self._suite_x.random_order + self._suite_y.random_order
        try:
            temp_result = random.choice(list(zip(temp_routine, temp_order)))
        except IndexError:
            return
        self._random_routine = list(temp_result[0])
        self._random_order.append(temp_result[1])

    def _pre_run(self):
        self._suite_x.begin_end_mode = self.begin_end_mode
        self._suite_y.begin_end_mode = self.begin_end_mode
        # 将控制点坐标输给 X 房间
        self._suite_x.control_points = self.control_points
        # 控制点转换并传递到 Y 房间
        self._suite_y.control_points = self._rotate_points(self.control_points)

    def run(self):
        """
        开始运行
        :return:
        """
        self._pre_run()
        if self.suite_type == 'X mode':
            # 进行计算，结果保存在 X 房间类中，还未提取
            self._suite_x.run()
        elif self.suite_type == 'Y mode':
            # 进行计算，结果保存在 Y 房间类中，还未提取
            self._suite_y.run()
        elif self.suite_type == 'X/Y mode':
            self._suite_x.run()
            self._suite_y.run()
        else:
            raise ValueError("房间类型参数错误: %s" % self.suite_type)
        # 提取计算结果，保存到 orders 和 routines 中
        self._merge()

    @staticmethod
    def _rotate_points(cp) -> list:
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
    r = Room(5, 5)
    r.control_points = []
    for i in range(10):
        r.random()
        print(r.random_routine)