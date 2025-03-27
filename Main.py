import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog, ttk
from tkinter.ttk import Combobox
import database as db
import random
from PIL import Image, ImageTk  # Add this import for image handling
from tkcalendar import Calendar  # Import Calendar for date selection

db.connect_db()


class PetServiceManagementSystem:
    def __init__(self, window):
        self.window = window
        self.window.title("PET SERVICE MANAGEMENT SYSTEM")
        self.window.geometry("900x700")
        self.window.configure(bg="#B7D8E6")

        tk.Label(window, text="Pet Service Management System", font=("Bebas Neue", 30),bg="#B7D8E6",fg="white", pady=20).pack()
        self.frame = tk.Frame(self.window, bg="#B7D8E6")
        self.frame.pack()
        
        button_style = {
            "bg": "#45A29E",  # Sand color
            "fg": "black",
            "font": ("Arial", 14),
            "width": 20,  # Equal width for buttons
        }

        tk.Button(self.frame, text="User", command=self.User, **button_style).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(self.frame, text="Admin", command=self.Doctor, **button_style).grid(row=0, column=1, padx=5, pady=5)

        self.appointments = []

    def clear_frame(self):
        """Clear all widgets from the frame."""
        for widget in self.frame.winfo_children():
            widget.destroy()

    def back_to_main(self):
        """Clear the frame and show the main content."""
        self.clear_frame()
        self.frame.pack()
        tk.Button(self.frame, text="User", command=self.User).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(self.frame, text="Admin", command=self.Doctor).grid(row=0, column=1, padx=5, pady=5)

    def User(self):
        self.clear_frame()
        tk.Label(self.frame, text="User Login", font=("Bebas Neue", 20),bg="#B7D8E6",fg="white").grid(row=0, column=0, padx=5, pady=20, columnspan=3)
        tk.Button(self.frame, text="Login", command=self.UserLogIn).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self.frame, text="Create Account", command=self.UserRegister).grid(row=1, column=2, padx=5, pady=5)
        tk.Button(self.frame, text="Back", command=self.back_to_main).grid(row=2, column=1, padx=5, pady=5)

    def Doctor(self):
        self.clear_frame()
        tk.Label(self.frame, text="Admin Login", font=("Bebas Neue", 20),bg="#B7D8E6",fg="white").grid(row=0, column=0, columnspan=2, pady=20)
        tk.Label(self.frame, text="Username", font=("Bebas Neue", 10),bg="#B7D8E6",fg="white").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        admin_username = tk.Entry(self.frame)
        admin_username.grid(row=1, column=1, padx=10, pady=5)
        tk.Label(self.frame, text="Password", font=("Bebas Neue", 10),bg="#B7D8E6",fg="white").grid(row=2, column=0, padx=10, pady=5, sticky="w")
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
        tk.Label(self.frame, text="Admin Dashboard", font=("Bebas Neue", 20),bg="#B7D8E6",fg="white").pack(pady=20)
        tk.Button(self.frame, text="Manage Users", font=("Arial", 12, "bold"), command=self.view_all_users).pack(pady=5)
        tk.Button(self.frame, text="Manage Pets", font=("Arial", 12, "bold"), command=self.view_all_pets).pack(pady=5)
        tk.Button(self.frame, text="Manage Grooming Appointments", font=("Arial", 12, "bold"), command=self.manage_grooming_appointments).pack(pady=5)
        tk.Button(self.frame, text="Manage Daycare Booking", font=("Arial", 12, "bold"), command=self.manage_service_history).pack(pady=5)
        tk.Button(self.frame, text="View Service History", font=("Arial", 12, "bold"), command=self.Doctor).pack(pady=10)
        tk.Button(self.frame, text="Back", command=self.back_to_main).pack(pady=10)
        
    def load_user_dashboard(self, username):
        self.clear_frame()
        tk.Label(self.frame, text=f"Welcome, {username}", font=("Bebas Neue", 20),bg="#B7D8E6",fg="white").pack(pady=20)
        tk.Button(self.frame, text="Manage My Pets", font=("Arial", 12, "bold"), command=lambda: self.ManageMyPets(username)).pack(pady=5)
        tk.Button(self.frame, text="Grooming Services", font=("Arial", 12, "bold"), command=lambda: self.GroomingServices(username)).pack(pady=5)
        tk.Button(self.frame, text="Daycare", font=("Arial", 12, "bold"), command=lambda: self.Daycare(username)).pack(pady=5)
        tk.Button(self.frame, text="Service History", font=("Arial", 12, "bold"), command=lambda: self.ServiceHistory(username)).pack(pady=5)
        tk.Button(self.frame, text="Back", command=self.User).pack(pady=10)

    def manage_service_history(self):
        self.clear_frame()
        tk.Label(self.frame, text="Manage Service History", font=("Bebas Neue", 20),bg="#B7D8E6",fg="white").pack(pady=20)

        history = db.get_all_service_history()
        if history:
            for record in history:
                record_frame = tk.Frame(self.frame, borderwidth=1, relief="solid", padx=10, pady=10)
                record_frame.pack(fill=tk.X, padx=10, pady=5)

                details = (
                    f"ID: {record['id']}\n"
                    f"Pet: {record['pet_name']}\n"
                    f"Service: {record['service_type']}\n"
                    f"Date: {record['date']}\n"
                    f"Details: {record['details']}\n"
                    f"Status: {record['status']}"
                )
                tk.Label(record_frame, text=details, justify="left", font=("Bebas Neue", 10),bg="#B7D8E6",fg="white").pack(side=tk.LEFT, padx=10)

                if record["status"] == "Pending":
                    tk.Button(
                        record_frame,
                        text="Mark as Done",
                        command=lambda record_id=record['id']: self.update_service_status(record_id)
                    ).pack(side=tk.RIGHT, padx=10)
        else:
            tk.Label(self.frame, text="No service history found.", font=("Bebas Neue", 10),bg="#B7D8E6",fg="white").pack(pady=10)

        tk.Button(self.frame, text="Back", command=self.load_admin_dashboard).pack(pady=10)
        
    def manage_grooming_appointments(self):
        self.clear_frame()
        tk.Label(self.frame, text="Manage Grooming Appointments", font=("Bebas Neue", 20),bg="#B7D8E6",fg="white").pack(pady=20)

    # Fetch all grooming appointments with status = 'Pending'
        appointments = db.get_all_grooming_appointments()
        pending_appointments = [appt for appt in appointments if appt["status"] == "Pending"]

        if pending_appointments:
            for appointment in pending_appointments:
                appointment_frame = tk.Frame(self.frame, borderwidth=1, relief="solid", padx=10, pady=10)
                appointment_frame.pack(fill=tk.X, padx=10, pady=5)

                details = (
                f"ID: {appointment['id']}\n"
                f"User ID: {appointment['user_id']}\n"
                f"Pet: {appointment['pet_name']}\n"
                f"Service: {appointment['service_type']}\n"
                f"Date: {appointment['service_date']}\n"
                f"Status: {appointment['status']}"
            )
                tk.Label(appointment_frame, text=details, justify="left", font=("Bebas Neue", 10),bg="#B7D8E6",fg="white").pack(side=tk.LEFT, padx=10)

            # Add a button to mark the appointment as "Done"
                tk.Button(
                appointment_frame,
                text="Mark as Done",
                command=lambda appointment_id=appointment['id']: self.update_grooming_status(appointment_id)
            ).pack(side=tk.RIGHT, padx=10)
        else:
            tk.Label(self.frame, text="No pending grooming appointments found.", font=("Arial", 12)).pack(pady=10)

        tk.Button(self.frame, text="Back", command=self.load_admin_dashboard).pack(pady=10)
    
    def update_grooming_status(self, appointment_id):
        try:
        # Update the status in the database
            db.update_grooming_status(appointment_id, "Done")
            messagebox.showinfo("Success", "Grooming appointment marked as 'Done'!")
            self.manage_grooming_appointments()  # Refresh the grooming appointments menu
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update appointment status: {e}")

    def update_service_status(self, record_id):
        try:
            db.update_service_status(record_id, "Done")
            messagebox.showinfo("Success", "Service status updated to 'Done'!")
            self.manage_service_history()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update status: {e}")

    def view_all_users(self):
        self.clear_frame()
        tk.Label(self.frame, text="All Users", font=("Bebas Neue", 20),bg="#B7D8E6",fg="white").pack(pady=20)
        users = db.get_all_users()
        if users:
            for user in users:
                tk.Label(self.frame, text=f"ID: {user['id']}, Username: {user['username']}", font=("Bebas Neue", 10),bg="#B7D8E6",fg="white").pack(pady=5)
        else:
            tk.Label(self.frame, text="No users found.", font=("Bebas Neue", 10),bg="#B7D8E6",fg="white").pack(pady=5)
        tk.Button(self.frame, text="Back", command=self.load_admin_dashboard).pack(pady=10)

    def view_all_pets(self):
        self.clear_frame()
        tk.Label(self.frame, text="All Pets", font=("Bebas Neue", 20),bg="#B7D8E6",fg="white").pack(pady=20)
        pets = db.get_all_pets()
        if pets:
            for pet in pets:
                tk.Label(self.frame, text=f"Name: {pet['name']}, Species: {pet['species']}, Owner ID: {pet['user_id']}", font=("Bebas Neue", 10),bg="#B7D8E6",fg="white").pack(pady=5)
        else:
            tk.Label(self.frame, text="No pets found.", font=("Bebas Neue", 10),bg="#B7D8E6",fg="white").pack(pady=5)
        tk.Button(self.frame, text="Back", command=self.load_admin_dashboard).pack(pady=10)

    def UserLogIn(self):
        self.clear_frame()
        tk.Label(self.frame, text="Login", font=("Bebas Neue", 20),bg="#B7D8E6",fg="white").grid(row=0, column=0, padx=5, pady=5, columnspan=2)
        tk.Label(self.frame, text="Username", font=("Bebas Neue", 10),bg="#B7D8E6",fg="white").grid(row=1, column=0, padx=5, pady=5)
        username_entry = tk.Entry(self.frame)
        username_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(self.frame, text="Password", font=("Bebas Neue", 10),bg="#B7D8E6",fg="white").grid(row=2, column=0, padx=5, pady=5)
        password_entry = tk.Entry(self.frame, show="*")
        password_entry.grid(row=2, column=1, padx=5, pady=5)
        tk.Button(self.frame, text="Login", command=lambda: self.Login(username_entry.get(), password_entry.get())).grid(row=3, column=0, padx=5, pady=5)
        tk.Button(self.frame, text="Back", command=self.User).grid(row=3, column=1, padx=5, pady=5)

    def UserRegister(self):
        self.clear_frame()
        tk.Label(self.frame, text="Register", font=("Bebas Neue", 20),bg="#B7D8E6",fg="white").grid(row=0, column=0, padx=5, pady=20, columnspan=2)
        tk.Label(self.frame, text="Username",font=("Bebas Neue", 10),bg="#B7D8E6",fg="white").grid(row=1, column=0, padx=5, pady=5)
        username_entry = tk.Entry(self.frame)
        username_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(self.frame, text="Password", font=("Bebas Neue", 10),bg="#B7D8E6",fg="white").grid(row=2, column=0, padx=5, pady=5)
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
                self.load_user_dashboard(username)
            else:
                print("Login failed")  # Debugging output
                messagebox.showerror("Login Failed", "Invalid username or password.")
        else:
            messagebox.showwarning("Input Error", "Please enter both username and password.")
    
    
    def ManageMyPets(self, username):
        self.clear_frame()
        tk.Label(self.frame, text="Manage My Pets", font=("Bebas Neue", 20),bg="#B7D8E6",fg="white").pack(pady=20)

        pets = db.get_user_pets(username)
        if pets:
            for pet in pets:
                pet_frame = tk.Frame(self.frame, borderwidth=1, relief="solid", padx=10, pady=10)
                pet_frame.pack(fill=tk.X, padx=10, pady=5)

                # Display pet details
                details = f"Name: {pet['name']}\nSpecies: {pet['species']}\nAge: {pet['age']}"
                tk.Label(pet_frame, text=details, justify="left", font=("Bebas Neue", 10),bg="#B7D8E6",fg="white").pack(side=tk.LEFT, padx=10)

                # Display pet image
                try:
                    if pet["picture_path"]:
                        pil_image = Image.open(pet["picture_path"]).resize((100, 100), Image.LANCZOS)
                        image = ImageTk.PhotoImage(pil_image)
                        image_label = tk.Label(pet_frame, image=image)
                        image_label.image = image  # Keep a reference to avoid garbage collection
                        image_label.pack(side=tk.RIGHT, padx=10)
                    else:
                        tk.Label(pet_frame, text="No Image", font=("Bebas Neue", 10),bg="#B7D8E6",fg="white").pack(side=tk.RIGHT, padx=10)
                except Exception as e:
                    print(f"Error loading image: {e}")
                    tk.Label(pet_frame, text="Error Displaying Image", font=("Bebas Neue", 10),bg="#B7D8E6",fg="white").pack(side=tk.RIGHT, padx=10)

                # Add Edit and Delete buttons
                tk.Button(pet_frame, text="Edit", command=lambda pet=pet: self.EditPet(username, pet)).pack(side=tk.RIGHT, padx=5)
                tk.Button(pet_frame, text="Delete", command=lambda pet=pet: self.DeletePet(username, pet['name'])).pack(side=tk.RIGHT, padx=5)
        else:
            tk.Label(self.frame, text="No pets registered yet.", font=("Bebas Neue", 10),bg="#B7D8E6",fg="white").pack(pady=5)

        tk.Button(self.frame, text="Add Pet", font=("Arial", 12, "bold"), command=lambda: self.AddPet(username)).pack(pady=5)
        tk.Button(self.frame, text="Back", command=lambda: self.load_user_dashboard(username)).pack(pady=10)

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
        tk.Label(self.frame, text="Edit Pet", font=("Bebas Neue", 20),bg="#B7D8E6",fg="white").grid(row=0, column=0, columnspan=2, pady=20)
        tk.Label(self.frame, text="Name", font=("Bebas Neue", 10),bg="#B7D8E6",fg="white").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        pet_name = tk.Entry(self.frame)
        pet_name.insert(0, pet['name'])
        pet_name.grid(row=1, column=1, padx=10, pady=5)
        tk.Label(self.frame, text="Species", font=("Bebas Neue", 10),bg="#B7D8E6",fg="white").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        species_options = ["Dog", "Cat"]
        pet_species = Combobox(self.frame, values=species_options, state="readonly")
        pet_species.set(pet['species'])
        pet_species.grid(row=2, column=1, padx=10, pady=5)
        tk.Label(self.frame, text="Age", font=("Bebas Neue", 10),bg="#B7D8E6",fg="white").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        pet_age = tk.Entry(self.frame)
        pet_age.insert(0, pet['age'])
        pet_age.grid(row=3, column=1, padx=10, pady=5)
        tk.Label(self.frame, text="Upload Picture", font=("Bebas Neue", 10),bg="#B7D8E6",fg="white").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        picture_path_label = tk.Label(self.frame, text=pet['picture_path'] or "No file selected", font=("Bebas Neue", 10),bg="#B7D8E6",fg="white")
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
        # Validate input fields
            if not all([username, new_name, new_species, new_age]):
                raise ValueError("All fields are required.")
        
        # Validate and convert age
            new_age = int(new_age) if new_age.isdigit() else None
            if new_age is None:
                raise ValueError("Age must be a number.")
        
        # Get user ID
            user_id = db.get_user_id(username)
            if not user_id:
                raise ValueError("User not found.")
        
        # Update pet details in the pets table
            db.edit_pet(user_id, old_name, new_name, new_species, new_age, new_picture_path)
        
        # Update pet name in service history, grooming services, and daycare
            db.update_pet_name_in_service_history(user_id, old_name, new_name)
            db.update_pet_name_in_grooming_services(user_id, old_name, new_name)
            db.update_pet_name_in_daycare_services(user_id, old_name, new_name)
        
        # Show success message and reload the pet management screen
            messagebox.showinfo("Success", "Pet details updated successfully!")
            self.ManageMyPets(username)
        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update pet details: {e}")

    def GroomingServices(self, username):
        self.clear_frame()
        tk.Label(self.frame, text="Grooming Services",font=("Bebas Neue", 20),bg="#B7D8E6",fg="white").grid(row=0, column=0, columnspan=2, pady=20)

    # Fetch user's pets
        pets = db.get_user_pets(username)
        if not pets:
            tk.Label(self.frame, text="No pets registered. Please add a pet first.", font=("Bebas Neue", 10),bg="#B7D8E6",fg="white").grid(row=1, column=0, columnspan=2, pady=10)
            tk.Button(self.frame, text="Back", command=lambda: self.load_user_dashboard(username)).grid(row=2, column=0, columnspan=2, pady=10)
            return

    # Pet selection dropdown
        tk.Label(self.frame, text="Select Pet:", font=("Bebas Neue", 10),bg="#B7D8E6",fg="white").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        pet_options = [pet["name"] for pet in pets]
        selected_pet = tk.StringVar()
        pet_dropdown = ttk.Combobox(self.frame, values=pet_options, textvariable=selected_pet, state="readonly")
        pet_dropdown.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    # Grooming services radio buttons
        tk.Label(self.frame, text="Select Service:", font=("Bebas Neue", 10),bg="#B7D8E6",fg="white").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        selected_service = tk.StringVar()
        services = ["Basic Grooming", "Full Grooming", "Nail Clipping", "Ear Cleaning", "Bath & Blow Dry"]
        for i, service in enumerate(services):
            tk.Radiobutton(self.frame, text=service, variable=selected_service, value=service).grid(row=5 + i, column=0, padx=10, pady=2, sticky="w")

    # Date selection dropdown
        tk.Label(self.frame, text="Select Date:", font=("Bebas Neue", 10),bg="#B7D8E6",fg="white").grid(row=4, column=1, padx=10, pady=5, sticky="w")
        available_dates = ["2025-03-25", "2025-03-26", "2025-03-27", "2025-03-28"]  # Example dates
        selected_date = tk.StringVar(value=available_dates[0])
        date_dropdown = ttk.Combobox(self.frame, textvariable=selected_date, values=available_dates, state="readonly")
        date_dropdown.grid(row=5, column=1, padx=10, pady=5, sticky="w")

    # Book button
        tk.Button(self.frame,text="Book Service",font=("Arial", 12, "bold"),command=lambda: self.book_grooming(username, selected_pet.get(), selected_service.get(), selected_date.get())).grid(row=10, column=0, columnspan=2, pady=10)

    # My grooming appointments
        tk.Label(self.frame, text="My Grooming Appointments", font=("Bebas Neue", 20),bg="#B7D8E6",fg="white").grid(row=11, column=0, columnspan=2, pady=20)
        appointments = db.get_grooming_appointments(username, status="Pending")  # Fetch only pending appointments
        if appointments:
            for i, appointment in enumerate(appointments):
                tk.Label(self.frame, text=f"{i + 1}. {appointment['pet_name']} - {appointment['service_type']} - {appointment['service_date']}", font=("Bebas Neue", 10),bg="#B7D8E6",fg="white").grid(row=12 + i, column=0, padx=10, pady=5, sticky="w")
                tk.Button(
                self.frame,
                text="Cancel",
                command=lambda appointment_id=appointment['id']: self.cancel_grooming(username, appointment_id)
            ).grid(row=12 + i, column=1, padx=10, pady=5)
        else:
            tk.Label(self.frame, text="No grooming appointments found.", font=("Bebas Neue", 10),bg="#B7D8E6",fg="white").grid(row=12, column=0, columnspan=2, pady=5)

    # Back button
        tk.Button(self.frame, text="Back", font=("Arial", 12, "bold"), command=lambda: self.load_user_dashboard(username)).grid(row=20, column=0, columnspan=2, pady=10)

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
            status = "Pending"
            db.add_grooming_service(user_id, pet_name, selected_service, selected_date, status)

        # Show success message
            messagebox.showinfo("Success", f"Grooming service booked for {pet_name} on {selected_date}: {selected_service}")
            self.GroomingServices(username)  # Refresh the grooming services page
        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to book grooming service: {e}")

    def create_scrollable_frame(self):
        """Create a scrollable frame inside the main frame with a larger scroll area."""
        self.canvas = tk.Canvas(self.frame, bg="#B7D8E6", highlightthickness=0, height=600)  # Increased height
        scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#B7D8E6")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def Daycare(self, username):
        self.clear_frame()
        self.create_scrollable_frame()
        tk.Label(self.scrollable_frame, text="Daycare Booking", font=("Bebas Neue", 20), bg="#B7D8E6", fg="white").pack(pady=20)

        # Fetch user's pets
        pets = db.get_user_pets(username)
        if not pets:
            tk.Label(self.scrollable_frame, text="No pets registered. Please add a pet first.", font=("Bebas Neue", 10), bg="#B7D8E6", fg="white").pack(pady=10)
            tk.Button(self.scrollable_frame, text="Back", command=lambda: self.load_user_dashboard(username)).pack(pady=10)
            return

        # Pet selection dropdown
        tk.Label(self.scrollable_frame, text="Select Pet:", font=("Bebas Neue", 10), bg="#B7D8E6", fg="white").pack(pady=5)
        pet_names = [pet["name"] for pet in pets]
        selected_pet = tk.StringVar()
        pet_dropdown = Combobox(self.scrollable_frame, textvariable=selected_pet, values=pet_names, state="readonly")
        pet_dropdown.pack(pady=5)

        # Date selection using Calendar
        tk.Label(self.scrollable_frame, text="Select Date:", font=("Bebas Neue", 10), bg="#B7D8E6", fg="white").pack(pady=5)
        calendar = Calendar(self.scrollable_frame, selectmode="day")
        calendar.pack(pady=5)

        # Drop-off time
        tk.Label(self.scrollable_frame, text="Drop-off Time:", font=("Bebas Neue", 10), bg="#B7D8E6", fg="white").pack(pady=5)
        drop_off_frame = tk.Frame(self.scrollable_frame)
        drop_off_frame.pack(pady=5)
        drop_off_hour = Combobox(drop_off_frame, values=[f"{i:02}" for i in range(1, 13)], width=5, state="readonly")
        drop_off_hour.set("01")
        drop_off_hour.grid(row=0, column=0, padx=2)
        drop_off_minute = Combobox(drop_off_frame, values=[f"{i:02}" for i in range(0, 60)], width=5, state="readonly")
        drop_off_minute.set("00")
        drop_off_minute.grid(row=0, column=1, padx=2)
        drop_off_ampm = Combobox(drop_off_frame, values=["AM", "PM"], width=5, state="readonly")
        drop_off_ampm.set("AM")
        drop_off_ampm.grid(row=0, column=2, padx=2)

        # Pick-up time
        tk.Label(self.scrollable_frame, text="Pick-up Time:", font=("Bebas Neue", 10), bg="#B7D8E6", fg="white").pack(pady=5)
        pick_up_frame = tk.Frame(self.scrollable_frame)
        pick_up_frame.pack(pady=5)
        pick_up_hour = Combobox(pick_up_frame, values=[f"{i:02}" for i in range(1, 13)], width=5, state="readonly")
        pick_up_hour.set("01")
        pick_up_hour.grid(row=0, column=0, padx=2)
        pick_up_minute = Combobox(pick_up_frame, values=[f"{i:02}" for i in range(0, 60)], width=5, state="readonly")
        pick_up_minute.set("00")
        pick_up_minute.grid(row=0, column=1, padx=2)
        pick_up_ampm = Combobox(pick_up_frame, values=["AM", "PM"], width=5, state="readonly")
        pick_up_ampm.set("AM")
        pick_up_ampm.grid(row=0, column=2, padx=2)

        # Submit button
        tk.Button(
            self.scrollable_frame,
            text="Book Daycare",
            font=("Arial", 12, "bold"),
            command=lambda: self.submit_daycare_booking(
                username,
                selected_pet.get(),
                calendar.get_date(),
                f"{drop_off_hour.get()}:{drop_off_minute.get()} {drop_off_ampm.get()}",
                f"{pick_up_hour.get()}:{pick_up_minute.get()} {pick_up_ampm.get()}"
            )
        ).pack(pady=10)

        # My daycare appointments
        tk.Label(self.scrollable_frame, text="My Daycare Appointments", font=("Bebas Neue", 20), bg="#B7D8E6", fg="white").pack(pady=20)
        appointments = db.get_daycare_appointments(username, status="Pending")  # Fetch only pending appointments
        if appointments:
            for i, appointment in enumerate(appointments):
                tk.Label(self.scrollable_frame, text=f"{i + 1}. {appointment['pet_name']} - {appointment['date']}", font=("Bebas Neue", 10), bg="#B7D8E6", fg="white").pack(pady=5)
                tk.Button(
                    self.scrollable_frame,
                    text="Cancel",
                    command=lambda appointment_id=appointment['id']: self.cancel_daycare(username, appointment_id)
                ).pack(pady=5)  # Ensure the button is displayed
        else:
            tk.Label(self.scrollable_frame, text="No daycare appointments found.", font=("Bebas Neue", 10), bg="#B7D8E6", fg="white").pack(pady=5)

        # Back button
        tk.Button(self.scrollable_frame, text="Back", command=lambda: self.load_user_dashboard(username)).pack(pady=10)

    def cancel_daycare(self, username, appointment_id):
        """Cancel a daycare appointment by its ID."""
        try:
            db.cancel_daycare_appointment(appointment_id)  # Correct function call
            messagebox.showinfo("Success", "Daycare appointment canceled successfully!")
            self.Daycare(username)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to cancel appointment: {e}")
    
    def submit_daycare_booking(self, username, pet_name, date, drop_off_time, pick_up_time):
        try:
            if not pet_name:
                raise ValueError("Please select a pet.")
            if not date:
                raise ValueError("Please select a date.")
            if not drop_off_time or not pick_up_time:
                raise ValueError("Please specify both drop-off and pick-up times.")

            user_id = db.get_user_id(username)
            if not user_id:
                raise ValueError("User not found.")

        # Save to service history with status 'Pending'
            status = "Pending"  # Change this to 'Done' if you want it to be marked as completed immediately
            db.add_service_history(
            user_id,
            pet_name,
            "Daycare",
            date=date,
            details=f"Drop-off: {drop_off_time}, Pick-up: {pick_up_time}",
            status=status
        )

            messagebox.showinfo("Success", f"Daycare booked for {pet_name} on {date}.\nDrop-off: {drop_off_time}, Pick-up: {pick_up_time}")
            self.Daycare(username)
        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to book daycare: {e}")

    def ServiceHistory(self, username):
        self.clear_frame()
        tk.Label(self.frame, text="Service History", font=("Bebas Neue", 20),bg="#B7D8E6",fg="white").pack(pady=20)

        user_id = db.get_user_id(username)
        if not user_id:
            tk.Label(self.frame, text="User not found.", font=("Bebas Neue", 10),bg="#B7D8E6",fg="white").pack(pady=10)
            tk.Button(self.frame, text="Back", command=lambda: self.load_user_dashboard(username)).pack(pady=10)
            return

    # Fetch grooming and daycare services with status 'Done'
        grooming_history = db.get_grooming_services_done(user_id)
        daycare_history = db.get_daycare_services_done(user_id)

        if not grooming_history and not daycare_history:
            tk.Label(self.frame, text="No service history found.", font=("Bebas Neue", 10),bg="#B7D8E6",fg="white").pack(pady=10)
        else:
        # Display Grooming Services
            if grooming_history:
                tk.Label(self.frame, text="Grooming Services", font=("Bebas Neue", 20),bg="#B7D8E6",fg="white").pack(pady=20, anchor="w")
                for record in grooming_history:
                    details = f"Pet: {record['pet_name']}\nDate: {record['date']}\nService: {record['service_type']}"
                    tk.Label(self.frame, text=details, justify="left", font=("Bebas Neue", 10),bg="#B7D8E6",fg="white").pack(pady=5, anchor="w")
            else:
                tk.Label(self.frame, text="No grooming services found.", font=("Bebas Neue", 10),bg="#B7D8E6",fg="white").pack(pady=5, anchor="w")

        # Display Daycare Services
            if daycare_history:
                tk.Label(self.frame, text="Daycare Services", font=("Bebas Neue", 20),bg="#B7D8E6",fg="white").pack(pady=20, anchor="w")
                for record in daycare_history:
                    details = f"Pet: {record['pet_name']}\nDate: {record['date']}\nDetails: {record['details']}"
                    tk.Label(self.frame, text=details, justify="left", font=("Bebas Neue", 10),bg="#B7D8E6",fg="white").pack(pady=5, anchor="w")
            else:
                tk.Label(self.frame, text="No daycare services found.", font=("Bebas Neue", 10),bg="#B7D8E6",fg="white").pack(pady=5, anchor="w")

        tk.Button(self.frame, text="Back", command=lambda: self.load_user_dashboard(username)).pack(pady=10)
 
    
    def update_service_status(self, record_id):
        try:
            db.update_service_status(record_id, "Done")
            messagebox.showinfo("Success", "Service status updated to 'Done'!")
            self.ServiceHistory("admin")  # Reload the service history for admin
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update status: {e}")

    def AddPet(self, username):
        self.clear_frame()
        tk.Label(self.frame, text="Add Pet", font=("Bebas Neue", 20),bg="#B7D8E6",fg="white").grid(row=0, column=0, columnspan=2, pady=20)
        tk.Label(self.frame, text="Name", font=("Bebas Neue", 10),bg="#B7D8E6",fg="white").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        pet_name = tk.Entry(self.frame)
        pet_name.grid(row=1, column=1, padx=10, pady=5)
        tk.Label(self.frame, text="Species", font=("Bebas Neue", 10),bg="#B7D8E6",fg="white").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        species_options = ["Dog", "Cat"]
        pet_species = Combobox(self.frame, values=species_options, state="readonly")
        pet_species.grid(row=2, column=1, padx=10, pady=5)
        tk.Label(self.frame, text="Age", font=("Bebas Neue", 10),bg="#B7D8E6",fg="white").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        pet_age = tk.Entry(self.frame)
        pet_age.grid(row=3, column=1, padx=10, pady=5)
        tk.Label(self.frame, text="Upload Picture", font=("Bebas Neue", 10),bg="#B7D8E6",fg="white").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        picture_path_label = tk.Label(self.frame, text="No file selected", font=("Bebas Neue", 10),bg="#B7D8E6",fg="white")
        picture_path_label.grid(row=4, column=1, padx=10, pady=5)
        upload_button = tk.Button(self.frame, text="Upload Picture", command=lambda: self.upload_picture(picture_path_label))
        upload_button.grid(row=5, column=1, padx=10, pady=5)
        save_button = tk.Button(
            self.frame,
            text="Save",
            font=("Arial", 12, "bold"),
            command=lambda: self.submit_pet(username, pet_name.get(), pet_species.get(), pet_age.get(), picture_path_label.cget("text"))
        )
        save_button.grid(row=6, column=0, padx=10, pady=10)
        back_button = tk.Button(self.frame, text="Cancel", font=("Arial", 12, "bold"), command=lambda: self.ManageMyPets(username))
        back_button.grid(row=6, column=1, padx=10, pady=10)

    def upload_picture(self, label):
        """Open a file dialog to select a picture and update the label with the file path."""
        file_path = filedialog.askopenfilename(
            title="Select a Picture",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
        )
        if file_path:
            label.config(text=file_path)

    def submit_pet(self, username, name, species, age, picture_path=None):
        """Submit a new pet to the database."""
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

window = tk.Tk()
PetServiceManagementSystem(window)
window.mainloop()