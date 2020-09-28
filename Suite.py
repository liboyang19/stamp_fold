from collections import deque
import numpy as np
from itertools import combinations
from Order import Order
import random


class Suite:
    """
    房间类。
    """

    def __init__(self, width: int, height: int, mode=False):
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
        self._begin_end_mode = mode
        self._random_flag = False
        self._random_routine = []
        self._random_order = []

    @property
    def begin_end_mode(self):
        return self._begin_end_mode

    @property
    def control_points(self):
        return self._control_points

    @property
    def orders(self):
        return self._orders

    @property
    def routines(self):
        return self._routines

    @property
    def random_routine(self):
        return self._random_routine

    @property
    def random_order(self):
        return self._random_order

    @begin_end_mode.setter
    def begin_end_mode(self, mode):
        self._begin_end_mode = mode

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
        # 注意这里需要加1，表示个数
        if np.max(odd_counter) + np.max(even_counter) + 1 > self._width:
            # 如果画不出，则返回两个空集
            return [], []
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
        self._create_init()
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

    def _kernel(self, routine) -> bool:
        """
        验证现有的Order是否符合实际情况，即通过螺旋数组来判断经过点的先后顺序。
        :return:
        """
        # 要生成螺旋数组
        # 利用一个虚拟条带，模拟螺旋数组的生成过程
        ref_strip = np.arange(1, self._height * self._width + 1)
        stamp_matrix = np.zeros([self._height, self._width], dtype=int)
        i = 0
        if not routine:
            return False
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
                    stamp_matrix[start_y - 1,start_x - 1:end_x] = ref_strip[i:i + strip_len + 1]
                if strip_len < 0:
                    stamp_matrix[start_y - 1, end_x - 1:start_x] = ref_strip[i:i-strip_len+1][::-1]
            i += np.abs(strip_len)
        cp_row = [t[1] - 1 for t in self.control_points]
        cp_col = [t[0] - 1 for t in self.control_points]
        cp_ranks = stamp_matrix[cp_row, cp_col]
        if self.begin_end_mode:
            if cp_ranks[0] != 1 or cp_ranks[-1] != len(ref_strip):
                return False
        return np.array_equal(cp_ranks, np.sort(cp_ranks))

    def _find_one_routine(self, arr: Order, rou: list) -> bool:
        """
        判断某个已经到了n折的排列是不是符合最后的实际要求，如果符合返回True并将路径存在rou中
        如果不符合返回False，并且不去修改rou中的值
        :param arr:
        :return:
        """
        temp_result = []
        right_r, left_r = self._get_routine(arr)
        if self._kernel(right_r):
            temp_result.append(right_r)
        if self._kernel(left_r):
            temp_result.append(left_r)
        if temp_result:
            rou.append(random.choice(temp_result))
            return True
        else:
            return False

    def random(self):
        """
        生成池子，即最初始的栈，为random递归做准备
        :return:
        """
        # 调用创建池子，获得初始的深度优先搜索的栈
        self._get_cp_rank()
        arr_pool, index_pool, insert_no = self._get_init_pool()
        # 将arr_pool和index_pool打包存在初始栈中
        init_stack = deque()
        # pop操作真的很快
        while arr_pool:
            init_stack.append((arr_pool.pop(), index_pool.pop()))
        result = []
        # 调用递归函数
        self._prepare_for_random(init_stack, insert_no, result)
        # 返回的result如果为空，则说明没找到结果
        for routine_result, order_result in result:
            self._random_routine = routine_result.copy()
            self._random_order.append(order_result)

    def _prepare_for_random(self, stack_space: list, insert_no: set, result: list):
        """
        递归函数，目的是为了寻找一条合适的路径就停下来，如果递归结束都没有找到，那就输出不存在
        注意：现在还没有考虑递归深度的问题
        stack_space:
        [(now_address),(able_index)]
        [(1,2,0,0),(2,3)]
        [(1,0,2,0),(1,3)]
        """
        # 栈中没东西，说明本层没有合适路径，需要退回上一层寻找，直接return
        if not stack_space:
            return
        else:
            # 最后一个数字查好了以后，栈中只可能有一个元素
            # 如果没有数字可以插，表示需要判断这个元素是不是满足要求
            if not insert_no:
                # 把该元素弹出来，去判断是不是符合要求
                temp_item = stack_space.pop()
                temp_address = list(temp_item[0])
                temp_routine = []
                # 如果满足了要求，修改标志位，修改result（result必须是可变的），return
                if self._find_one_routine(Order(temp_address), temp_routine):
                    result.append((temp_routine, Order(temp_address)))
                    # 修改标志位
                    self._random_flag = True
                    return
            # 如果还有能插的位置，则对该栈中的元素洗牌后，依次弹出，弹的每一个去计算新表，然后递归调用
            else:
                # 这里其实也可以对插入数字的队列进行洗牌，显得更加的随机
                curr_insert_no = insert_no.pop()
                random.shuffle(stack_space)
                while stack_space and (not self._random_flag):
                    # 弹出一个，进行操作
                    temp_item = stack_space.pop()
                    temp_address = temp_item[0].copy()
                    temp_index = deque(temp_item[1].copy())
                    # 下面进行插入操作，可行结果放到新的stack中，进行后续递归
                    new_stack_space = []
                    # 循环进行几次，取决有有多少个空位
                    loop_times = len(temp_index)
                    for i in range(loop_times):
                        curr_index = temp_index.popleft()
                        temp_address[curr_index] = curr_insert_no
                        if self.arr_checker(temp_address):
                            # 将新的一个下一折的地址和对应空位的信息打包放入新栈
                            new_stack_space.append(((temp_address.copy()), temp_index.copy()))
                        # 还原操作
                        temp_address[curr_index] = 0
                        temp_index.append(curr_index)
                    # 某一个排列对应的next的新表做好了以后，直接递归调用求下一次的
                    self._prepare_for_random(new_stack_space, insert_no.copy(), result)

    def _get_init_pool(self):
        """
        该函数主要为了获得从组合中推断出的最原始池子，分为BE模式和非BE模式
        :return:
        """
        # 这里需要对Begin/End模式的行为进行优化，将控制点的绝对位置固定住，加快运算
        # 不管什么模式都需要创建两个池子，一个放数组，一个放插入位置的索引
        arr_pool = deque()
        index_pool = deque()
        insert_no = set(range(1, self._height + 1)) - set(self._control_points_rank)
        if self._begin_end_mode:
            # 如果是BE模式，需要将控制点头尾去掉，将头尾固定在第一个和最后一个位置的位置，在对剩余的点做组合
            # 有BE限制，只有2~n-1可以插
            folder_set = set(range(1, self._height - 1))
            # 这里需要都减去2
            iter_index = combinations(range(self._height - 2),
                                      len(self._control_points_rank) - 2)
            # 把池子初始化
            # 例如，self._control_points_rank = [1, 3, 2], self._height = 4
            # 初始化后的结果为：
            #    arr_pool:          index_pool:
            # [  [1, 3, 0, 2]  ]        [ [2] ]
            # [  [1, 0, 3, 2]  ]        [ [1] ]
            for item in iter_index:
                arr = np.zeros(self._height, dtype=int)
                # 每一个位置相当于往后都推了一格
                new_item = [i + 1 for i in list(item)]
                # 相应的我们只需要取cp除了首位的控制点
                arr[new_item] = self._control_points_rank[1:-1]
                arr[0] = self._control_points_rank[0]
                arr[-1] = self._control_points_rank[-1]
                # 因为folder_set是2~n-1所以new_item也应该是2~n-1中的某些数字
                insert_index = deque(folder_set - set(new_item))
                if self.arr_checker(arr):
                    arr_pool.append(arr)
                    index_pool.append(insert_index)
        else:
            # 没有BE限制，所有位置都可以插
            folder_set = set(range(self._height))
            # 先将控制点的相对顺序固定好
            iter_index = combinations(range(self._height),
                                      len(self._control_points_rank))
            # 把池子初始化
            # 例如，self._control_points_rank = [1, 2], self._height = 3
            # 初始化后的结果为：
            #    arr_pool:          index_pool:
            # [  [1, 2, 0]  ]        [ [2] ]
            # [  [1, 0, 2]  ]        [ [1] ]
            # [  [0, 1, 2]  ]        [ [0] ]
            for item in iter_index:
                arr = np.zeros(self._height, dtype=int)
                arr[list(item)] = self._control_points_rank
                insert_index = deque(folder_set - set(item))
                if self.arr_checker(arr):
                    arr_pool.append(arr)
                    index_pool.append(insert_index)
        return arr_pool, index_pool, insert_no

    def _create_init(self):
        # 调用创建池子，获得初始随机池子
        arr_pool, index_pool, insert_no = self._get_init_pool()
        # 开始pop
        # 当要插入的数字非空时，进行循环
        try:
            temp_arr = arr_pool.popleft()
            temp_index = index_pool.popleft()
        except IndexError:
            return
        # if not insert_no:
        #     self._init_orders.append(Order(temp_arr))
        while insert_no:
            temp_insert = insert_no.pop()
            while len(temp_index) > len(insert_no):
                loop_times = len(temp_index)
                for i in range(loop_times):
                    to_insert = temp_index.popleft()
                    temp_arr[to_insert] = temp_insert
                    if self.arr_checker(temp_arr):
                        arr_pool.append(temp_arr.copy())
                        index_pool.append(temp_index.copy())
                    # 还原
                    temp_arr[to_insert] = 0
                    temp_index.append(to_insert)
                try:
                    temp_arr = arr_pool.popleft()
                    temp_index = index_pool.popleft()
                except IndexError:
                    return

        # 循环结束以后多把第一个排列弹出了
        arr_pool.appendleft(temp_arr)
        index_pool.appendleft(temp_index)
        while arr_pool:
            address = arr_pool.pop()
            self._init_orders.append(Order(address))

    def arr_checker(self, arr):
        """
        检查arr是否可折
        :param arr:
        :return:
        """
        odd, even = self.get_need_seg(arr)
        return Order.judge_list(odd) and Order.judge_list(even)

    def get_need_seg(self, arr):
        if self._height % 2 != 0:
            # 这里的切片设置需要对分割过程有一定的总结，最好在纸上推导一下。
            odd_list = [(x, y) for x, y in zip(arr[:-2:2],
                                               arr[1:-1:2]) if x * y != 0]
            even_list = [(x, y) for x, y in zip(arr[1:-1:2],
                                                arr[2::2]) if x * y != 0]
        else:
            odd_list = [(x, y) for x, y in zip(arr[:-1:2],
                                               arr[1::2]) if x * y != 0]
            even_list = [(x, y) for x, y in zip(arr[1:-2:2],
                                                arr[2:-1:2]) if x * y != 0]
        return odd_list, even_list

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


if __name__ == '__main__':
    r = Suite(10, 10)
    r.control_points = [(1,2)]
    for i in range(10):
        r.random()
        print(r.random_routine)