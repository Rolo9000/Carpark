import tkinter as tk
from tkinter.simpledialog import askstring, askinteger
#hello
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
        
        self.registered_cars = {}

    def toggle_space(self, row, col):
        if self.car_park[row][col]:
            self.car_park[row][col] = None  
            self.buttons[row][col].config(bg="green", text=f"Space {row * self.cols + col + 1}")
        else:
            self.car_park[row][col] = "Occupied"  
            self.buttons[row][col].config(bg="red", text=f"Occupied")

    def process_user_choice(self):
        choice = askstring("Car Park", "Do you want to park or exit? (Park/Exit)").lower()
        if choice == "park":
            number_plate = askstring("Enter Number Plate", "Please enter your number plate:")
            if number_plate:
                self.choose_parking_slot(number_plate)
        elif choice == "exit":
            number_plate = askstring("Exit Car Park", "Please enter the number plate of the car leaving:")
            if number_plate:
                self.remove_car(number_plate)
        else:
            print("Invalid choice. Please enter 'Park' or 'Exit'.")
            self.process_user_choice()

    def choose_parking_slot(self, number_plate):
        if number_plate in self.registered_cars:
            print(f"Car {number_plate} is already parked.")
            return  

        slot = askstring("Choose Parking Slot", "Please enter the parking slot number (1 to {0}):".format(self.rows * self.cols))
        try:
            slot = int(slot) - 1
            row = slot // self.cols
            col = slot % self.cols

            if 0 <= slot < self.rows * self.cols and self.car_park[row][col] is None:
                self.car_park[row][col] = number_plate
                self.buttons[row][col].config(bg="red", text=f"Occupied")
                self.registered_cars[number_plate] = (row, col)
                print(f"Car {number_plate} parked in space {slot + 1}.")
            else:
                print("Invalid or already occupied parking spot.")
        except ValueError:
            print("Invalid slot number. Please try again.")
            self.choose_parking_slot(number_plate)

    def remove_car(self, number_plate):
        if number_plate not in self.registered_cars:
            print(f"Car with number plate {number_plate} is not parked in the car park.")
            return  

        row, col = self.registered_cars[number_plate]
        self.car_park[row][col] = None
        self.buttons[row][col].config(bg="green", text=f"Space {row * self.cols + col + 1}")
        del self.registered_cars[number_plate]
        print(f"Car {number_plate} has exited and the parking space is now available.")

    def refresh_display(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.car_park[i][j] is None:
                    self.buttons[i][j].config(bg="green", text=f"Space {i * self.cols + j + 1}")
                else:
                    self.buttons[i][j].config(bg="red", text=f"Occupied")

root = tk.Tk()
car_park = CarPark(root)

def keep_running():
    car_park.process_user_choice()
    car_park.refresh_display()
    root.after(1000, keep_running)

keep_running()
root.mainloop()
