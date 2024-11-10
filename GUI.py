import tkinter as tk
import math

def change_rpm():
    global rpm
    if rpm_entry.get() != "":
        rpm = rpm_entry.get()
    rpm_label.config(text=f"RPM: {rpm}") 

def increment_rpm():
    global rpm
    rpm += 1
    rpm_label.config(text=f"RPM: {rpm}") 

def decrement_rpm():
    global rpm
    rpm -= 1
    rpm_label.config(text=f"RPM: {rpm}") 

def toggle_direction():
    if direction:
        toggle_label.config(text="ON", fg="green")
    else:
        toggle_label.config(text="OFF", fg="red")


root = tk.Tk()
root.title("Snowfall Symphony")
root.geometry("500x500")

rpm = 100
direction = 0 # 0 is cw, 1 is ccw



rpm_label = tk.Label(root, text=f"RPM: {rpm}")
rpm_label.grid(row=0, column=0, padx=10, pady=10)

rpm_entry = tk.Entry(root)
rpm_entry.grid(row=0, column=1, padx=10, pady=10)

set_button = tk.Button(root, text="Set RPM", command=change_rpm)
set_button.grid(row=0, column=2, padx=10, pady=10)

increment_button = tk.Button(root, text="+", command=increment_rpm)
increment_button.grid(row=1, column=0, padx=10, pady=10)

decrement_button = tk.Button(root, text="-", command=decrement_rpm)
decrement_button.grid(row=2, column=0, padx=10, pady=10)

direction_toggle = tk.Checkbutton(
    root, text="Toggle", command=toggle_direction,
    onvalue=True, offvalue=False, width=6, height=2, indicatoron=False
)
direction_toggle.grid(row=3, column=0, padx=10, pady=10)

root.mainloop()

print(rpm)