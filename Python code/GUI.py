import tkinter as tk
from tkinter.simpledialog import askinteger
import csv
from datetime import datetime

class CarPark:
    def __init__(self, root):
        self.root = root
        self.root.title("Car Park")
        
        self.rows = askinteger("Car Park", "Enter the number of rows:", minvalue=1, maxvalue=20)
        self.cols = askinteger("Car Park", "Enter the number of columns:", minvalue=1, maxvalue=20)
        
        self.car_park = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.buttons = []  
        
        for i in range(self.rows):
            row_buttons = []
            for j in range(self.cols):
                button = tk.Button(self.root, text=f"Space {i * self.cols + j + 1}", width=10, height=3, 
                                   font=("Arial", 12), bg="green", command=lambda i=i, j=j: self.toggle_space(i, j))
                button.grid(row=i, column=j, padx=5, pady=5)
                row_buttons.append(button)
            self.buttons.append(row_buttons)
        
        self.update_gui()

    def log_activity(self, action, slot):
        with open("ActivityLog.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%H:%M:%S"), action, f"Slot {slot}"])

    def toggle_space(self, row, col):
        slot_number = row * self.cols + col + 1
        if self.car_park[row][col]:
            self.car_park[row][col] = None  
            self.buttons[row][col].config(bg="green", text=f"Space {slot_number}")
            self.log_activity("Exit", slot_number)
        else:
            self.car_park[row][col] = "Occupied"  
            self.buttons[row][col].config(bg="red", text=f"Occupied")
            self.log_activity("Entry", slot_number)
        self.update_gui()

    def update_gui(self):
        for i in range(self.rows):
            for j in range(self.cols):
                slot_number = i * self.cols + j + 1
                if self.car_park[i][j] is None:
                    self.buttons[i][j].config(bg="green", text=f"Space {slot_number}")
                else:
                    self.buttons[i][j].config(bg="red", text="Occupied")
        self.root.after(1000, self.update_gui)

root = tk.Tk()
car_park = CarPark(root)
root.mainloop()
