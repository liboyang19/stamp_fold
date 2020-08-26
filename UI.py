import tkinter as tk
from collections import deque
from Room import Room
from Order import Order


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
        # 一些房间基本参数
        self.cell_size = 100
        self.room_height = 5
        self.room_width = 5
        self.control_points = []
        # 起点终点
        self.begin_point = []
        self.end_point = []
        # 画界面
        self.draw_surface()

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
        self.tip_info1["text"] = "请输入房间大小信息："
        self.tip_info1.grid(row=0, column=0, columnspan=2, padx=0, pady=0)

        self.input_width_text = tk.Label(self.info_region)
        self.input_width_text["text"] = "宽："
        self.input_width_text.grid(row=1, column=0)

        self.input_height_text = tk.Label(self.info_region)
        self.input_height_text["text"] = "长："
        self.input_height_text.grid(row=2, column=0)

        self.input_width = tk.Entry(self.info_region, width=5)
        self.input_width.grid(row=1, column=1)

        self.input_height = tk.Entry(self.info_region, width=5)
        self.input_height.grid(row=2, column=1)

        tk.Label(self.info_region, text="").grid(row=3, column=0)

        self.generate_bt = tk.Button(self.info_region)
        self.generate_bt["text"] = "生成房间"
        self.generate_bt["command"] = self.generate_room
        self.generate_bt.grid(row=4, column=1)

        # 占位
        interval = 5
        start_row = 5
        end_row = start_row + interval
        for i in range(start_row, end_row):
            tk.Label(self.info_region, text="").grid(row=i, column=0)

        self.confirm_bt = tk.Button(self.info_region)
        self.confirm_bt["text"] = "确定"
        self.confirm_bt["command"] = self.confirm
        self.confirm_bt.grid(row=end_row, column=1)

        tk.Label(self.info_region, text="").grid(row=end_row + 1, column=0)

        self.next_bt = tk.Button(self.info_region)
        self.next_bt["text"] = "下一页"
        self.next_bt["command"] = self.next_page
        self.next_bt.grid(row=end_row + 2, column=1)

        # 用该变量判断是否为起终点模式
        self.is_ht = tk.IntVar()
        self.ht_checkbtn = tk.Checkbutton(self.info_region,
                                          text="Begin/End Mode",
                                          variable=self.is_ht)
        self.ht_checkbtn.grid(row=end_row + 3, column=1)

    def set_control_points(self, event):
        self.room_canvas.focus_set()
        cp_rank = len(self.control_points) + 1
        cp = self.transform_axis((event.x, event.y), arg='real')
        if self.is_ht.get():
            if not self.begin_point:
                self.begin_point.append(cp)
                self.draw_no(cp, content='S')
                print("Begin: ", event.x, event.y)
                return
            elif not self.end_point:
                self.end_point.append(cp)
                self.draw_no(cp, content='E')
                print("End: ", event.x, event.y)
                return
        self.control_points.append(cp)
        print("clicked at", event.x, event.y)
        self.draw_no(cp, content=cp_rank)
        print(self.control_points)
        print("Control_points_no:%d" % cp_rank)

    def callback(self, event):
        print(self.rec.canvasx(event.x))
        self.rec.focus_set()
        # if event.x < 50 and event.y < 50:
        #     self.create_button()
        print("clicked at", event.x, event.y)

    def color_config(self):
        # 所有的用户设置
        # 颜色可以是 #00000
        self.color_set = {}
        self.color_set["room"] = "blue"
        self.color_set["routine"] = "green"
        self.color_set["control_points"] = "green"
        self.color_set["cell_gap"] = "black"
        self.color_set["font_color"] = "red"

    def generate_room(self):
        """
        生成房间
        :return:
        """
        self.clean_room()
        self.room_height = int(self.input_height.get())
        self.room_width = int(self.input_width.get())
        self.create_room()
        self.room = Room(height=self.room_height, width=self.room_width)

    def next_page(self):
        self.room_canvas.delete("all")
        self.create_cell()
        if self.is_ht.get():
            self.draw_no(self.begin_point[0], 'B')
            self.draw_no(self.end_point[0], 'E')
        for i, c in enumerate(self.control_points, 1):
            self.draw_no(c, i)
        self.draw_routine()

    def confirm(self):
        """
        开始寻找路径
        :return:
        """
        self.room.control_points = self.begin_point + self.control_points + self.end_point
        self.room.begin_end_mode = bool(self.is_ht.get())
        print("计算中...")
        self.room.run()
        print("计算完毕...")
        self.routines = deque(self.room.routines)
        self.next_page()
        print(self.room.routines)

    def draw_routine(self):
        if not self.routines:
            print("没有合适路径")
            return
        # 先取出来一个
        current_routine = self.routines.popleft()
        routine_pixel = list(map(self.transform_axis, current_routine))
        self.connect(routine_pixel)
        # 然后又加到队尾
        self.routines.append(current_routine)

    def clean_room(self):
        """
        清除房间
        :return:
        """
        self.room_canvas.destroy()
        self.control_points = []
        self.begin_point = []
        self.end_point = []

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

    def draw_no(self, coord, content):
        (real_x, real_y) = self.transform_axis(coord, arg='virtual')
        font_size = int(self.cell_size * 0.3)
        self.room_canvas.create_text((real_x, real_y),
                                     text="{}".format(content),
                                     fill=self.color_set["font_color"],
                                     font=('Menlo', '%s' % font_size))
        circle_x_0, circle_x_1 = (real_x - int(font_size * 0.6),
                                  real_x + int(font_size * 0.6))
        circle_y_0, circle_y_1 = (real_y - int(font_size * 0.6),
                                  real_y + int(font_size * 0.6))
        self.room_canvas.create_oval((circle_x_0, circle_y_0,
                                      circle_x_1, circle_y_1),
                                     width=2,
                                     outline=self.color_set["font_color"])

    def connect(self, l):
        """
        连接l中的所有点
        :return:
        """
        for (start_x, start_y), (end_x, end_y) in zip(l[:-1], l[1:]):
            self.room_canvas.create_line(start_x, start_y, end_x, end_y,
                                         fill=self.color_set["routine"],
                                         width=self.cell_size // 10)

    def test(self):
        """
        测试
        :return:
        """
        pass

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Clean Room")
    app = Application(master=root)
    app.mainloop()