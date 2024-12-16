import tkinter as tk
import math
from time import sleep
import time
import threading
import RPi.GPIO as GPIO

# gate servos that release marbles individually
class release_servo():

    def __init__(self, pin, number, closed_angle, open_angle):
        self.pin = pin # GPIO pin
        self.number = number # the ordering of the servo (for each note)

        self.closed_angle = closed_angle # gate closed
        self.open_angle = open_angle # gate open

        # convert to duty cycle
        self.closed_dc = (closed_angle+2)/20
        self.open_dc = (open_angle+2)/20

        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 50)
        self.pwm.start(self.closed_dc)
        sleep(0.5)

    def release_marble(self):
        # open gate then close it again
        self.pwm.ChangeDutyCycle(self.closed_dc)
        sleep(0.5)
        self.pwm.ChangeDutyCycle(self.open_dc)
        sleep(0.5)
        self.pwm.ChangeDutyCycle(self.closed_dc)
        sleep(0.5)

    def play_note(self, delay):
        threading.Thread(target=self._play_note_worker, args=(delay,), daemon=True).start()

    def _play_note_worker(self, delay):
        # Worker method to handle play_note logic
        self.release_marble()
        sleep(delay)

    def stop(self):
        self.pwm.stop()

# range finder to detect when marble passes
class range_finder():

    def __init__(self, trigger_pin, echo_pin, selector_servo):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        self.selector_servo = selector_servo # selector servo that listens for when range finder goes off
        self.running = False

        GPIO.setup(self.trigger_pin, GPIO.OUT) 
        GPIO.setup(self.echo_pin, GPIO.IN) 

        GPIO.output(self.trigger_pin, 0)

    def pulse_trigger(self):
        GPIO.output(self.trigger_pin, 1)
        sleep(10 * 10**(-6))
        GPIO.output(self.trigger_pin, 0)

    def detect_marble(self):
        self.pulse_trigger()
        start_time = 0
        end_time = 0

        while GPIO.input(self.echo_pin) == 0:
            start_time = time.time()
        while GPIO.input(self.echo_pin) == 1:
            end_time = time.time()


        duration = end_time - start_time # in seconds
        duration = duration * 10**(6)
        distance_cm = duration/58

        # if marble was detected
        if distance_cm > 2 and distance_cm < 8:
            print(distance_cm)
            return True

        return False

    def loop(self):
        while self.running:
            if self.detect_marble():
                self.selector_servo.change_track()
            sleep(0.01)

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread.is_alive():
            self.thread.join()

# servo to change marble track
class selector_servo():

    def __init__(self, pin, max_tracks=4):
        self.pin = pin
        self.max_tracks = max_tracks
        self.cur_track = 0

        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 50)
        self.pwm.start(0)

    def change_track(self):
        threading.Thread(target=self._change_track_worker).start()

    def _change_track_worker(self):
        initial = 0
        self.cur_track = (self.cur_track + 1) % self.max_tracks

        # initially change anlge for each gate to fill all gates with some supply
        # then change to filling gates that were recently played
        if initial < 5:
            angle = 30 + 30*self.cur_track
            angle_to_dc = (angle*11)/297 + 2

            self.pwm = GPIO.PWM(self.pin, 50)

            self.pwm.ChangeDutyCycle(angle_to_dc)
            initial += 1
        else:
            angle = 30 + 30*self.number
            angle_to_dc = (angle*11)/297 + 2
            self.pwm.ChangeDutyCycle(angle_to_dc)
            sleep(1)

            offshoot_track_angle = 180
            angle_to_dc = (offshoot_track_angle*11)/297 + 2
            self.pwm.ChangeDutyCycle(angle_to_dc)
            sleep(1)

    def stop(self):
        self.pwm.stop()


# main dc motor driving windmill and archimedes screw
class motor():

    def __init__(self, pin1, pin2, rpm=0):
        # pin1, pin2 control hbridge
        self.pin1 = pin1
        self.pin2 = pin2
        self.rpm = rpm

        GPIO.setup(self.pin1, GPIO.OUT)
        GPIO.setup(self.pin2, GPIO.OUT)

        GPIO.output(self.pin1, 0)
        GPIO.output(self.pin2, 0)

    def change_rpm(self, new_rpm):
        old_rpm = self.rpm
        self.rpm = int(new_rpm)

        # changed from cw to ccw
        if self.rpm < 0 and old_rpm >= 0:
            GPIO.output(self.pin1, 1)
            GPIO.output(self.pin2, 0)

        # changed from ccw to cw
        if self.rpm > 0 and old_rpm < 0:
            GPIO.output(self.pin1, 0)
            GPIO.output(self.pin2, 1)

# the GUI elements hat show the windmill spinning
class gui_blades():
    def __init__(self, root, motor):
        self.root = root
        self.angle = 0
        self.motor = motor

        # Create a canvas
        self.canvas = tk.Canvas(root, width=300, height=300, bg="white")
        self.canvas.grid(row=0, column=19, padx=20, pady=20)

        # Create a rect
        self.canvas.create_rectangle(130, 120, 170, 300, fill="brown", tags="trunk")

        triangle_coords = [80, 250, 150, 50, 220, 250]
        self.canvas.create_polygon(triangle_coords, fill="green", outline="black", width=2)

        self.canvas.create_oval(125, 125, 175, 175, fill='brown', tags='circle')


        # Start the animation
        self.update_rectangle()

    def rotate_rectangle(self, angle):
        # Define the center of the canvas
        center_x, center_y = 150, 150

        # Coordinates for a centered rectangle before rotation
        width, height = 150, 20
        rect_coords = [
            (center_x - width / 2, center_y - height / 2),
            (center_x + width / 2, center_y - height / 2),
            (center_x + width / 2, center_y + height / 2),
            (center_x - width / 2, center_y + height / 2)
        ]

        # Rotate the rectangle coordinates
        rotated_coords = []
        for (x, y) in rect_coords:
            new_x = center_x + (x - center_x) * math.cos(math.radians(angle)) - (y - center_y) * math.sin(math.radians(angle))
            new_y = center_y + (x - center_x) * math.sin(math.radians(angle)) + (y - center_y) * math.cos(math.radians(angle))
            rotated_coords.append((new_x, new_y))

        return rotated_coords

    def update_rectangle(self):
        self.angle += motor.rpm * 0.1
        
        # Delete only the rectangles (not the circle)
        self.canvas.delete("blade")  # Delete elements tagged as "rect"

        # Draw the two rectangles forming the "X"
        rect1_coords = self.rotate_rectangle(self.angle)
        rect2_coords = self.rotate_rectangle(self.angle + 90)  # Rotate second rectangle by 90 degrees to form X

        self.canvas.create_polygon(rect1_coords, fill="blue", outline="black", tags="blade")
        self.canvas.create_polygon(rect2_coords, fill="red", outline="black", tags="blade")

        # Update the canvas after 50ms (for smooth animation)
        self.root.after(50, self.update_rectangle)



# ---------------------------------------
# begin class main
# --------------------------------------

# draw the RPM slider gui element
def draw_slider(root, motor):
    def update_motor_rpm(value):
        motor.change_rpm(int(slider.get()))

    rotation_speed = tk.DoubleVar(value=2)
    slider = tk.Scale(root, length=300, from_=-100, to=100, orient="horizontal", label="Adjust RPM", background='lightblue', command=update_motor_rpm)
    slider.grid(row=1, column=0, columnspan=2, pady=10)
    angle = 0

# draw the note selector
def draw_piano(root):
    piano_grid = tk.Frame(root, bg="black", bd=20)
    piano_grid.grid(row=0, column=0, padx=20)

    key_c = tk.Button(piano_grid, height=8, width=4, bd=4, text="C", bg="red", fg="black", command=lambda: ss())
    key_c.grid(row=0, column=0, padx=1, pady=1)

    key_d = tk.Button(piano_grid, height=8, width=4, bd=4, text="D", bg="orange", fg="black", command=lambda: ss())
    key_d.grid(row=0, column=1, padx=1, pady=1)

    key_e = tk.Button(piano_grid, height=8, width=4, bd=4, text="E", bg="yellow", fg="black", command=lambda: ss())
    key_e.grid(row=0, column=2, padx=1, pady=1)

    key_f = tk.Button(piano_grid, height=8, width=4, bd=4, text="F", bg="green", fg="black", command=lambda: ss())
    key_f.grid(row=0, column=3, padx=1, pady=1)

    key_g = tk.Button(piano_grid, height=8, width=4, bd=4, text="G", bg="cyan", fg="black", command=lambda: ss())
    key_g.grid(row=0, column=4, padx=1, pady=1)


if __name__ == "__main__":

    GPIO.setmode(GPIO.BCM)
    root = tk.Tk()
    root.title("Snowfall Symphony")
    root.geometry("1000x600")

    bg = tk.PhotoImage(file = "winter.png")

    background = tk.Label(root, image=bg)
    background.grid(row=0,column=0)

    frame = tk.Frame(root, bg='lightblue')
    frame.grid(row=0,column=0)

    servo_c = release_servo(27, 5, 110, 0)
    servo_d = release_servo(17, 4, 0, 90)
    servo_e = release_servo(4, 3, 0, 120)
    servo_f = release_servo(3, 2, 0, 90)
    servo_g = release_servo(2, 1, 0, 90)

    ss = selector_servo(26)
    rf = range_finder(5, 6, ss)

    motor = motor(0, 7, 8)

    blade = gui_blades(frame, motor)
    draw_piano(frame)
    draw_slider(frame, motor)

    rf.start()

    root.mainloop()


    servo.stop()
    rf.stop()
    GPIO.cleanup()