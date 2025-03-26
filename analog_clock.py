import tkinter as tk
import math
import time
from datetime import datetime

class AnalogClock(tk.Canvas):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(background='#F0F0F0')  # 淺灰色背景
        self.create_clock_face()
        self.hands = []
        self.update_clock()

    def create_clock_face(self):
        # Create clock circle
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()
        self.center_x = width // 2
        self.center_y = height // 2
        self.radius = min(width, height) // 2 - 20  # 稍微縮小半徑以留出更多邊距

        # Draw the outer circle with gradient effect
        outer_circle = self.create_oval(
            self.center_x - self.radius - 5,
            self.center_y - self.radius - 5,
            self.center_x + self.radius + 5,
            self.center_y + self.radius + 5,
            width=3,
            outline='#2C3E50'  # 深藍灰色外圈
        )

        # Draw inner circle for better appearance
        inner_circle = self.create_oval(
            self.center_x - self.radius,
            self.center_y - self.radius,
            self.center_x + self.radius,
            self.center_y + self.radius,
            width=2,
            outline='#34495E',  # 較淺的藍灰色內圈
            fill='#FFFFFF'      # 純白色填充
        )

        # Draw hour markers
        for i in range(60):  # 增加到60個刻度，包含分鐘刻度
            angle = i * math.pi/30 - math.pi/2
            if i % 5 == 0:  # 整點刻度
                start_r = self.radius - 15
                end_r = self.radius - 5
                width = 3
                color = '#2C3E50'  # 深藍灰色
            else:  # 分鐘刻度
                start_r = self.radius - 10
                end_r = self.radius - 5
                width = 1
                color = '#7F8C8D'  # 淺灰色

            start_x = self.center_x + start_r * math.cos(angle)
            start_y = self.center_y + start_r * math.sin(angle)
            end_x = self.center_x + end_r * math.cos(angle)
            end_y = self.center_y + end_r * math.sin(angle)
            self.create_line(start_x, start_y, end_x, end_y, width=width, fill=color)

        # Add hour numbers
        for i in range(1, 13):
            angle = i * math.pi/6 - math.pi/2
            r = self.radius - 35  # 數字位置稍微向內
            x = self.center_x + r * math.cos(angle)
            y = self.center_y + r * math.sin(angle)
            # 創建數字標籤
            self.create_text(x, y, text=str(i), font=('Arial', 14, 'bold'), fill='#2C3E50')

    def update_clock(self):
        # Clear previous hands
        for hand in self.hands:
            self.delete(hand)
        self.hands.clear()

        # Get current time
        now = datetime.now()
        hours, minutes, seconds = now.hour, now.minute, now.second
        milliseconds = now.microsecond / 1000000  # 添加毫秒以使移動更平滑

        # Hour hand
        hour_angle = (hours % 12 + minutes / 60) * 30 - 90
        hour_hand = self.create_hand(hour_angle, self.radius * 0.5, 6, '#2C3E50')  # 深藍灰色
        self.hands.append(hour_hand)

        # Minute hand
        minute_angle = (minutes + seconds / 60) * 6 - 90
        minute_hand = self.create_hand(minute_angle, self.radius * 0.7, 4, '#34495E')  # 較淺的藍灰色
        self.hands.append(minute_hand)

        # Second hand
        second_angle = (seconds + milliseconds) * 6 - 90
        second_hand = self.create_hand(second_angle, self.radius * 0.8, 2, '#E74C3C')  # 紅色
        self.hands.append(second_hand)

        # Center decorative circles
        # Outer circle
        center_dot_outer = self.create_oval(
            self.center_x-8, self.center_y-8,
            self.center_x+8, self.center_y+8,
            fill='#34495E', outline='#2C3E50'
        )
        # Inner circle
        center_dot_inner = self.create_oval(
            self.center_x-4, self.center_y-4,
            self.center_x+4, self.center_y+4,
            fill='#E74C3C', outline='#E74C3C'
        )
        self.hands.extend([center_dot_outer, center_dot_inner])

        # Update every 50ms for smoother second hand movement
        self.after(50, self.update_clock)

    def create_hand(self, angle, length, width, color):
        rad = math.radians(angle)
        x = self.center_x + length * math.cos(rad)
        y = self.center_y + length * math.sin(rad)
        return self.create_line(
            self.center_x, self.center_y, x, y,
            width=width, fill=color
        )

# Create main window
root = tk.Tk()
root.title("優雅時鐘")

# Set window size and position
window_size = 600  # 增加窗口大小以提高解析度
root.geometry(f"{window_size}x{window_size}")

# Create and pack the clock
clock = AnalogClock(root, width=window_size, height=window_size)
clock.pack(expand=True, fill='both', padx=20, pady=20)

# Configure window
root.configure(bg='#F0F0F0')  # 設置窗口背景色

# Start the application
root.mainloop()
