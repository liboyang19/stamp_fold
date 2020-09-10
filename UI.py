import tkinter as tk
from collections import deque
from Room import Room
from Order import Order
from tkinter import ttk


# Application 是继承 Frame 的，是一个 Frame
# 在 tkinter中，Frame相当于一个容器，所有的 Widget 都是放在上面的
# Widget 可以选择 master，就是它们 widget 的母版
# 利用这个思想，可以把界面的区域分割出来
class Application(tk.Frame):
    def __init__(self, master=None):
        # 这里的构造函数需要master作为参数，这里我们用root来初始化
        # 也就是说，Application 类的母版是在root上
        # 换句话说，Application 是 画在 root 上的一个 Frame
        # 所以这句话是先把父类构造好，用 master 去构造一个 frame
        super().__init__(master)
        self.master = master
        self.pack()
        # 设置颜色
        self.color_config()
        # 设置语言
        self.info_config()
        # 一些房间基本参数
        self.cell_size = 100
        self.room_height = 0
        self.room_width = 0
        self.control_points = []
        # 起点终点
        self.begin_point = []
        self.end_point = []
        # 所有点的横纵坐标集合，用以判断控制点和起点是否符合限制条件
        self.points_x = set()
        self.points_y = set()
        # 画界面
        self.draw_surface()
        # 生成房子
        # 前面的全局变量需要恢复
        self.generate_room()

    def draw_surface(self):
        """
        绘制主界面
        :return:
        """
        # 分别画出不同的区域，为了排列方便
        # 首先画出一个网格，也就是好多Frame
        self.create_grid()
        self.create_room()
        self.create_info()

    def create_grid(self):
        """
        创建区域，在区域上作图
        :return:
        """
        # room 区域的 Frame
        self.room_region = tk.Frame(self)
        self.room_region.grid(row=0, column=0)

        # 信息区域的Frame
        self.info_region = tk.Frame(self)
        self.info_region.grid(row=0, column=1)

    def create_cell(self):
        gap_width = 3
        # 先画行线
        for i in range(self.cell_size, self.room_height * self.cell_size + 1,
                       self.cell_size):
            self.room_canvas.create_line(0, i,
                                         self.room_width * self.cell_size, i,
                                         fill=self.color_set["cell_gap"],
                                         width=gap_width)

        # 画列线
        for i in range(self.cell_size, self.room_width * self.cell_size + 1,
                       self.cell_size):
            self.room_canvas.create_line(i, 0,
                                         i, self.room_height * self.cell_size,
                                         fill=self.color_set["cell_gap"],
                                         width=gap_width)

        # 画出边界上的两条线
        gap_width += 1
        self.room_canvas.create_line(gap_width, gap_width,
                                     self.room_width * self.cell_size,
                                     gap_width,
                                     fill=self.color_set["cell_gap"],
                                     width=gap_width)
        self.room_canvas.create_line(gap_width, gap_width,
                                     gap_width,
                                     self.room_width * self.cell_size,
                                     fill=self.color_set["cell_gap"],
                                     width=gap_width)

    def create_room(self):
        size_lim = max(self.room_width, self.room_height)
        if size_lim > 8:
            self.cell_size = 800 // size_lim
        room_canvas_height = self.room_height * self.cell_size
        room_canvas_width = self.room_width * self.cell_size
        self.room_canvas = tk.Canvas(self.room_region,
                                     height=room_canvas_height,
                                     width=room_canvas_width,
                                     bg=self.color_set["room"],)
        self.room_canvas.pack()
        # 画网格
        self.create_cell()
        # 绑定事件
        self.room_canvas.bind("<Button-1>", self.set_control_points)

    def create_info(self):
        self.tip_info1 = tk.Label(self.info_region)
        self.tip_info1["text"] = self.info_set["tip_info1"]
        self.tip_info1.grid(row=0, column=0)

        self.input_width_text = tk.Label(self.info_region)
        self.input_width_text["text"] = self.info_set["input_width_text"]
        self.input_width_text.grid(row=1, column=0)

        self.input_height_text = tk.Label(self.info_region)
        self.input_height_text["text"] = self.info_set["input_height_text"]
        self.input_height_text.grid(row=2, column=0)

        self.input_width = tk.Entry(self.info_region, width=5)
        self.input_width.insert(0, '5')
        self.input_width.grid(row=1, column=1)

        self.input_height = tk.Entry(self.info_region, width=5)
        self.input_height.insert(0, '5')
        self.input_height.grid(row=2, column=1)

        tk.Label(self.info_region, text="").grid(row=3, column=0)

        # 用该变量判断是否为起终点模式
        self.is_ht = tk.IntVar()
        self.ht_checkbtn = tk.Checkbutton(self.info_region,
                                          text=self.info_set["ht_checkbtn"],
                                          variable=self.is_ht)
        self.ht_checkbtn.grid(row=4, column=0, columnspan=2)

        tk.Label(self.info_region, text="").grid(row=5, column=0)

        # 设置下拉框，用以选择计算模式
        self.room_type_box = ttk.Combobox(self.info_region, width=10)
        self.room_type_box['value'] = self.info_set["room_type_box"]
        self.room_type_box['state'] = 'readonly'
        # 默认是X Y 型都计算
        self.room_type_box.current(2)
        self.room_type_box.grid(row=6, column=0, columnspan=2)

        tk.Label(self.info_region, text="").grid(row=7, column=0)

        self.generate_bt = tk.Button(self.info_region)
        self.generate_bt["text"] = self.info_set["generate_bt"]
        self.generate_bt["command"] = self.generate_room
        self.generate_bt.grid(row=8, column=1)

        tk.Label(self.info_region, text="").grid(row=9, column=0)

        # # 占位
        # interval = 5
        # start_row = 9
        # end_row = start_row + interval
        # for i in range(start_row, end_row):
        #     tk.Label(self.info_region, text="").grid(row=i, column=0)

        self.message = tk.Text(self.info_region, width=24, height=10)
        self.message.config(relief='groove', borderwidth=2)
        self.message.config(font='Menlo')
        self.message.config(background=self.color_set['text_bg'])
        self.message.grid(row=10, column=0, columnspan=2)

        tk.Label(self.info_region, text="").grid(row=11, column=0)

        self.confirm_bt = tk.Button(self.info_region)
        self.confirm_bt["text"] = self.info_set["confirm_bt"]
        self.confirm_bt["command"] = self.confirm
        self.confirm_bt.grid(row=12, column=1)

        tk.Label(self.info_region, text="").grid(row=13, column=0)

        self.next_bt = tk.Button(self.info_region)
        self.next_bt["text"] = self.info_set["next_bt"]
        self.next_bt["command"] = self.next_page
        # 此按钮在计算完成前不能使用
        self.next_bt.config(state='disabled')
        self.next_bt.grid(row=14, column=1)

    def set_control_points(self, event):
        # 设置控制点
        self.room_canvas.focus_set()
        # 如果已经点了一个点，则起终点模式不能再调整
        self.ht_checkbtn.config(state='disabled')
        # 确定现在是第几个控制点
        cp_rank = len(self.control_points) + 1
        # 将实际坐标转换为数学坐标
        cp = self.transform_axis((event.x, event.y), arg='real')
        # 如果勾选了起终点模式，则判断点的坐标是否为起终点
        if self.is_ht.get():
            if not self.begin_point:
                if not self.points_checker(cp):
                    return
                self.begin_point.append(cp)
                self.draw_no(cp, 'S', self.color_set["BE_points"])
                # print("Begin: ", event.x, event.y)
                return
            elif not self.end_point:
                if not self.points_checker(cp):
                    return
                self.end_point.append(cp)
                self.draw_no(cp, 'E', self.color_set["BE_points"])
                # print("End: ", event.x, event.y)
                return
        # 如果不是起终点，则标记为控制点，将点存进去
        # 还要判断这个点是否符合限制条件
        if not self.points_checker(cp):
            return
        self.control_points.append(cp)
        # print("clicked at", event.x, event.y)
        # 画出控制点
        self.draw_no(cp, cp_rank, self.color_set["control_points"])
        # print(self.control_points)
        # print("Control_points_no:%d" % cp_rank)

    def generate_room(self):
        """
        生成房间
        :return:
        """
        self.clean_room()
        self.room_height = int(self.input_height.get())
        self.room_width = int(self.input_width.get())
        self.create_room()
        self.room = Room(height=self.room_height, width=self.room_width,)
        self.message.insert(tk.END, self.info_set["select_points"])

    def clean_room(self):
        """
        打扫干净屋子
        :return:
        """
        self.room_canvas.destroy()
        # 解除锁定
        self.ht_checkbtn.config(state='normal')
        self.room_type_box.config(state='readonly')
        self.control_points = []
        self.begin_point = []
        self.end_point = []
        self.points_x = set()
        self.points_y = set()
        self.message.delete(0.0, tk.END)
        # 安排锁定
        self.next_bt.config(state='disabled')

    def next_page(self):
        if not self.routines:
            return
        self.counter = (self.counter % len(self.routines)) + 1
        self.message.delete(5.0, 6.0)
        self.message.insert(tk.END, "%s / %s\n" % (self.counter, len(self.routines)))
        self.room_canvas.delete("all")
        self.create_cell()
        self.draw_routine()
        if self.is_ht.get():
            self.draw_no(self.begin_point[0], 'S', self.color_set["BE_points"])
            self.draw_no(self.end_point[0], 'E', self.color_set["BE_points"])
        for i, c in enumerate(self.control_points, 1):
            self.draw_no(c, i, self.color_set["control_points"])

    def confirm(self):
        """
        开始寻找路径
        :return:
        """
        # 锁定现有选项，避免产生动态错误
        self.lock()
        self.room.control_points = self.begin_point + self.control_points + self.end_point
        self.room.begin_end_mode = bool(self.is_ht.get())
        # print("计算中...")
        self.message.insert(tk.END, self.info_set['computing'])
        # 设置计算样式
        self.room.suite_type = self.room_type_box.get()
        self.room.run()
        # print("计算完毕...")
        self.message.insert(tk.END, self.info_set['finish'])
        # 可以使用下一页按钮
        self.next_bt.config(state='normal')
        self.routines = deque(self.room.routines)
        if not self.routines:
            self.message.insert(tk.END, self.info_set["not_found"])
        else:
            self.message.insert(tk.END, "%s routines found.\n" % len(self.routines))
        self.counter = 0
        self.message.insert(tk.END, " \n")
        self.next_page()
        # print(self.room.routines)

    def points_checker(self, p):
        """
        判断点 p 是否符合控制点的限制条件
        :param p:
        :return:
        """
        condition = self.room_type_box.get()
        if condition == self.info_set["room_type_box"][0]:
            # 如果是 X 型，则规定所有点不能在同一行
            if p[0] in self.points_x:
                return False
            else:
                self.points_x.add(p[0])
                self.points_y.add(p[1])
                return True
        elif condition == self.info_set["room_type_box"][1]:
            # 如果是 Y 型，则规定所有点不能在同一列
            if p[1] in self.points_y:
                return False
            else:
                self.points_x.add(p[0])
                self.points_y.add(p[1])
                return True
        elif condition == self.info_set["room_type_box"][2]:
            # 如果是 X/Y型，则规定所有点不能在同行同列
            if p[0] in self.points_x or p[1] in self.points_y:
                return False
            else:
                self.points_x.add(p[0])
                self.points_y.add(p[1])
                return True

    def draw_routine(self):
        # 先取出来一个
        current_routine = self.routines.popleft()
        routine_pixel = list(map(self.transform_axis, current_routine))
        self.connect(routine_pixel)
        # 然后又加到队尾
        self.routines.append(current_routine)

    def transform_axis(self, c, arg='virtual'):
        """
        真实坐标与建模坐标的转换
        :param c: 坐标
        :param arg: 参数
        :return:
        """
        if arg == 'real':
            real_cx, real_cy = c
            return ((real_cx // self.cell_size) + 1,
                    (real_cy // self.cell_size) + 1)
        if arg == 'virtual':
            virtual_cx, virtual_cy = c
            return (int((virtual_cx - 0.5) * self.cell_size),
                    int((virtual_cy - 0.5) * self.cell_size))
        raise TypeError("Wrong argument.")

    def draw_no(self, coord, content, color):
        (real_x, real_y) = self.transform_axis(coord, arg='virtual')
        font_size = int(self.cell_size * 0.3)
        oval_coords = self.draw_circle(real_x, real_y, int(font_size * 0.6))
        circle_x_0, circle_x_1, circle_y_0, circle_y_1 = oval_coords
        self.room_canvas.create_oval((circle_x_0, circle_y_0,
                                      circle_x_1, circle_y_1),
                                     width=2,
                                     outline=color,
                                     fill=color)
        self.room_canvas.create_text((real_x, real_y),
                                     text="{}".format(content),
                                     fill=self.color_set["font_color"],
                                     font=('Menlo', '%s' % font_size))

    def connect(self, l):
        """
        连接l中的所有点
        :return:
        """
        for (start_x, start_y), (end_x, end_y) in zip(l[:-1], l[1:]):
            self.room_canvas.create_line(start_x, start_y, end_x, end_y,
                                         fill=self.color_set["routine"],
                                         width=self.cell_size // 10)
        # 将起点处标记为圆圈
        start_x, start_y = l[0]
        circle_coords = self.draw_circle(start_x, start_y, int(self.cell_size * 0.1))
        left_x, right_x, up_y, down_y = circle_coords
        self.room_canvas.create_oval((left_x, up_y,
                                      right_x, down_y),
                                     width=2,
                                     outline=self.color_set["routine"],
                                     fill=self.color_set["routine"])

        # 将终点标记为三角
        end_x, end_y = l[-1]
        # 确定方向，默认向左
        face = 'L'
        for _, (p_x, p_y) in enumerate(l[::-1]):
            delta_p = (end_x - p_x, end_y - p_y)
            if delta_p[0] > 0:
                face = 'R'
                break
            elif delta_p[0] < 0:
                face = 'L'
                break
            elif delta_p[1] > 0:
                face = 'D'
                break
            elif delta_p[1] < 0:
                face = 'U'
                break
        triangle_points = self.draw_triangle(end_x, end_y,
                                             int(self.cell_size * 0.1),
                                             face=face)
        self.room_canvas.create_polygon(triangle_points,
                                        fill=self.color_set["routine"])

    @staticmethod
    def draw_triangle(x, y, l, face):
        """
        画三角形
        :param (x,y) 底边中点
        :param l: 底边的一半
        :param face: 朝向
        :return:
        """
        if face == 'U':
            # 面朝上
            x_0, y_0 = x - l, y
            x_2, y_2 = x + l, y
            x_1, y_1 = x, y - 2 * l
        elif face == 'D':
            # 面朝下
            x_0, y_0 = x - l, y
            x_2, y_2 = x + l, y
            x_1, y_1 = x, y + 2 * l
        elif face == 'L':
            # 面朝左
            x_0, y_0 = x, y - l
            x_2, y_2 = x, y + l
            x_1, y_1 = x - 2 * l, y
        elif face == 'R':
            # 面朝右
            x_0, y_0 = x, y - l
            x_2, y_2 = x, y + l
            x_1, y_1 = x + 2 * l, y
        else:
            raise ValueError("Face doesn't accept a keyword: % s" % face)
        return [x_0, y_0, x_1, y_1, x_2, y_2]

    @staticmethod
    def draw_circle(x, y, r):
        """
        返回以(x,y)为圆心，r为半径的圆的四周坐标
        """
        left_x, right_x = x - r, x + r
        up_y, down_y = y - r, y + r
        return left_x, right_x, up_y, down_y

    def lock(self):
        """
        锁定所有可能引起计算bug的选项
        :return:
        """
        self.ht_checkbtn.config(state='disabled')
        self.room_type_box.config(state='disabled')
        self.room_canvas.unbind("<Button-1>")

    def color_config(self):
        # 所有的用户设置
        # 颜色可以是 #00000
        self.color_set = {}
        self.color_set["room"] = "#fff953"                   # 柠檬黄
        self.color_set["routine"] = "#3d97f7"                # 浅蓝色
        self.color_set["BE_points"] = "#eb4891"              # 草莓红
        self.color_set["control_points"] = "#3e8c27"         # 三叶草绿
        self.color_set["cell_gap"] = "black"                 # 黑色
        self.color_set["font_color"] = "#ffffff"             # 白色
        self.color_set["text_bg"] = "#FFEAE5"

    def info_config(self):
        # 界面语言自定义
        self.info_set = {}
        self.info_set["tip_info1"] = "Size: "
        self.info_set["input_width_text"] = "Width: "
        self.info_set["input_height_text"] = "Height: "
        self.info_set["ht_checkbtn"] = "Begin/End Mode"
        self.info_set["generate_bt"] = "Reset"
        self.info_set["confirm_bt"] = "Confirm"
        self.info_set["next_bt"] = "Next"
        self.info_set["room_type_box"] = ("X mode", "Y mode", "X/Y mode")
        self.info_set["select_points"] = "Selecting points...\n"
        self.info_set["computing"] = "Computing...\n"
        self.info_set["finish"] = "Complete!\n"
        self.info_set["not_found"] = "No routine found.\n"


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Clean Room")
    app = Application(master=root)
    app.mainloop()
