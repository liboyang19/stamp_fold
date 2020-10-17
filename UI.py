import tkinter as tk
from collections import deque
from Room import Room
import threading
import time
from tkinter import ttk
from Canvas import Canvas


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.interface = Canvas(self)
        # Basic parameters.
        self.room_height = 0
        self.room_width = 0
        # Draw_surface
        self.draw_interface()
        # Generate room
        self.generate_room()

    def draw_interface(self):
        self.interface.draw_surface()
        self.interface.bind_event(generate_room=self.generate_room,
                                  confirm=self.confirm,
                                  next_page=self.next_page,
                                  random=self.random)
    #     self.interface.bind("<Button-1>", self.test_click)
    #
    # def test_click(self, event):
    #     print("Oh")

    def generate_room(self):
        """
        生成房间
        :return:
        """
        self.clean_room()
        self.room_height = self.interface.room_height
        self.room_width = self.interface.room_width
        self.interface.create_room()
        self.update_info()
        self.interface.select_points_info()

    def clean_room(self):
        """
        打扫干净屋子
        :return:
        """
        self.interface.clear()
        # 解除锁定
        self.unlock()

    def next_page(self):
        if not self.routines:
            return
        self.counter = (self.counter % len(self.routines)) + 1
        current_routine = self.routines.popleft()
        self.interface.draw_page(routine=current_routine,
                                 cur_no=self.counter,
                                 total_num=len(self.routines) + 1)
        self.routines.append(current_routine)

    def confirm(self):
        """
        Start looking for a path.
        :return:
        """
        # Settings before the calculation, print the current status.
        self.interface.clear_board()
        self.update_info()
        pre_compute_thread = threading.Thread(target=self.pre_compute, name='pre_compute')
        in_compute_thread = threading.Thread(target=self.in_compute, name='in_compute')
        pre_compute_thread.start()
        in_compute_thread.start()

    def random(self):
        """
        Randomly select a path.
        :return:
        """
        # 上传信息
        self.interface.clear_board()
        self.update_info()
        pre_compute_thread = threading.Thread(target=self.pre_compute, name='pre_random_compute')
        in_compute_thread = threading.Thread(target=self.in_random_compute, name='in_random_compute')
        pre_compute_thread.start()
        in_compute_thread.start()

    def in_random_compute(self):
        """
        进行随机巡径，并输出结果
        :return:
        """
        # 防止粘包
        time.sleep(0.01)
        self.room.random()
        # print("计算完毕...")
        self.interface.finish_info()
        # 可以使用下一页按钮
        self.interface.switch_btn_status(next_bt='normal')
        self.routines = deque()
        if self.room.random_routine:
            self.routines.append(self.room.random_routine)
        if not self.routines:
            self.interface.not_found_info()
        else:
            self.interface.found_random_path()
        self.after_compute()

    def after_compute(self):
        """
        输出计算结果
        :return:
        """
        self.counter = 0
        self.interface.insert_message(' \n')
        self.next_page()
        self.reset_btn_after_computer()

    def reset_btn_after_computer(self):
        self.interface.switch_btn_status(generate_bt='normal',
                                         random_bt='normal',
                                         confirm_bt='normal')

    def update_info(self):
        """
        将房间信息传递到房间类中
        :return:
        """
        self.room = Room(height=self.room_height, width=self.room_width, )
        self.room.control_points = list(self.interface.begin_point +
                                        self.interface.control_points +
                                        self.interface.end_point)
        self.room.begin_end_mode = self.interface.begin_end_mode
        self.room.suite_type = self.interface.room_type

    def pre_compute(self):
        """
        进行计算前的准备工作
        :return:
        """
        self.lock()
        # print("计算中...")
        self.interface.computing_info()

    def in_compute(self):
        """
        进行计算，并输出计算结果
        :return:
        """
        # 防止粘包
        time.sleep(0.01)
        self.room.run()
        # print("计算完毕...")
        self.interface.finish_info()
        # 可以使用下一页按钮
        self.interface.switch_btn_status(next_bt='normal')
        self.routines = deque(self.room.routines)
        if not self.routines:
            self.interface.not_found_info()
        else:
            self.insert_message("%s routines found.\n" % len(self.routines))
        self.after_compute()

    def lock(self):
        """
        Lock all the options that could cause unexpected results.
        :return:
        """
        return self.interface.lock()

    def unlock(self):
        return self.interface.unlock()

    def insert_message(self, msg):
        return self.interface.insert_message(msg)


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Clean Room")
    app = Application(master=root)
    app.mainloop()
