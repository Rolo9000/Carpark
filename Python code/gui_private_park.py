import tkinter as tk
from tkinter.simpledialog import askinteger
import csv
from datetime import datetime

class CarPark:
    #This initialises the car park by modelling it as a grid with rows and columns. It prompts the user to input the number of rows and columns. Free spaces are green. The GUI updates as cars enter / leave.
    def __init__(self, root):
        self.root = root
        self.root.title("Car Park")
        
        self.rows = askinteger("Car Park", "Enter number of rows:", minvalue = 1, maxvalue = 20)
        self.cols = askinteger("Car Park", "Enter number of columns:", minvalue = 1, maxvalue = 20)
        
        self.car_park = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.buttons = []  
        
        for i in range(self.rows):
            row_buttons = []
            for j in range(self.cols):
                button = tk.Button(self.root, text = f"Space {i * self.cols + j + 1}", width = 10, height = 3, 
                                   font = ("Arial", 12), bg = "green", command = lambda i = i, j = j: self.toggle_space(i, j))
                button.grid(row = i, column = j, padx = 5, pady = 5)
                row_buttons.append(button)
            self.buttons.append(row_buttons)
        
        with open("activity_log.csv", mode = "a", newline = "") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Time", "Action", "Space", "Number Plate", "Registration Status"]) #These are the attributes
        
        self.update_gui()

#Reads the number plate of the most recent car that entered
    def read_last_number_plate(self):
        try:
            with open("last_number_plate.txt", "r") as file:
                return file.read().strip()
        except FileNotFoundError:
            return "Error"

#Reads whether or not the car is registered. If it is not, then the gate would not open.
    def read_registration_status(self):
        try:
            with open("is_last_num_plate_registered.txt", "r") as file:
                return file.read().strip()
        except FileNotFoundError:
            return "Error"

##Logs activity on a CSV file. Writes to a flat-file database with the following attributes: Date, Time, Entry / Exit, Space, Number plate, Registration status.
    def log_activity(self, action, space):
        number_plate = self.read_last_number_plate()
        registration_status = self.read_registration_status()
        
        with open("activity_log.csv", mode = "a", newline = "") as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now().strftime("%Y-%m-%d"),
                             datetime.now().strftime("%H:%M:%S"),
                             action, f"Space {space}",
                             number_plate, registration_status])

#The following two subroutines work together to constantly refresh and update the GUI. If a user selects a free space, the space becomes occupied and the colour changes to red. This is marked as an entry. If the user selects an occupied space, the space becomes free and the colour changes back to green. This is marked as an exit.
    def toggle_space(self, row, col):
        space_number = row * self.cols + col + 1
        if self.car_park[row][col]:
            self.car_park[row][col] = None  
            self.buttons[row][col].config(bg = "green", text = f"Space {space_number}")
            self.log_activity("Exit", space_number)
        else:
            self.car_park[row][col] = "Occupied"  
            self.buttons[row][col].config(bg = "red", text = "Occupied")
            self.log_activity("Entry", space_number)
        self.update_gui()

    def update_gui(self):
        for i in range(self.rows):
            for j in range(self.cols):
                space_number = i * self.cols + j + 1
                if self.car_park[i][j] is None:
                    self.buttons[i][j].config(bg = "green", text = f"Space {space_number}")
                else:
                    self.buttons[i][j].config(bg = "red", text = "Occupied")
        self.root.after(1000, self.update_gui)

#Create main window
root = tk.Tk()
car_park = CarPark(root)
root.mainloop()
