import tkinter as tk
from tkinter import ttk


class Canvas(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.cell_size = 100
        # Set language
        self.info_set = {}
        self.color_set = {}
        # Parameters
        self._room_width = 0
        self._room_height = 0
        self._control_points = []
        # Begin and end points.
        self._begin_point = []
        self._end_point = []
        # Set of horizontal and vertical coordinates of all points to determine
        # if the control points and starting point meet the limits.
        self.points_x = set()
        self.points_y = set()
        self.small_widget = {}
        self.display_option = {'cell': False,
                               'arrow': False,
                               'vanilla': True,
                               'points': True}
        # Apply settings
        self.set_color()
        self.set_language()

    @property
    def room_width(self):
        return self._room_width

    @property
    def room_height(self):
        return self._room_height

    @room_width.setter
    def room_width(self, width):
        self._room_width = width

    @room_height.setter
    def room_height(self, height):
        self._room_height = height

    @property
    def begin_end_mode(self):
        return bool(self.is_ht.get())

    @property
    def room_type(self):
        return self.small_widget['room_type_box'].get()

    @property
    def control_points(self):
        return self._control_points

    @property
    def begin_point(self):
        return self._begin_point

    @property
    def end_point(self):
        return self._end_point

    def draw_surface(self):
        # Draw separate areas for arrangement.
        # Draw a grid, i.e. many frames.
        self.draw_grid()
        self.create_info()
        self.create_room()

    def draw_grid(self):
        # Frame of the room area.
        self.room_region = tk.Frame(self)
        self.room_region.grid(row=0, column=0)

        # Frame of information area.
        self.info_region = tk.Frame(self)
        self.info_region.grid(row=0, column=1)

    def draw_room_floor(self, display=True):
        self.draw_room_floor_boundary()
        if self.display_option['cell'] or display:
            self.draw_room_floor_cell()

    def draw_room_floor_cell(self):
        gap_width = 3
        # 先画行线
        for i in range(self.cell_size,
                       (self.room_height - 1) * self.cell_size + 1,
                       self.cell_size):
            self.room_canvas.create_line(0, i,
                                         self.room_width * self.cell_size, i,
                                         fill=self.color_set["cell_gap"],
                                         width=gap_width)

        # 画列线
        for i in range(self.cell_size,
                       (self.room_width - 1) * self.cell_size + 1,
                       self.cell_size):
            self.room_canvas.create_line(i, 0,
                                         i, self.room_height * self.cell_size,
                                         fill=self.color_set["cell_gap"],
                                         width=gap_width)

    def draw_room_floor_boundary(self):
        gap_width = 4
        canvas_width = self.room_width * self.cell_size
        canvas_height = self.room_height * self.cell_size
        self.room_canvas.create_line(gap_width, gap_width, gap_width, canvas_height,
                                     fill=self.color_set["cell_gap"], width=gap_width)
        self.room_canvas.create_line(gap_width, gap_width, canvas_width, gap_width,
                                     fill=self.color_set["cell_gap"], width=gap_width)
        gap_width = 3
        self.room_canvas.create_line(canvas_width, gap_width,
                                     canvas_width, canvas_height,
                                     fill=self.color_set["cell_gap"], width=gap_width)
        self.room_canvas.create_line(gap_width, canvas_height,
                                     canvas_width, canvas_height,
                                     fill=self.color_set["cell_gap"], width=gap_width)

    def create_info(self):
        row = 0
        self.small_widget['tip_info'] = tk.Label(self.info_region)
        self.small_widget['tip_info']["text"] = self.info_set["tip_info1"]
        self.small_widget['tip_info'].grid(row=row, column=0)
        row += 1

        self.small_widget['input_width_text'] = tk.Label(self.info_region)
        self.small_widget['input_width_text']["text"] = self.info_set[
            "input_width_text"]
        self.small_widget['input_width_text'].grid(row=row, column=0)
        row += 1

        self.small_widget['input_height_text'] = tk.Label(self.info_region)
        self.small_widget['input_height_text']["text"] = self.info_set[
            "input_height_text"]
        self.small_widget['input_height_text'].grid(row=row, column=0)
        row += 1

        self.small_widget['input_width'] = ttk.Combobox(self.info_region,
                                                        width=5)
        self.small_widget['input_width']['value'] = self.info_set["input_size"]
        self.small_widget['input_width']['state'] = 'readonly'
        # 默认是 5 * 5 的房间
        self.small_widget['input_width'].current(2)
        self.small_widget['input_width'].grid(row=1, column=1)

        self.small_widget['input_height'] = ttk.Combobox(self.info_region,
                                                         width=5)
        self.small_widget['input_height']['value'] = self.info_set["input_size"]
        self.small_widget['input_height']['state'] = 'readonly'
        # 默认是 5 * 5 的房间
        self.small_widget['input_height'].current(2)
        self.small_widget['input_height'].grid(row=2, column=1)

        tk.Label(self.info_region, text="").grid(row=row, column=0)
        row += 1

        # 用该变量判断是否为起终点模式
        self.is_ht = tk.IntVar()
        self.small_widget['ht_checkbtn'] = tk.Checkbutton(self.info_region,
                                                          text=self.info_set["ht_checkbtn"],
                                                          variable=self.is_ht)

        self.small_widget['ht_checkbtn'].grid(row=row, column=0, columnspan=2)
        row += 1
        tk.Label(self.info_region, text="").grid(row=row, column=0)
        row += 1

        # 设置下拉框，用以选择计算模式
        self.small_widget['room_type_box'] = ttk.Combobox(self.info_region,
                                                          width=10)
        self.small_widget['room_type_box']['value'] = self.info_set[
            "room_type_box"]
        self.small_widget['room_type_box']['state'] = 'readonly'
        # 默认是X Y 型都计算
        self.small_widget['room_type_box'].current(0)
        self.small_widget['room_type_box'].grid(row=row, column=0, columnspan=2)
        row += 1

        tk.Label(self.info_region, text="").grid(row=row, column=0)
        row += 1

        self.small_widget['generate_bt'] = tk.Button(self.info_region)
        self.small_widget['generate_bt']['text'] = self.info_set["generate_bt"]
        self.small_widget['generate_bt'].grid(row=row, column=1)
        row += 1

        tk.Label(self.info_region, text="").grid(row=row, column=0)
        row += 1

        self.message = tk.Text(self.info_region, width=24, height=10)
        self.message.config(relief='groove', borderwidth=2)
        self.message.config(font='Menlo')
        self.message.config(background=self.color_set['text_bg'])
        self.message.grid(row=row, column=0, columnspan=2)
        row += 1

        tk.Label(self.info_region, text="").grid(row=row, column=0)
        row += 1

        self.small_widget['confirm_bt'] = tk.Button(self.info_region)
        self.small_widget['confirm_bt']['text'] = self.info_set["confirm_bt"]
        self.small_widget['confirm_bt'].grid(row=row, column=0)
        row += 1

        tk.Label(self.info_region, text="").grid(row=row, column=0)
        row += 1

        self.small_widget["next_bt"] = tk.Button(self.info_region)
        self.small_widget["next_bt"]["text"] = self.info_set["next_bt"]
        # 此按钮在计算完成前不能使用
        self.small_widget["next_bt"].config(state='disabled')
        row -= 2
        self.small_widget["next_bt"].grid(row=row, column=1)
        row += 1
        tk.Label(self.info_region, text="").grid(row=row, column=0)
        row += 1

        self.small_widget['random_bt'] = tk.Button(self.info_region)
        self.small_widget['random_bt']["text"] = self.info_set["random_bt"]
        self.small_widget['random_bt'].grid(row=row, column=1)
        row += 1

        tk.Label(self.info_region, text="").grid(row=row, column=0)
        row += 1

    def bind_event(self, generate_room, confirm, next_page, random):
        self.small_widget['generate_bt']["command"] = generate_room
        self.small_widget['confirm_bt']["command"] = confirm
        self.small_widget["next_bt"]["command"] = next_page
        self.small_widget['random_bt']["command"] = random

    def set_control_points(self, event):
        # 设置控制点
        self.room_canvas.focus_set()
        # 如果已经点了一个点，则起终点模式不能再调整
        self.small_widget['ht_checkbtn'].config(state='disabled')
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
                return
            elif not self.end_point:
                if not self.points_checker(cp):
                    return
                self.end_point.append(cp)
                self.draw_no(cp, 'E', self.color_set["BE_points"])
                return
        # 如果不是起终点，则标记为控制点，将点存进去
        # 还要判断这个点是否符合限制条件
        if not self.points_checker(cp):
            return
        self._control_points.append(cp)
        # 画出控制点
        self.draw_no(cp, cp_rank, self.color_set["control_points"])

    def create_room(self):
        self.get_user_room_size()
        size_lim = max(self.room_width, self.room_height)
        if size_lim > 8:
            self.cell_size = 800 // size_lim
        room_canvas_height = self.room_height * self.cell_size
        room_canvas_width = self.room_width * self.cell_size
        self.room_canvas = tk.Canvas(self.room_region,
                                     height=room_canvas_height,
                                     width=room_canvas_width,
                                     bg=self.color_set["room"], )

        self.room_canvas.pack()
        # 画网格
        self.draw_room_floor()
        self.room_canvas.bind("<Button-1>", self.set_control_points)

    def points_checker(self, p):
        """
        判断点 p 是否符合控制点的限制条件
        :param p:
        :return:
        """
        condition = self.small_widget['room_type_box'].get()
        if condition == self.info_set["room_type_box"][0]:
            # 如果是 X 型，则规定所有点不能在同一行
            if p[1] in self.points_y:
                return False
            else:
                self.points_x.add(p[0])
                self.points_y.add(p[1])
                return True
        elif condition == self.info_set["room_type_box"][1]:
            # 如果是 Y 型，则规定所有点不能在同一列
            if p[0] in self.points_x:
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

    def draw_routine(self, routine):
        routine_pixel = list(map(self.transform_axis, routine))
        self.connect(routine_pixel)

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
        if self.display_option['arrow']:
            self.draw_start_circle(l)
            self.draw_end_arrow(l)

    def draw_start_circle(self, l):
        # 将起点处标记为圆圈
        start_x, start_y = l[0]
        circle_coords = self.draw_circle(start_x, start_y,
                                         int(self.cell_size * 0.1))
        left_x, right_x, up_y, down_y = circle_coords
        self.room_canvas.create_oval((left_x, up_y,
                                      right_x, down_y),
                                     width=2,
                                     outline=self.color_set["routine"],
                                     fill=self.color_set["routine"])

    def draw_end_arrow(self, l):
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
        :param (x,y) bottom midpoint
        :param l: half bottom
        :return: Coordinates of the three vertices of the triangle.
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
        Return the coordinates of the circle with (x,y) as the center and r as the radius.
        """
        left_x, right_x = x - r, x + r
        up_y, down_y = y - r, y + r
        return left_x, right_x, up_y, down_y

    def get_user_room_size(self):
        self.room_width = int(self.small_widget['input_width'].get())
        self.room_height = int(self.small_widget['input_height'].get())

    def draw_page(self, routine, cur_no, total_num):
        self.message.config(state='normal')
        self.message.delete(4.0, 5.0)
        self.message.insert(tk.END, "%s / %s\n" % (cur_no, total_num))
        self.message.config(state='disabled')
        self.room_canvas.delete("all")
        self.draw_room_floor(False)
        self.draw_routine(routine=routine)
        if self.display_option['points']:
            self.draw_begin_end_points()
            self.draw_control_points()

    def draw_begin_end_points(self):
        if self.is_ht.get():
            self.draw_no(self.begin_point[0], 'S', self.color_set["BE_points"])
            self.draw_no(self.end_point[0], 'E', self.color_set["BE_points"])

    def draw_control_points(self):
        for i, c in enumerate(self.control_points, 1):
            self.draw_no(c, i, self.color_set["control_points"])

    def finish_info(self):
        self.insert_message(self.info_set['finish'])

    def not_found_info(self):
        self.insert_message(self.info_set['not_found'])

    def found_random_path(self):
        self.insert_message(self.info_set['random_found'])

    def computing_info(self):
        self.insert_message(self.info_set['computing'])

    def select_points_info(self):
        self.insert_message(self.info_set['select_points'])

    def insert_message(self, msg):
        self.message.config(state='normal')
        self.message.insert(tk.END, msg)
        self.message.config(state='disabled')

    def switch_btn_status(self, **kwargs):
        for btn_name, status in kwargs.items():
            self.small_widget[btn_name].config(state=status)

    def set_color(self):
        self.color_set["cell_gap"] = "black"          # 黑色
        self.color_set["font_color"] = "#ffffff"      # 白色
        self.color_set["text_bg"] = "#FFEAE5"
        self.color_set["BE_points"] = "#eb4891"       # 草莓红
        self.color_set["control_points"] = "#3e8c27"  # 三叶草绿
        if self.display_option['vanilla']:
            self.color_set["room"] = "white"
            self.color_set["routine"] = "black"
        else:
            self.color_set["room"] = "#fff953"        # 柠檬黄
            self.color_set["routine"] = "#3d97f7"     # 浅蓝色

    def lock(self):
        self.small_widget['ht_checkbtn'].config(state='disabled')
        self.small_widget['room_type_box'].config(state='disabled')
        self.small_widget['generate_bt'].config(state='disabled')
        self.small_widget['confirm_bt'].config(state='disabled')
        self.small_widget['random_bt'].config(state='disabled')
        self.room_canvas.unbind("<Button-1>")

    def unlock(self):
        self.small_widget['ht_checkbtn'].config(state='normal')
        self.small_widget['room_type_box'].config(state='readonly')
        self.small_widget['confirm_bt'].config(state='normal')
        self.small_widget['generate_bt'].config(state='normal')

    def clear(self):
        self.room_canvas.destroy()
        self._begin_point = []
        self._end_point = []
        self._control_points = []
        self.points_x = set()
        self.points_y = set()
        self.clear_board()
        # 安排锁定
        self.small_widget["next_bt"].config(state='disabled')

    def clear_board(self):
        """
        清除消息框
        :return:
        """
        self.message.config(state='normal')
        self.message.delete(0.0, tk.END)
        self.message.config(state='disabled')

    def set_language(self):
        # Interface language.
        self.info_set["tip_info1"] = "Size: "
        self.info_set["input_width_text"] = "Width: "
        self.info_set["input_height_text"] = "Height: "
        self.info_set["ht_checkbtn"] = "Begin/End Mode"
        self.info_set["generate_bt"] = "Reset"
        self.info_set["confirm_bt"] = "Find All"
        self.info_set["next_bt"] = "Next"
        self.info_set["room_type_box"] = ("X mode", "Y mode", "X/Y mode")
        self.info_set["select_points"] = "Selecting points...\n"
        self.info_set["computing"] = "Computing...\n"
        self.info_set["finish"] = "Complete!\n"
        self.info_set["not_found"] = "No routine found.\n"
        self.info_set["input_size"] = "3 4 5 6 7 8 9 10 11 12".split()
        self.info_set["random_bt"] = "Random"
        self.info_set["random_found"] = "Random routine found.\n"
