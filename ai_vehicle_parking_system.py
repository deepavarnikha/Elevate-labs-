
import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import datetime
import random

# Database Connection
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="vehicle_parking"
    )

# Initialize DB and create required tables
def init_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE,
        password VARCHAR(50)
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS parking_slots (
        slot_id INT PRIMARY KEY,
        is_occupied BOOLEAN DEFAULT FALSE
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vehicle_log (
        id INT AUTO_INCREMENT PRIMARY KEY,
        plate_number VARCHAR(20),
        entry_time DATETIME,
        slot_id INT,
        FOREIGN KEY (slot_id) REFERENCES parking_slots(slot_id)
    );
    """)
    # Populate parking slots if empty
    cursor.execute("SELECT COUNT(*) FROM parking_slots")
    if cursor.fetchone()[0] == 0:
        for i in range(1, 11):  # 10 parking slots
            cursor.execute("INSERT INTO parking_slots (slot_id) VALUES (%s)", (i,))
    conn.commit()
    conn.close()

# Simulated AI: Predict peak hour (based on random generation)
def predict_peak_hour():
    peak_hour = random.choice(["9 AM", "12 PM", "3 PM", "6 PM"])
    return peak_hour

# GUI Application
class ParkingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Vehicle Parking System")
        self.root.geometry("400x400")
        self.username = None

        self.login_screen()

    def login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Login", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text="Username").pack()
        self.login_user = tk.Entry(self.root)
        self.login_user.pack()
        tk.Label(self.root, text="Password").pack()
        self.login_pass = tk.Entry(self.root, show="*")
        self.login_pass.pack()
        tk.Button(self.root, text="Login", command=self.login).pack(pady=5)
        tk.Button(self.root, text="Register", command=self.register_screen).pack()

    def register_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Register", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text="Username").pack()
        self.reg_user = tk.Entry(self.root)
        self.reg_user.pack()
        tk.Label(self.root, text="Password").pack()
        self.reg_pass = tk.Entry(self.root, show="*")
        self.reg_pass.pack()
        tk.Button(self.root, text="Register", command=self.register).pack(pady=5)
        tk.Button(self.root, text="Back to Login", command=self.login_screen).pack()

    def dashboard(self):
        self.clear_screen()
        tk.Label(self.root, text=f"Welcome {self.username}", font=("Arial", 14)).pack(pady=10)
        tk.Button(self.root, text="Add Vehicle", command=self.add_vehicle).pack(pady=5)
        tk.Button(self.root, text="View Current Parking", command=self.view_parking).pack(pady=5)
        tk.Button(self.root, text="AI: Predict Peak Hour", command=self.show_prediction).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.login_screen).pack(pady=20)

    def add_vehicle(self):
        plate = f"KA-{random.randint(10,99)}-{random.randint(1000,9999)}"  # Simulated license
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT slot_id FROM parking_slots WHERE is_occupied = FALSE LIMIT 1")
        result = cursor.fetchone()
        if result:
            slot_id = result[0]
            cursor.execute("INSERT INTO vehicle_log (plate_number, entry_time, slot_id) VALUES (%s, %s, %s)",
                           (plate, datetime.now(), slot_id))
            cursor.execute("UPDATE parking_slots SET is_occupied = TRUE WHERE slot_id = %s", (slot_id,))
            conn.commit()
            messagebox.showinfo("Success", f"Vehicle {plate} added to Slot {slot_id}")
        else:
            messagebox.showwarning("Full", "No slots available!")
        conn.close()

    def view_parking(self):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT plate_number, entry_time, slot_id FROM vehicle_log ORDER BY entry_time DESC LIMIT 5")
        records = cursor.fetchall()
        conn.close()
        top = tk.Toplevel(self.root)
        top.title("Current Parking")
        for r in records:
            tk.Label(top, text=f"Plate: {r[0]}, Time: {r[1]}, Slot: {r[2]}").pack()

    def show_prediction(self):
        peak = predict_peak_hour()
        messagebox.showinfo("AI Prediction", f"Next Peak Hour Likely Around: {peak}")

    def login(self):
        user = self.login_user.get()
        pwd = self.login_pass.get()
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (user, pwd))
        if cursor.fetchone():
            self.username = user
            self.dashboard()
        else:
            messagebox.showerror("Error", "Invalid credentials")
        conn.close()

    def register(self):
        user = self.reg_user.get()
        pwd = self.reg_pass.get()
        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (user, pwd))
            conn.commit()
            messagebox.showinfo("Success", "User registered. Login now.")
            self.login_screen()
        except mysql.connector.errors.IntegrityError:
            messagebox.showerror("Error", "Username already exists")
        conn.close()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Run
if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = ParkingApp(root)
    root.mainloop()
