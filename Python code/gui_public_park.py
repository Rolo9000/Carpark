import tkinter as tk
from tkinter.simpledialog import askinteger, askstring
import csv
from datetime import datetime

class CarPark:
    #This initialises the car park by modelling it as a grid with rows and columns. It prompts the user to input the number of rows and columns. Free spaces are green. The GUI updates as cars enter / leave.
    def __init__(self, root):
        self.root = root
        self.root.title("Car Park")
        
        self.rows = askinteger("Car Park", "Enter the number of rows:", minvalue = 1, maxvalue = 20)
        self.cols = askinteger("Car Park", "Enter the number of columns:", minvalue = 1, maxvalue = 20)
        
        self.car_park = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.occupied_plates = set()
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
            writer.writerow(["Date", "Time", "Action", "Space", "Number Plate"]) #These are the attributes
        
        self.update_gui()

#Logs activity on a CSV file. Writes to a flat-file database with the following attributes: Date, Time, Entry / Exit, Space, Number plate.
    def log_activity(self, action, space, number_plate):
        with open("activity_log.csv", mode = "a", newline = "") as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%H:%M:%S"), action, f"Space {space}", number_plate])

#The following two subroutines work together to constantly refresh and update the GUI. If a user selects a free space, the space becomes occupied and the colour changes to red. This is marked as an entry. If the user selects an occupied space, the space becomes free and the colour changes back to green. This is marked as an exit.
    def toggle_space(self, row, col):
        space_number = row * self.cols + col + 1
        if self.car_park[row][col]:
            number_plate = self.car_park[row][col]
            self.car_park[row][col] = None  
            self.occupied_plates.remove(number_plate)
            self.buttons[row][col].config(bg = "green", text = f"Space {space_number}")
            self.log_activity("Exit", space_number, number_plate)
        else:
            while True:
                number_plate = askstring("Car Entry", "Enter vehicle number plate:")
                if not number_plate:
                    continue
                if number_plate in self.occupied_plates:
                    tk.messagebox.showerror("Error", "This number plate is already parked.")
                    return
                break
            
            self.car_park[row][col] = number_plate  
            self.occupied_plates.add(number_plate)
            self.buttons[row][col].config(bg = "red", text = "Occupied")
            self.log_activity("Entry", space_number, number_plate)
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
