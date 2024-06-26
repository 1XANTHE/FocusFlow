import time
import tkinter as tk
from tkinter import messagebox, ttk
from plyer import notification
import threading

class PomodoroTimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        
        self.focus_duration = tk.StringVar(value="25")
        self.focus_unit = tk.StringVar(value="Minutes")
        self.break_duration = tk.StringVar(value="5")
        self.break_unit = tk.StringVar(value="Minutes")
        self.cycles = tk.StringVar(value="4")
        
        self.setup_ui()

      
        self.stop_flag = False

    def setup_ui(self):
        style = ttk.Style()
        style.configure("TButton", foreground="black", background="blue", font=('Berlin Sans FB', 15))
        
        self.title_label = tk.Label(self.root, text="Pomodoro Timer", font=('Algerian', 30, 'bold'), background="#f9f9f9")
        self.title_label.pack(pady=16)

        frame = tk.Frame(self.root)
        frame.pack(padx=20, pady=20)

        focus_frame = tk.Frame(frame)
        focus_frame.pack(pady=(0, 20))

        self.focus_label = tk.Label(focus_frame, text="Focus Duration:")
        self.focus_label.grid(row=0, column=0, padx=(0, 5))
        self.focus_entry = tk.Entry(focus_frame, textvariable=self.focus_duration, width=10, font=('Helvetica', 20))
        self.focus_entry.grid(row=0, column=1, padx=(0, 10))
        self.focus_unit_dropdown = ttk.Combobox(focus_frame, textvariable=self.focus_unit, values=["Seconds", "Minutes", "Hours"], width=8, font=('Helvetica', 15))
        self.focus_unit_dropdown.grid(row=0, column=2)

        break_frame = tk.Frame(frame)
        break_frame.pack(pady=(0, 10))

        self.break_label = tk.Label(break_frame, text="Break Duration:")
        self.break_label.grid(row=0, column=0, padx=(0, 5))
        self.break_entry = tk.Entry(break_frame, textvariable=self.break_duration, width=10, font=('Helvetica', 20))
        self.break_entry.grid(row=0, column=1, padx=(0, 10))
        self.break_unit_dropdown = ttk.Combobox(break_frame, textvariable=self.break_unit, values=["Seconds", "Minutes", "Hours"], width=8, font=('Helvetica', 15))
        self.break_unit_dropdown.grid(row=0, column=2)

        self.cycles_label = tk.Label(frame, text="Number of Cycles:")
        self.cycles_label.pack(pady=(0, 5))
        self.cycles_entry = tk.Entry(frame, textvariable=self.cycles, width=10, font=('Helvetica', 15))
        self.cycles_entry.pack(pady=(0, 10))

        buttons_frame = tk.Frame(frame)
        buttons_frame.pack()

        self.start_button = ttk.Button(buttons_frame, text="Start", command=self.start_timer)
        self.start_button.grid(row=0, column=0, padx=(0, 5))

        self.stop_button = ttk.Button(buttons_frame, text="Stop", command=self.stop_timer)
        self.stop_button.grid(row=0, column=1)

    def notify(self, title, message):
        notification.notify(
            title=title,
            message=message,
            app_icon=None,
            timeout=10
        )

    def convert_to_seconds(self, duration, unit):
        if unit == "Seconds":
            return duration
        elif unit == "Minutes":
            return duration * 60
        elif unit == "Hours":
            return duration * 3600

    def pomodoro_timer(self, duration, unit, cycles):
        total_seconds = self.convert_to_seconds(duration, unit)
        for i in range(cycles):
            if self.stop_flag:
                break
            self.notify("Pomodoro - Focus Time", f"Stay focused for {duration} {unit}!")
            time.sleep(total_seconds)
            if self.stop_flag:
                break
            self.notify("Pomodoro - Break Time", f"Take a break!")
            time.sleep(5)  
        if not self.stop_flag:
            messagebox.showinfo("Pomodoro Timer", "Pomodoro completed!")
        else:
            messagebox.showinfo("Pomodoro Timer", "Thank you for using Pomodoro!")

    def start_timer(self):
        focus_duration = int(self.focus_duration.get())
        focus_unit = self.focus_unit.get()
        break_duration = int(self.break_duration.get())
        break_unit = self.break_unit.get()
        cycles = int(self.cycles.get())

       
        self.stop_flag = False
        threading.Thread(target=self.pomodoro_timer, args=(focus_duration, focus_unit, cycles)).start()
        messagebox.showinfo("Pomodoro Timer", "Timer started!")

    def stop_timer(self):
        self.stop_flag = True
        messagebox.showinfo("Pomodoro Timer", "Timer stopped!")

def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    root.geometry(f"{width}x{height}+{x}+{y}")

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#f9f9f9")  
    app = PomodoroTimerApp(root)
    center_window(root, 500, 500)  
    root.mainloop()
