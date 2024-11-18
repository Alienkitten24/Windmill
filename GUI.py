import tkinter as tk
import math
from enum import Enum

class direction_enum(Enum):
    CLOCKWISE = 0
    COUNTERCLOCKWISE = 1

def change_rpm(new_rpm):
    global rpm
    global direction

    if rpm_entry.get() != "":
        rpm = int(rpm_entry.get())
    rpm_label.config(text=f"RPM: {rpm}") 

    if rpm < 0:
        rpm = abs(rpm)
        direction = direction_enum.COUNTERCLOCKWISE
    if rpm > 0:
        direction = direction_enum.CLOCKWISE


def toggle_direction():
    global direction
    direction = not direction

    if direction:
        toggle_label.config(text="COUNTERCLOCKWISE", fg="green")
    else:
        toggle_label.config(text="CLOCKWISE", fg="red")


root = tk.Tk()
root.title("Snowfall Symphony")
root.geometry("500x500")

rpm = 100
direction = direction_enum.CLOCKWISE


rpm_label = tk.Label(root, text=f"RPM: {rpm}")
rpm_label.grid(row=0, column=0, padx=10, pady=10)

# TODO change to SpinBox
rpm_entry = tk.Entry(root)
rpm_entry.grid(row=0, column=1, padx=10, pady=10)

set_button = tk.Button(root, text="Set RPM",
                       command=lambda: change_rpm(int(rpm_entry.get()) if rpm_entry.get() != "" else rpm))
set_button.grid(row=0, column=2, padx=10, pady=10)

direction_toggle = tk.Checkbutton(
    root, text="CW / CCW", command=toggle_direction,
    onvalue=True, offvalue=False, width=8, height=2, indicatoron=False
)
direction_toggle.grid(row=3, column=0, padx=10, pady=10)

toggle_label = tk.Label(root, text="CLOCKWISE", fg="RED")
toggle_label.grid(row=3, column=1, padx=10, pady=10)

def test():
    print("Note Pressed")

def test2():
    key_c.config(relief="sunken")
    test()
    root.after(150, lambda: key_c.config(relief="raised"))

piano_grid = tk.Frame(root, bg="black", bd=20)
piano_grid.grid(row=4, column=0, columnspan=3)

key_c = tk.Button(piano_grid, height=10, width=6, bd=4, text="C", bg="white", fg="black", command=test)
key_c.grid(row=0, column=0, padx=1, pady=1)
root.bind("1", lambda event: test2())
label_c = tk.Label(piano_grid, width=6, bd=4, text="1", bg="white", fg="black")
label_c.grid(row=1, column=0, padx=1, pady=1)

key_d = tk.Button(piano_grid, height=10, width=6, bd=4, text="D", bg="white", fg="black")
key_d.grid(row=0, column=1, padx=1, pady=1)
label_d = tk.Label(piano_grid, width=6, bd=4, text="2", bg="white", fg="black")
label_d.grid(row=1, column=1, padx=1, pady=1)

key_e = tk.Button(piano_grid, height=10, width=6, bd=4, text="E", bg="white", fg="black")
key_e.grid(row=0, column=2, padx=1, pady=1)
label_e = tk.Label(piano_grid, width=6, bd=4, text="3", bg="white", fg="black")
label_e.grid(row=1, column=2, padx=1, pady=1)

key_f = tk.Button(piano_grid, height=10, width=6, bd=4, text="F", bg="white", fg="black")
key_f.grid(row=0, column=3, padx=1, pady=1)
label_f = tk.Label(piano_grid, width=6, bd=4, text="4", bg="white", fg="black")
label_f.grid(row=1, column=3, padx=1, pady=1)

key_g = tk.Button(piano_grid, height=10, width=6, bd=4, text="G", bg="white", fg="black")
key_g.grid(row=0, column=4, padx=1, pady=1)
label_g = tk.Label(piano_grid, width=6, bd=4, text="5", bg="white", fg="black")
label_g.grid(row=1, column=4, padx=1, pady=1)

key_a = tk.Button(piano_grid, height=10, width=6, bd=4, text="A", bg="white", fg="black")
key_a.grid(row=0, column=5, padx=1, pady=1)
label_a = tk.Label(piano_grid, width=6, bd=4, text="6", bg="white", fg="black")
label_a.grid(row=1, column=5, padx=1, pady=1)

key_b = tk.Button(piano_grid, height=10, width=6, bd=4, text="B", bg="white", fg="black")
key_b.grid(row=0, column=6, padx=1, pady=1)
label_b = tk.Label(piano_grid, width=6, bd=4, text="7", bg="white", fg="black")
label_b.grid(row=1, column=6, padx=1, pady=1)

slider = tk.Scale(root, length=300, from_=-100, to=100, orient="horizontal", label="Adjust RPM", command=lambda p: print(slider.get()))
slider.grid(row=7, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()

print(rpm)