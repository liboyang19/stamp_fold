from collections import deque
import numpy as np
from Order import Order


class Suite:
    """
    房间类。
    """

    def __init__(self, width: int, height: int):
        if not (isinstance(width, int) and isinstance(height, int)):
            raise TypeError("The width and height of room must be integers.")
        if width < 3 or height < 3:
            raise RuntimeWarning("Warning: size of (%d,%d) maybe too small. "
                                 "Unexpected result may occur." % (width, height))
        self._width = width
        self._height = height
        self._control_points = []
        self._init_orders = deque()
        self._routines = []
        self._orders = []
        self._control_points_rank = []

    @property
    def control_points(self):
        return self._control_points

    @property
    def orders(self):
        return self._orders

    @property
    def routines(self):
        return self._routines

    def _get_routine(self, order):
        """
        获取 X 型右折和左折路径
        :return: (右折路径, 左折路径)
        """
        odd_list, even_list = order.segment()
        # 添加起点
        even_list.insert(0, (order.address[0], order.address[0]))
        # 添加终点
        if len(order) % 2 == 0:
            even_list.append((order.address[-1], order.address[-1]))
        else:
            odd_list.append((order.address[-1], order.address[-1]))
        # 计算奇偶对的厚度
        odd_counter = self._get_thick(odd_list)
        even_counter = self._get_thick(even_list)
        # 判断厚度是否大于宽度，如果大于，则无法画出，即时返回 None
        if np.max(odd_counter) + np.max(even_counter) > self._width:
            return None, None
        odd_x = self._width - odd_counter
        even_x = even_counter + 1
        len_axis = len(odd_x) + len(even_x)
        routine_x = np.zeros(len_axis, dtype=int)
        # 把奇数横坐标放到偶数Index上，偶数横坐标放到奇数Index上
        routine_x[1::2] = odd_x
        routine_x[::2] = even_x
        # 然后处理纵坐标，方法同上，只不过用的是list，但注意，横坐标每次要考虑两个值，
        # 即 x = 3, y = (4, 7) -> (3, 4), (3, 7)
        routine_y = [0 for i in range(len_axis)]
        # 同样，奇偶序列安排
        routine_y[1::2] = odd_list
        routine_y[::2] = even_list
        # 生成最后的坐标序列
        right_routine = []
        for x, (y1, y2) in zip(routine_x, routine_y):
            right_routine.append((x, y1))
            right_routine.append((x, y2))
        left_routine = self._mirror(right_routine)
        return right_routine, left_routine

    def _get_thick(self, tuple_list):
        counter = np.zeros(len(tuple_list), dtype=int)
        for i, item in enumerate(tuple_list):
            for item_t in tuple_list:
                if self._is_within(item, item_t):
                    counter[i] += 1
        return counter

    @staticmethod
    def _is_within(t1, t2):
        """
        看t1是否在t2里面，如果在，则返回 True；否则返回 False
        即，若 t1 = (4, 2), t2 = (7, 1)，则返回 True
        :param t1:
        :param t2:
        :return:
        """
        st1 = sorted(t1)
        st2 = sorted(t2)
        return st1[1] < st2[1] and st1[0] > st2[0]

    @control_points.setter
    def control_points(self, control_points_list: list):
        """
        控制点应当为索引坐标，不是实际坐标。这里没有检查，但应该注意
        :param control_points_list: 控制点坐标列表
        :return:
        """
        self._control_points = list(control_points_list)

    def _mirror(self, coord):
        new_coord = list(coord)
        for i, (x, y) in enumerate(new_coord):
            new_coord[i] = (self._width - x + 1, y)
        return new_coord

    def run(self):
        """
        计算最终验证后的结果
        :return:
        """
        # 通过控制点坐标计算控制点顺序，用self._control_points_rank保存
        self._get_cp_rank()
        # 计算所有理论上的可折序列
        self._calc_init()
        # 过滤掉无法实现的路径
        self._filter()

    def _filter(self):
        """
        用self._kernel(过滤器)过滤掉所有不符合实际的路径，将合乎要求的存入类中。
        :return:
        """
        while self._init_orders:
            current_order = self._init_orders.pop()
            current_routine = self._get_routine(current_order)
            for cr in current_routine:
                if self._kernel(cr):
                    self._orders.append(current_order)
                    self._routines.append(cr)

    def _calc_init(self):
        """
        计算生成初始Orders，即满足地址要求的Orders，但未验证是否满足实际情况。
        会将计算结果保存在 self._init_orders 中
        :return:
        """
        # 先用长度为1的地址构建Order类，然后入队
        self._init_orders.append(Order([1]))
        front_order = self._init_orders.popleft()
        while len(front_order) < self._height:
            # print(front_order.address)
            [self._init_orders.append(x) for x in front_order.plus(key=self._key)]
            try:
                front_order = self._init_orders.popleft()
            except IndexError:
                return
        self._init_orders.append(front_order)

    def _key(self, addr_list: list) -> bool:
        """
        判断地址是否符合控制点要求，输出布尔值
        :param addr_list: 地址数组
        :return: bool
        """
        rank_index = []
        for item in addr_list:
            if item in self._control_points_rank:
                rank_index.append(self._control_points_rank.index(item))
        return sorted(rank_index) == rank_index

    def _get_cp_rank(self):
        """
        得到控制点的顺序数组，存入self._control_points_rank中。
        注意，这里所有的类型都视为 X 型
        :return:
        """
        for item in self._control_points:
            self._control_points_rank.append(item[1])

    def _kernel(self, routine):
        """
        验证现有的Order是否符合实际情况，即通过螺旋数组来判断经过点的先后顺序。
        :return:
        """
        # 要生成螺旋数组
        # 利用一个虚拟条带，模拟螺旋数组的生成过程
        ref_strip = np.arange(1, self._height * self._width + 1)
        stamp_matrix = np.zeros([self._height, self._width], dtype=int)
        i = 0
        for (start_x, start_y), (end_x, end_y) in zip(routine[:-1], routine[1:]):
            ref_c = (end_x - start_x, end_y - start_y)
            if ref_c[0] == 0:
                strip_len = ref_c[1]
                if strip_len > 0:
                    stamp_matrix[start_y - 1:end_y, start_x - 1] = ref_strip[i:i+strip_len+1]
                if strip_len < 0:
                    stamp_matrix[end_y - 1:start_y, start_x - 1] = ref_strip[i:i-strip_len+1][::-1]
            else:
                strip_len = ref_c[0]
                if strip_len > 0:
                    stamp_matrix[start_y - 1, start_x - 1:end_x] = ref_strip[i:i+strip_len+1]
                if strip_len < 0:
                    stamp_matrix[start_y - 1, end_x - 1:start_x] = ref_strip[i:i-strip_len+1][::-1]
            i += np.abs(strip_len)
        cp_row = [t[1] - 1 for t in self.control_points]
        cp_col = [t[0] - 1 for t in self.control_points]
        cp_ranks = stamp_matrix[cp_row, cp_col]
        return np.array_equal(cp_ranks, np.sort(cp_ranks))

    def clear(self):
        """
        清除所有控制点，但保留房间结构。
        :return:
        """
        self.__init__(self._width, self._height)

    def resize(self):
        """
        调整房间大小
        :return:
        """
        pass
