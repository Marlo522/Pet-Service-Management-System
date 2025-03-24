import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog, ttk
from tkinter.ttk import Combobox
import database as db
import random
from PIL import Image, ImageTk  # Add this import for image handling

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
        """Clear the frame and show the main content."""
        self.clear_frame()
        tk.Label(self.window, text="Pet Service Management System", font=("Arial", 20)).pack()
        self.frame = tk.Frame(self.window)
        self.frame.pack()
        tk.Button(self.frame, text="User", command=self.User).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(self.frame, text="Admin", command=self.Doctor).grid(row=0, column=1, padx=5, pady=5)

    def User(self):
        self.clear_frame()
        tk.Label(self.frame, text="Pet").grid(row=0, column=0, padx=5, pady=5, columnspan=3)
        tk.Button(self.frame, text="Login", command=self.UserLogIn).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self.frame, text="Create Account", command=self.UserRegister).grid(row=1, column=2, padx=5, pady=5)
        tk.Button(self.frame, text="Back", command=self.back_to_main).grid(row=2, column=1, padx=5, pady=5)

    def Doctor(self):
        self.clear_frame()
        tk.Label(self.frame, text="Admin Login", font=("Arial", 20, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        tk.Label(self.frame, text="Username").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        admin_username = tk.Entry(self.frame)
        admin_username.grid(row=1, column=1, padx=10, pady=5)
        tk.Label(self.frame, text="Password").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        admin_password = tk.Entry(self.frame, show="*")
        admin_password.grid(row=2, column=1, padx=10, pady=5)
        tk.Button(self.frame, text="Login", font=("Arial", 12, "bold"),
                  command=lambda: self.AdminLogin(admin_username.get(), admin_password.get())).grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(self.frame, text="Back", command=self.back_to_main).grid(row=4, column=0, columnspan=2, pady=10)

    def AdminLogin(self, username, password):
        if username == "admin" and password == "admin":
            messagebox.showinfo("Success", "Admin login successful!")
            self.load_admin_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid admin credentials.")

    def load_admin_dashboard(self):
        self.clear_frame()
        tk.Label(self.frame, text="Admin Dashboard", font=("Arial", 20, "bold")).pack(pady=10)
        tk.Button(self.frame, text="View All Users", font=("Arial", 12, "bold"), command=self.view_all_users).pack(pady=5)
        tk.Button(self.frame, text="View All Pets", font=("Arial", 12, "bold"), command=self.view_all_pets).pack(pady=5)
        tk.Button(self.frame, text="Back", command=self.back_to_main).pack(pady=10)

    def view_all_users(self):
        self.clear_frame()
        tk.Label(self.frame, text="All Users", font=("Arial", 20, "bold")).pack(pady=10)
        users = db.get_all_users()
        if users:
            for user in users:
                tk.Label(self.frame, text=f"ID: {user['id']}, Username: {user['username']}").pack(pady=5)
        else:
            tk.Label(self.frame, text="No users found.").pack(pady=5)
        tk.Button(self.frame, text="Back", command=self.load_admin_dashboard).pack(pady=10)

    def view_all_pets(self):
        self.clear_frame()
        tk.Label(self.frame, text="All Pets", font=("Arial", 20, "bold")).pack(pady=10)
        pets = db.get_all_pets()
        if pets:
            for pet in pets:
                tk.Label(self.frame, text=f"Name: {pet['name']}, Species: {pet['species']}, Owner ID: {pet['user_id']}").pack(pady=5)
        else:
            tk.Label(self.frame, text="No pets found.").pack(pady=5)
        tk.Button(self.frame, text="Back", command=self.load_admin_dashboard).pack(pady=10)

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

        pets = db.get_user_pets(username)
        if pets:
            for pet in pets:
                pet_frame = tk.Frame(self.frame, borderwidth=1, relief="solid", padx=10, pady=10)
                pet_frame.pack(fill=tk.X, padx=10, pady=5)

                # Display pet details
                details = f"Name: {pet['name']}\nSpecies: {pet['species']}\nAge: {pet['age']}"
                tk.Label(pet_frame, text=details, justify="left").pack(side=tk.LEFT, padx=10)

                # Display pet image
                try:
                    if pet["picture_path"]:
                        pil_image = Image.open(pet["picture_path"]).resize((100, 100), Image.LANCZOS)
                        image = ImageTk.PhotoImage(pil_image)
                        image_label = tk.Label(pet_frame, image=image)
                        image_label.image = image  # Keep a reference to avoid garbage collection
                        image_label.pack(side=tk.RIGHT, padx=10)
                    else:
                        tk.Label(pet_frame, text="No Image").pack(side=tk.RIGHT, padx=10)
                except Exception as e:
                    print(f"Error loading image: {e}")
                    tk.Label(pet_frame, text="Error Displaying Image").pack(side=tk.RIGHT, padx=10)

                # Add Edit and Delete buttons
                tk.Button(pet_frame, text="Edit", command=lambda pet=pet: self.EditPet(username, pet)).pack(side=tk.RIGHT, padx=5)
                tk.Button(pet_frame, text="Delete", command=lambda pet=pet: self.DeletePet(username, pet['name'])).pack(side=tk.RIGHT, padx=5)
        else:
            tk.Label(self.frame, text="No pets registered yet.").pack(pady=5)

        tk.Button(self.frame, text="Add Pet", font=("Arial", 12, "bold"), command=lambda: self.AddPet(username)).pack(pady=5)
        tk.Button(self.frame, text="Back", command=lambda: self.load_patient_dashboard(username)).pack(pady=10)

    def DeletePet(self, username, pet_name):
        try:
            user_id = db.get_user_id(username)
            if not user_id:
                raise ValueError("User not found.")
            db.delete_pet(user_id, pet_name)
            messagebox.showinfo("Success", f"Pet '{pet_name}' deleted successfully!")
            self.ManageMyPets(username)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete pet: {e}")

    def EditPet(self, username, pet):
        self.clear_frame()
        tk.Label(self.frame, text="Edit Pet", font=("Arial", 20, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        tk.Label(self.frame, text="Name").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        pet_name = tk.Entry(self.frame)
        pet_name.insert(0, pet['name'])
        pet_name.grid(row=1, column=1, padx=10, pady=5)
        tk.Label(self.frame, text="Species").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        species_options = ["Dog", "Cat"]
        pet_species = Combobox(self.frame, values=species_options, state="readonly")
        pet_species.set(pet['species'])
        pet_species.grid(row=2, column=1, padx=10, pady=5)
        tk.Label(self.frame, text="Age").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        pet_age = tk.Entry(self.frame)
        pet_age.insert(0, pet['age'])
        pet_age.grid(row=3, column=1, padx=10, pady=5)
        tk.Label(self.frame, text="Upload Picture").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        picture_path_label = tk.Label(self.frame, text=pet['picture_path'] or "No file selected")
        picture_path_label.grid(row=4, column=1, padx=10, pady=5)
        upload_button = tk.Button(self.frame, text="Upload Picture", command=lambda: self.upload_picture(picture_path_label))
        upload_button.grid(row=5, column=1, padx=10, pady=5)
        save_button = tk.Button(self.frame, text="Save", font=("Arial", 12, "bold"),
                                command=lambda: self.submit_edit_pet(username, pet['name'], pet_name.get(), pet_species.get(), pet_age.get(), picture_path_label.cget("text")))
        save_button.grid(row=6, column=0, padx=10, pady=10)
        back_button = tk.Button(self.frame, text="Cancel", font=("Arial", 12, "bold"), command=lambda: self.ManageMyPets(username))
        back_button.grid(row=6, column=1, padx=10, pady=10)

    def submit_edit_pet(self, username, old_name, new_name, new_species, new_age, new_picture_path=None):
        try:
            if not all([username, new_name, new_species, new_age]):
                raise ValueError("All fields are required.")
            new_age = int(new_age) if new_age.isdigit() else None
            if new_age is None:
                raise ValueError("Age must be a number.")
            user_id = db.get_user_id(username)
            if not user_id:
                raise ValueError("User not found.")
            db.edit_pet(user_id, old_name, new_name, new_species, new_age, new_picture_path)
            messagebox.showinfo("Success", "Pet details updated successfully!")
            self.ManageMyPets(username)
        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update pet: {e}")

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
        tk.Label(self.frame, text="Grooming Services", font=("Arial", 20, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

    # Fetch user's pets
        pets = db.get_user_pets(username)
        if not pets:
            tk.Label(self.frame, text="No pets registered. Please add a pet first.", font=("Arial", 12)).grid(row=1, column=0, columnspan=2, pady=10)
            tk.Button(self.frame, text="Back", command=lambda: self.load_patient_dashboard(username)).grid(row=2, column=0, columnspan=2, pady=10)
            return

    # Pet selection dropdown
        tk.Label(self.frame, text="Select Pet:", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=5, sticky="w")
        pet_options = [pet["name"] for pet in pets]
        selected_pet = tk.StringVar()
        pet_dropdown = ttk.Combobox(self.frame, values=pet_options, textvariable=selected_pet, state="readonly")
        pet_dropdown.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    # Grooming services radio buttons
        tk.Label(self.frame, text="Select Service:", font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=5, sticky="w")
        selected_service = tk.StringVar()
        services = ["Basic Grooming", "Full Grooming", "Nail Clipping", "Ear Cleaning", "Bath & Blow Dry"]
        for i, service in enumerate(services):
            tk.Radiobutton(self.frame, text=service, variable=selected_service, value=service).grid(row=5 + i, column=0, padx=10, pady=2, sticky="w")

    # Date selection dropdown
        tk.Label(self.frame, text="Select Date:", font=("Arial", 12)).grid(row=4, column=1, padx=10, pady=5, sticky="w")
        available_dates = ["2025-03-25", "2025-03-26", "2025-03-27", "2025-03-28"]  # Example dates
        selected_date = tk.StringVar(value=available_dates[0])
        date_dropdown = ttk.Combobox(self.frame, textvariable=selected_date, values=available_dates, state="readonly")
        date_dropdown.grid(row=5, column=1, padx=10, pady=5, sticky="w")

    # Book button
        tk.Button(
        self.frame,
        text="Book Service",
        font=("Arial", 12, "bold"),
        command=lambda: self.book_grooming(username, selected_pet.get(), selected_service.get(), selected_date.get())
    ).grid(row=10, column=0, columnspan=2, pady=10)
        
    # my grooming appointments
        tk.Label(self.frame, text="My Grooming Appointments", font=("Arial", 16, "bold")).grid(row=11, column=0, columnspan=2, pady=10)
        appointments = db.get_grooming_appointments(username)
        if appointments:
            for i, appointment in enumerate(appointments):
                tk.Label(self.frame, text=f"{i + 1}. {appointment['pet_name']} - {appointment['service_type']} - {appointment['service_date']}").grid(row=12 + i, column=0, padx=10, pady=5, sticky="w")
                tk.Button(
                self.frame,
                text="Cancel",
                command=lambda appointment_id=appointment['id']: self.cancel_grooming(username, appointment_id)
            ).grid(row=12 + i, column=1, padx=10, pady=5)
        else:
            tk.Label(self.frame, text="No grooming appointments found.").grid(row=12, column=0, columnspan=2, pady=5)

    # Back button
        tk.Button(self.frame, text="Back", font=("Arial", 12, "bold"), command=lambda: self.load_patient_dashboard(username)).grid(row=20, column=0, columnspan=2, pady=10)

    def cancel_grooming(self, username, appointment_id):
        try:
            db.cancel_grooming_appointment(appointment_id)
            messagebox.showinfo("Success", "Grooming appointment canceled successfully!")
            self.GroomingServices(username)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to cancel appointment: {e}")

            
        

    def book_grooming(self, username, pet_name, selected_service, selected_date):
        try:
            print(f"Booking details: Pet: {pet_name}, Service: {selected_service}, Date: {selected_date}")  # Debugging output
            if not pet_name:
                raise ValueError("Please select a pet.")
            if not selected_service:
                raise ValueError("Please select a grooming service.")
            if not selected_date:
                raise ValueError("Please select a date.")

        # Get the user ID from the username
            user_id = db.get_user_id(username)
            if not user_id:
                raise ValueError("User not found.")

        # Save the booking to the database
            db.add_grooming_service(user_id, pet_name, selected_service, selected_date)

        # Show success message
            messagebox.showinfo("Success", f"Grooming service booked for {pet_name} on {selected_date}: {selected_service}")
            self.load_patient_dashboard(username)
        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to book grooming service: {e}")
window = tk.Tk()
PetServiceManagementSystem(window)
window.mainloop()