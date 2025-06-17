import tkinter as tk
from tkinter import ttk
import os
import PIL.Image, PIL.ImageTk
import cv2 as cv
import cam
import model
import sqlite3
from datetime import date
from datetime import datetime

class App:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title = "Bicep Rep Counter"

        self.window.geometry("800x600")  # Default size
        self.window.resizable(True, True)  # Allow resizing

        self.running = True  # Add a flag to track if the app is running

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.create_database()

        self.counters = [1, 1]
        self.rep_counter = 0

        self.extended = False
        self.contracted = False

        self.stopwatch_running = False
        self.elapsed_time = 0
        self.minutes = 0

        self.last_prediction = 0

        self.model = model.Model()

        self.counting_enabled = False

        self.finished = False

        self.camera = cam.Camera()

        self.init_gui()

        self.delay = 15
        self.update()

        self.window.attributes("-topmost", True)
        self.window.mainloop()

    def create_database(self):
        connection = sqlite3.connect('fit.db')
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                workout_num INTEGER NOT NULL,
                exercise TEXT NOT NULL,
                sets INTEGER NOT NULL,
                reps INTEGER NOT NULL,
                date DATE
            )
        """)
        connection.commit()
        connection.close()
        print("Workout table created")

    """def init_gui(self):
        self.canvas = tk.Canvas(self.window, width=self.camera.width, height=self.camera.height)
        self.canvas.pack()

        frame = tk.Frame(self.window)
        frame.pack(anchor=tk.CENTER, expand=True)

        self.btn_toggleauto = tk.Button(frame, text="Toggle Counting", width=20, command=self.counting_toggle)
        self.btn_toggleauto.grid(row=0, column=0, padx=5, pady=5)

        self.btn_class_one = tk.Button(frame, text="Extended", width=20, command=lambda: self.save_for_class(1))
        self.btn_class_one.grid(row=0, column=1, padx=5, pady=5)

        self.btn_class_two = tk.Button(frame, text="Contracted", width=20, command=lambda: self.save_for_class(2))
        self.btn_class_two.grid(row=0, column=2, padx=5, pady=5)

        self.btn_train = tk.Button(frame, text="Train Model", width=20, command=lambda: self.model.train_model(self.counters))
        self.btn_train.grid(row=1, column=0, padx=5, pady=5)

        self.btn_reset = tk.Button(frame, text="Reset", width=20, command=self.reset)
        self.btn_reset.grid(row=1, column=1, padx=5, pady=5)

        self.counter_label = tk.Label(frame, text=f'{self.rep_counter}', font=('Arial', 24))
        self.counter_label.grid(row=1, column=2, padx=5, pady=5)

        user_input_frame = tk.Frame(self.window)
        user_input_frame.pack(anchor=tk.CENTER, expand=True)

        self.user_input_label = tk.Label(user_input_frame, text="Exercise Name:", font=('Arial', 12))
        self.user_input_label.grid(row=0, column=0, padx=5, pady=5)

        self.user_input_entry = tk.Entry(user_input_frame, width=20)
        self.user_input_entry.grid(row=0, column=1, padx=5, pady=5)

        self.date_label = tk.Label(user_input_frame, text="Sets:", font=('Arial', 12))
        self.date_label.grid(row=1, column=0, padx=5, pady=5)

        self.date_entry = tk.Entry(user_input_frame, width=20)
        self.date_entry.grid(row=1, column=1, padx=5, pady=5)

        self.reps_label = tk.Label(user_input_frame, text="Reps:", font=('Arial', 12))
        self.reps_label.grid(row=2, column=0, padx=5, pady=5)

        self.reps_entry = tk.Entry(user_input_frame, width=20)
        self.reps_entry.grid(row=2, column=1, padx=5, pady=5)

        self.work_num = tk.Label(user_input_frame, text="Workout Date:", font=('Arial', 12))
        self.work_num.grid(row=3, column=0, padx=5, pady=5)

        self.work_entry = tk.Entry(user_input_frame, width=20)
        self.work_entry.grid(row=3, column=1, padx=5, pady=5)

        self.log_button = tk.Button(user_input_frame, text="Log Exercise", width=20, command=self.log_exercise)
        self.log_button.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

        self.finish_btn = tk.Button(user_input_frame, text='Finish Workout', width=20, command=self.update_state)
        self.finish_btn.grid(row=3, column=1, columnspan=3, padx=5, pady=5)

        self.history_button = tk.Button(user_input_frame, text="View Workout", width=20, command=self.view_workout)
        self.history_button.grid(row=4, column=0, columnspan=3, padx=5, pady=5)"""

    def init_gui(self):

        # Scrollable canvas for overflow handling
        main_frame = tk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Canvas for camera display
        self.canvas = tk.Canvas(scrollable_frame, width=400, height=300, bg="gray")
        self.canvas.pack(pady=10)

        # Button Frame
        frame = tk.Frame(scrollable_frame)
        frame.pack(anchor=tk.CENTER, expand=True, pady=10)

        # Buttons in a grid layout
        self.btn_toggleauto = tk.Button(frame, text="Toggle Counting", width=20, command=self.counting_toggle)
        self.btn_toggleauto.grid(row=0, column=0, padx=5, pady=5)

        self.btn_class_one = tk.Button(frame, text="Extended", width=20, command=lambda: self.save_for_class(1))
        self.btn_class_one.grid(row=0, column=1, padx=5, pady=5)

        self.btn_class_two = tk.Button(frame, text="Contracted", width=20, command=lambda: self.save_for_class(2))
        self.btn_class_two.grid(row=0, column=2, padx=5, pady=5)

        self.btn_train = tk.Button(frame, text="Train Model", width=20, command=lambda: self.model.train_model(self.counters))
        self.btn_train.grid(row=1, column=0, padx=5, pady=5)

        self.btn_reset = tk.Button(frame, text="Reset", width=20, command=self.reset)
        self.btn_reset.grid(row=1, column=1, padx=5, pady=5)

        self.counter_label = tk.Label(frame, text='0', font=('Arial', 24))
        self.counter_label.grid(row=1, column=2, padx=5, pady=5)

        # User Input Frame
        user_input_frame = tk.Frame(scrollable_frame)
        user_input_frame.pack(anchor=tk.CENTER, expand=True)

        # Input fields and labels
        labels_and_entries = [
            ("Exercise Name:", "entry_exercise"),
            ("Sets:", "entry_sets"),
            ("Reps:", "entry_reps"),
            ("Workout Completion Date:", "entry_workout_date"),
        ]

        for i, (label_text, entry_var) in enumerate(labels_and_entries):
            label = tk.Label(user_input_frame, text=label_text, font=('Arial', 12))
            label.grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(user_input_frame)
            entry.grid(row=i, column=1, padx=5, pady=5)
            setattr(self, entry_var, entry)  # Dynamically create attributes for entries

        self.log_button = tk.Button(user_input_frame, text="Log Exercise", width=20, command=self.log_exercise)
        self.log_button.grid(row=len(labels_and_entries), columnspan=2, pady=(10, 5))

        self.finish_btn = tk.Button(user_input_frame, text='Finish Workout', width=20, command=self.update_state)
        self.finish_btn.grid(row=len(labels_and_entries) + 1 , columnspan=2 ,pady=(10))

        self.history_button = tk.Button(user_input_frame, text="View Workout", width=20, command=self.view_workout)
        self.history_button.grid(row=len(labels_and_entries) + 2, columnspan=2, pady=(10, 5))

        self.timer_label = tk.Label(self.window, text="Time: 0:00", font=('Arial', 16))
        self.timer_label.pack(pady=10)

        # Stopwatch Buttons
        stopwatch_frame = tk.Frame(self.window)
        stopwatch_frame.pack(pady=10)

        self.start_timer_button = tk.Button(stopwatch_frame, text="Start Stopwatch", width=15, command=self.start_timer)
        self.start_timer_button.grid(row=0, column=0, padx=5)

        self.reset_timer_button = tk.Button(stopwatch_frame, text="Reset Stopwatch", width=15, command=self.reset_timer)
        self.reset_timer_button.grid(row=0, column=1, padx=5)


    def update_state(self):
        self.finished = True

    def start_timer(self):
        # Start rest timer
        if not self.stopwatch_running:
            self.stopwatch_running = True
            self.update_stopwatch()

    def reset_timer(self):
        # Reset rest timer
        self.stopwatch_running = False
        self.elapsed_time = 0
        self.timer_label.config(text="Time: 0:00")

    def update_stopwatch(self):
        """Update the stopwatch every second."""
        if self.stopwatch_running:
            # Calculate minutes and seconds from elapsed time
            minutes = self.elapsed_time // 60
            seconds = self.elapsed_time % 60

            # Update the timer label with the formatted time
            self.timer_label.config(text=f"{minutes}:{seconds:02d}")  # Format seconds as two digits

            # Increment elapsed time
            self.elapsed_time += 1

            # Schedule the next update
            self.window.after(1000, self.update_stopwatch)

    def view_workout(self):
        dat = self.entry_workout_date.get()  # Example: "2025-04-12"

        try:
            # Convert the string to a datetime object
            date_object = datetime.strptime(dat, '%Y-%m-%d')  # Adjust format if needed
            
            dat = date_object.date()
            print(dat)  
        except ValueError:
            print("Invalid date format. Please enter the date in 'YYYY-MM-DD' format.")
        connection = sqlite3.connect('fit.db')
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM history WHERE date=?", (dat,))

        exercises = cursor.fetchall()
        connection.close()

        if len(exercises) == 0:
            print('None')

        for exercise in exercises:
            print(f"Exercise: {exercise[2]}, Sets: {exercise[1]}, Reps: {exercise[3]}")

    def log_exercise(self):
        exercise = self.entry_exercise.get()
        sets = self.entry_sets.get()
        reps = self.entry_reps.get()

        # Validate the input
        if not exercise or not sets or not reps:
            print("Please fill in all fields.")
            return

        try:
            sets = int(sets)
            reps = int(reps)
        except ValueError:
            print("Sets and reps must be integers.")
            return
        
        connection = sqlite3.connect('fit.db')
        cursor = connection.cursor()

        dat = date.today()

        cursor.execute("SELECT workout_num FROM history ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()

        workout_num = 1
        if result is not None:
            workout_num = result[0]
            if self.finished:
                workout_num += 1
                self.finished = False

        cursor.execute(f"INSERT INTO history (workout_num, exercise, sets, reps, date) VALUES (?, ?, ?, ?, ?)", (workout_num, exercise, sets, reps, dat))
        connection.commit()
        connection.close()
        print(f"{sets} of {reps} reps of {exercise} logged in workout {workout_num}")

    def on_closing(self):
        self.running = False  # Stop the update loop
        self.window.destroy() 
    
    def update(self):
        if not self.running:  # Stop the update loop if the app is not running
            return

        if self.counting_enabled:
            self.predict()

        if self.extended and self.contracted:
            self.extended, self.contracted = False, False
            self.rep_counter += 1

        # Safely update the counter label
        if self.counter_label.winfo_exists():  # Check if the widget still exists
            self.counter_label.config(text=f"{self.rep_counter}")

        ret, frame = self.camera.get_frame()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            if self.canvas.winfo_exists():  # Check if the canvas still exists
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(self.delay, self.update)

    def predict(self):
        frame = self.camera.get_frame()
        prediction = self.model.predict(frame)
        
        if prediction != self.last_prediction:
            if prediction == 1:
                self.extended = True
                self.last_prediction = 1
            if prediction == 2:
                self.contracted = True
                self.last_prediction = 2

    def counting_toggle(self):
        self.counting_enabled = not self.counting_enabled

    def save_for_class(self, class_num):
        ret, frame = self.camera.get_frame()
        if not os.path.exists('1'):
            os.mkdir('1')
        if not os.path.exists('2'):
            os.mkdir('2')

        cv.imwrite(f"{class_num}/frame{self.counters[class_num-1]}.jpg", cv.cvtColor(frame, cv.COLOR_RGB2GRAY))

        img = PIL.Image.open(f"{class_num}/frame{self.counters[class_num-1]}.jpg")
        img.thumbnail((150, 150), PIL.Image.LANCZOS)
        img.save(f"{class_num}/frame{self.counters[class_num-1]}.jpg")

        self.counters[class_num-1] += 1

        print('Class Saved')

    def reset(self):
        self.rep_counter = 0

App()