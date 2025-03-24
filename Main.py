import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog, ttk
from tkinter.ttk import Combobox
import database as db
import random

db.connect_db()


class PetServiceManagementSystem:
    def __init__(self, window):
        self.window = window
        self.window.title("PET SERVICE MANAGEMENT SYSTEM")
        self.window.geometry("1000x800")

        tk.Label(window, text="Pet Service Management System", font=("Arial", 20)).pack()
        self.frame = tk.Frame(self.window)
        self.frame.pack()

        tk.Button(self.frame, text="User", command=self.User).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(self.frame, text="Admin", command=self.Doctor).grid(row=0, column=1, padx=5, pady=5)

        self.appointments = []

    def clear_frame(self):
        """Clear all widgets from the frame."""
        for widget in self.frame.winfo_children():
            widget.destroy()

    def back_to_main(self):
        self.clear_frame()
        self.__init__(self.window)

    def User(self):
        self.clear_frame()
        tk.Label(self.frame, text="Pet").grid(row=0, column=0, padx=5, pady=5, columnspan=3)
        tk.Button(self.frame, text="Login", command=self.UserLogIn).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self.frame, text="Create Account", command=self.UserRegister).grid(row=1, column=2, padx=5, pady=5)
        tk.Button(self.frame, text="Back", command=self.back_to_main).grid(row=2, column=1, padx=5, pady=5)

    def Doctor(self):
        self.clear_frame()
        tk.Label(self.frame, text="Doctor").grid(row=0, column=0, padx=5, pady=5)
        tk.Button(self.frame, text="Login", command=self.DoctorLogIn).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(self.frame, text="Back", command=self.back_to_main).grid(row=2, column=0, padx=5, pady=5)

    def UserLogIn(self):
        self.clear_frame()
        tk.Label(self.frame, text="Login").grid(row=0, column=0, padx=5, pady=5, columnspan=2)
        tk.Label(self.frame, text="Username").grid(row=1, column=0, padx=5, pady=5)
        username_entry = tk.Entry(self.frame)
        username_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(self.frame, text="Password").grid(row=2, column=0, padx=5, pady=5)
        password_entry = tk.Entry(self.frame, show="*")
        password_entry.grid(row=2, column=1, padx=5, pady=5)
        tk.Button(self.frame, text="Login", command=lambda: self.Login(username_entry.get(), password_entry.get())).grid(row=3, column=0, padx=5, pady=5)
        tk.Button(self.frame, text="Back", command=self.User).grid(row=3, column=1, padx=5, pady=5)

    def UserRegister(self):
        self.clear_frame()
        tk.Label(self.frame, text="Register").grid(row=0, column=0, padx=5, pady=5, columnspan=2)
        tk.Label(self.frame, text="Username").grid(row=1, column=0, padx=5, pady=5)
        username_entry = tk.Entry(self.frame)
        username_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(self.frame, text="Password").grid(row=2, column=0, padx=5, pady=5)
        password_entry = tk.Entry(self.frame, show="*")
        password_entry.grid(row=2, column=1, padx=5, pady=5)
        tk.Button(self.frame, text="Register", command=lambda: self.Register(username_entry.get(), password_entry.get())).grid(row=3, column=0, padx=5, pady=5)
        tk.Button(self.frame, text="Back", command=self.User).grid(row=3, column=1, padx=5, pady=5)

    def Register(self, username, password):
        if username and password:
            try:
                user_id = db.insert_user(username, password)
                messagebox.showinfo("Success", f"User registered successfully! Your ID is: {user_id}")
                self.UserLogIn()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
    def Login(self, username, password):
        if username and password:
            print(f"Attempting login for: {username}")  # Debugging output
            if db.validate_user(username, password):
                print("Login successful")  # Debugging output
                self.load_patient_dashboard(username)
            else:
                print("Login failed")  # Debugging output
                messagebox.showerror("Login Failed", "Invalid username or password.")
        else:
            messagebox.showwarning("Input Error", "Please enter both username and password.")
    
    def load_patient_dashboard(self, username):
        self.clear_frame()
        tk.Label(self.frame, text=f"Welcome, {username}", font=("Arial", 20, "bold")).pack(pady=10)
        tk.Button(self.frame, text="Manage My Pets", font=("Arial", 12, "bold"), command=lambda: self.ManageMyPets(username)).pack(pady=5)
        tk.Button(self.frame, text="Grooming Services", font=("Arial", 12, "bold"), command=lambda: self.GroomingServices(username)).pack(pady=5)
        tk.Button(self.frame, text="Daycare", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Button(self.frame, text="Service History", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Button(self.frame, text="Back", command=self.User).pack(pady=10)
    
    def ManageMyPets(self, username):
        self.clear_frame()
        tk.Label(self.frame, text="Manage My Pets", font=("Arial", 20, "bold")).pack(pady=10)

        table_frame = tk.Frame(self.frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columns = ("Name", "Species", "Age", "Picture")
        pet_table = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

        pet_table.heading("Name", text="Name")
        pet_table.heading("Species", text="Species")
        pet_table.heading("Age", text="Age")
        pet_table.heading("Picture", text="Picture")

        pet_table.column("Name", width=150, anchor=tk.CENTER)
        pet_table.column("Species", width=100, anchor=tk.CENTER)
        pet_table.column("Age", width=50, anchor=tk.CENTER)
        pet_table.column("Picture", width=200, anchor=tk.CENTER)

        pet_table.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=pet_table.yview)
        pet_table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        pets = db.get_user_pets(username)
        if pets:
            for pet in pets:
                try:
                    if pet["picture_path"]:
                        image = tk.PhotoImage(file=pet["picture_path"]).subsample(4, 4)
                        pet_table.image = image  # Save a reference to avoid garbage collection
                        pet_table.insert("", tk.END, values=(pet["name"],pet["species"],pet["age"],"Image Displayed"
                        ))
                    else:
                        pet_table.insert("", tk.END, values=(pet["name"],pet["species"],pet["age"],"No Image"))
                except Exception as e:
                    print(f"Error loading image: {e}")
                    pet_table.insert("", tk.END, values=(pet["name"],pet["species"],pet["age"],"Error Displaying Image"))
        else:
            tk.Label(self.frame, text="No pets registered yet.").pack(pady=5)
        tk.Button(self.frame, text="Add Pet", font=("Arial", 12, "bold"), command=lambda: self.AddPet(username)).pack(pady=5)
        tk.Button(self.frame, text="Back", command=lambda: self.load_patient_dashboard(username)).pack(pady=10)

    def AddPet(self, username):
        self.clear_frame()
        tk.Label(self.frame, text="Add Pet", font=("Arial", 20, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        tk.Label(self.frame, text="Name").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        pet_name = tk.Entry(self.frame)
        pet_name.grid(row=1, column=1, padx=10, pady=5)
        tk.Label(self.frame, text="Species").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        species_options = ["Dog", "Cat"]
        pet_species = Combobox(self.frame, values=species_options, state="readonly")
        pet_species.grid(row=2, column=1, padx=10, pady=5)
        tk.Label(self.frame, text="Age").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        pet_age = tk.Entry(self.frame)
        pet_age.grid(row=3, column=1, padx=10, pady=5)
        tk.Label(self.frame, text="Upload Picture").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        picture_path_label = tk.Label(self.frame, text="No file selected")
        picture_path_label.grid(row=4, column=1, padx=10, pady=5)
        upload_button = tk.Button(self.frame, text="Upload Picture", command=lambda: self.upload_picture(picture_path_label))
        upload_button.grid(row=5, column=1, padx=10, pady=5)
        save_button = tk.Button(self.frame,text="Save",font=("Arial", 12, "bold"),command=lambda: self.submit_pet(username, pet_name.get(), pet_species.get(), pet_age.get(), picture_path_label.cget("text")))
        save_button.grid(row=6, column=0, padx=10, pady=10)
        back_button = tk.Button(self.frame,text="Cancel",font=("Arial", 12, "bold"),command=lambda: self.ManageMyPets(username))
        back_button.grid(row=6, column=1, padx=10, pady=10)

    def upload_picture(self, picture_path_label):
        file_path = filedialog.askopenfilename(title="Select Pet Picture",filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            picture_path_label.config(text=file_path)
            
    def submit_pet(self, username, name, species, age, picture_path=None):
        try:
            if not all([username, name, species, age]):
                raise ValueError("All fields are required.")
            age = int(age) if age.isdigit() else None
            if age is None:
                raise ValueError("Age must be a number.")
            user_id = db.get_user_id(username)
            if not user_id:
                raise ValueError("User not found.")
            db.add_pet(user_id, name, species, age, picture_path)
            messagebox.showinfo("Success", "Pet added successfully!")
            self.ManageMyPets(username)
        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add pet: {e}")
    
    def GroomingServices(self, username):
        self.clear_frame()
        tk.Label(self.frame, text="Grooming Services", font=("Arial", 20, "bold")).pack(pady=10)

    # Fetch user's pets
        pets = db.get_user_pets(username)
        if not pets:
            tk.Label(self.frame, text="No pets registered. Please add a pet first.", font=("Arial", 12)).pack(pady=10)
            tk.Button(self.frame, text="Back", command=lambda: self.load_patient_dashboard(username)).pack(pady=10)
            return

    # Pet selection dropdown
        tk.Label(self.frame, text="Select Pet:", font=("Arial", 12)).pack(pady=5)
        pet_names = [pet["name"] for pet in pets]
        selected_pet = tk.StringVar()
        pet_dropdown = Combobox(self.frame, textvariable=selected_pet, values=pet_names, state="readonly")
        pet_dropdown.pack(pady=5)

    # Grooming services checkboxes
        tk.Label(self.frame, text="Select Services:", font=("Arial", 12)).pack(pady=10)
        services = [
        "Basic Grooming",
        "Full Grooming",
        "Nail Clipping",
        "Ear Cleaning",
        "Bath & Blow Dry"
        ]
        selected_services = {service: tk.BooleanVar() for service in services}
        for service in services:
            tk.Checkbutton(self.frame, text=service, variable=selected_services[service]).pack(anchor="w", padx=20)

    # Submit button
        tk.Button(
        self.frame,
        text="Book Now",
        font=("Arial", 12, "bold"),
        command=lambda: self.book_grooming(username, selected_pet.get(), selected_services)
        ).pack(pady=10)

    # Back button
        tk.Button(self.frame, text="Back", command=lambda: self.load_patient_dashboard(username)).pack(pady=10)

    def book_grooming(self, username, pet_name, selected_services):
        try:
            if not pet_name:
                raise ValueError("Please select a pet.")
            services = [service for service, var in selected_services.items() if var.get()]
            if not services:
                raise ValueError("Please select at least one grooming service.")

        # Here, you can add logic to save the booking to the database or perform other actions.
            messagebox.showinfo("Success", f"Grooming services booked for {pet_name}: {', '.join(services)}")
            self.load_patient_dashboard(username)
        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to book grooming services: {e}")
window = tk.Tk()
PetServiceManagementSystem(window)
window.mainloop()