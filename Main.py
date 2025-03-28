import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog, ttk
from tkinter.ttk import Combobox
import database as db
import random
from PIL import Image, ImageTk  # Add this import for image handling
from tkcalendar import Calendar  # Import Calendar for date selection

# Initialize the database connection
db.connect_db()

class PetServiceManagementSystem:
    # Button style configuration
    button_style = {
        "bg": "#EDCC6F",  # Button background color
        "fg": "#2B2C41",  # Button text color
        "font": ("Century Gothic", 15),
        "width": 30,      # Equal width for buttons
        "padx": 10,       # Horizontal padding inside the button
        "pady": 10        # Vertical padding inside the button
    }
        
    def __init__(self, window):
        # Initialize the main window and set up the layout
        self.window = window
        self.window.title("PET SERVICE MANAGEMENT SYSTEM")
        self.window.geometry("1200x700")
        self.window.configure(bg="#D2EBFF")

        # Title label
        tk.Label(window, text="🐾 Pet Service Management System 🐾", font=("Broadway", 30), bg="#88CAFC", fg="#2B2C41", padx=25, pady=20).pack()

        # Main frame for buttons
        self.frame = tk.Frame(self.window, bg="#FFFFED")
        self.frame.pack(padx=70, pady=70)

        # Create a box frame for User and Admin buttons
        button_box = tk.Frame(self.frame, bg="#FFFFED", bd=2)
        button_box.pack(pady=20, padx=20)
        
        # Main buttons for User and Admin access with icons
        tk.Button(button_box, text="USER 👤", command=self.User, **self.button_style).pack(pady=10)
        tk.Button(button_box, text="ADMIN 🔐", command=self.Admin, **self.button_style).pack(pady=10)

        self.appointments = []

    def clear_frame(self):
        # Clear all widgets from the current frame
        for widget in self.frame.winfo_children():
            widget.destroy()

    def back_to_main(self):
        # Return to the main menu by clearing the frame
        self.clear_frame()
        self.frame.pack(padx=70, pady=70)
        
        # Recreate the button box
        button_box = tk.Frame(self.frame, bg="#FFFFED", bd=2)
        button_box.pack(pady=20, padx=20)
        tk.Button(button_box, text="USER 👤", command=self.User, **self.button_style).pack(pady=10)
        tk.Button(button_box, text="ADMIN 🔐", command=self.Admin, **self.button_style).pack(pady=10)

    def User(self):
        # Display the user login interface
        self.clear_frame()
        inner = tk.Frame(self.frame, bg="#FFFFED", width=410, height=280)
        inner.pack_propagate(False)  # Prevent the frame from resizing to fit its contents
        inner.pack(pady=20)

        # Title label
        tk.Label(inner, text="🦴 USER LOGIN 🦴", font=("Century Gothic", 20, "bold"), bg="#FFFFED", fg="#2B2C41").pack(padx=20, pady=20)

        # Create buttons with the specified styles
        tk.Button(inner, text="Login", command=self.UserLogIn, **self.button_style).pack(pady=5)
        tk.Button(inner, text="Create Account", command=self.UserRegister, **self.button_style).pack(pady=5)
        tk.Button(inner, text="Back", command=self.back_to_main, **self.button_style).pack(pady=5)

    def Admin(self):
        # Display the admin login interface
        self.clear_frame()
        inner = tk.Frame(self.frame, bg="#FFFFED", width=410, height=350)
        inner.pack_propagate(False)  # Prevent the frame from resizing to fit its contents
        inner.pack(pady=20)
        
        # Title label
        tk.Label(inner, text="🦴 ADMIN LOGIN 🦴", font=("Century Gothic", 20, "bold"), bg="#FFFFED", fg="#2B2C41").grid(row=0, column=0, padx=5, pady=20, columnspan=2)
        tk.Label(inner, text="Username", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").grid(row=1, column=0, padx=5, pady=10)
        
        # Username label
        admin_username = tk.Entry(inner, font=("Century Gothic", 15), bg="#404066", fg="#88cafc", bd=2, relief="groove")  # Entry with border
        admin_username.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(inner, text="Password", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").grid(row=2, column=0, padx=5, pady=10)
        
        # Password label
        admin_password = tk.Entry(inner, show="*", font=("Century Gothic", 15), bg="#404066", fg="#88cafc", bd=2, relief="groove")  # Entry with border
        admin_password.grid(row=2, column=1, padx=5, pady=10)
        
        # Login and Back button
        tk.Button(inner, text="Login", bg="#EDCC6F", fg="#2B2C41", width=15, font=("Century Gothic", 15), 
                  command=lambda: self.AdminLogin(admin_username.get(), admin_password.get())).grid(row=3, column=0, padx=5, pady=10)
        tk.Button(inner, text="Back", command=self.back_to_main,
                bg="#EDCC6F", fg="#2B2C41", font=("Century Gothic", 15), width=15).grid(row=3, column=1, padx=5, pady=10)

    def AdminLogin(self, username, password):
        # Validate admin login credentials
        if username == "admin" and password == "admin":
            messagebox.showinfo("Success", "Admin login successful!")
            self.load_admin_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid admin credentials.")

    def load_admin_dashboard(self):
        # Load the admin dashboard with management options
        self.clear_frame()

        # Title label
        tk.Label(self.frame, text="🧶 ADMIN DASHBOARD 🧶", font=("Century Gothic", 20, "bold"), bg="#FFFFED", fg="#2B2C41").pack(pady=20)

        # Create a box frame for buttons
        button_box = tk.Frame(self.frame, bg="#FFFFED", bd=0)  # Create a frame with a border
        button_box.pack(pady=20, padx=70)

        # Management option buttons with updated font and style
        tk.Button(button_box, text="Manage Users", command=self.manage_all_users, font=("Century Gothic", 15), 
                bg="#EDCC6F", fg="#2B2C41", width=30).pack(pady=5)
        tk.Button(button_box, text="Manage Pets", command=self.manage_all_pets, font=("Century Gothic", 15), 
                bg="#EDCC6F", fg="#2B2C41", width=30).pack(pady=5)
        tk.Button(button_box, text="Manage Grooming Appointments", command=self.manage_grooming_appointments, font=("Century Gothic", 15), 
                bg="#EDCC6F", fg="#2B2C41", width=30).pack(pady=5)
        tk.Button(button_box, text="Manage Daycare Booking", command=self.manage_daycare_booking, font=("Century Gothic", 15), 
                bg="#EDCC6F", fg="#2B2C41", width=30).pack(pady=5)
        tk.Button(button_box, text="View Service History", command=self.view_service_history, font=("Century Gothic", 15), 
                bg="#EDCC6F", fg="#2B2C41", width=30).pack(pady=5)

        # Back button
        tk.Button(self.frame, text="Back", command=self.back_to_main, font=("Century Gothic", 15), 
                bg="#EDCC6F", fg="#2B2C41", width=25).pack(pady=20)
    
    def load_user_dashboard(self, username):
        # Load the user dashboard with options for managing pets and services
        self.clear_frame()

        # Title label
        tk.Label(self.frame, text=f"👋 Welcome, {username} 👋", font=("Century Gothic", 20, "bold"), bg="#FFFFED", fg="#2B2C41").pack(pady=20)

        # Create a box frame for buttons
        button_box = tk.Frame(self.frame, bg="#FFFFED", bd=0)  # Create a frame without a border
        button_box.pack(pady=20, padx=70)

        # User management option buttons
        tk.Button(button_box, text="Manage My Pets", command=lambda: self.ManageMyPets(username), font=("Century Gothic", 15), 
                bg="#EDCC6F", fg="#2B2C41", width=25).pack(pady=5)
        tk.Button(button_box, text="Grooming Services", command=lambda: self.GroomingServices(username), font=("Century Gothic", 15), 
                bg="#EDCC6F", fg="#2B2C41", width=25).pack(pady=5)
        tk.Button(button_box, text="Daycare", command=lambda: self.Daycare(username), font=("Century Gothic", 15), 
                bg="#EDCC6F", fg="#2B2C41", width=25).pack(pady=5)
        tk.Button(button_box, text="Service History", command=lambda: self.ServiceHistory(username), font=("Century Gothic", 15), 
                bg="#EDCC6F", fg="#2B2C41", width=25).pack(pady=5)

        # Back button
        tk.Button(self.frame, text="Back", command=self.User, font=("Century Gothic", 15), 
                bg="#EDCC6F", fg="#2B2C41", width=25).pack(pady=20)

    def manage_all_users(self):
        # Display and manage all registered users
        self.clear_frame()
        
        # Title label with updated font and color
        tk.Label(self.frame, text="👥 MANAGE USERS 👥", font=("Century Gothic", 20, "bold"), bg="#FFFFED", fg="#2B2C41").pack(pady=20)

        # Create a box frame for user management
        user_box = tk.Frame(self.frame, bg="#FFFFED", bd=0)  # Create a frame without a border
        user_box.pack(pady=20, padx=30)

        users = db.get_all_users()  # Fetch all users from the database
        if users:
            for user in users:
                user_frame = tk.Frame(user_box, bg="#FFFFED", bd=0)  # Frame for each user
                user_frame.pack(fill=tk.X, padx=10, pady=5)

                details = f"ID: {user['id']}, Username: {user['username']}"
                tk.Label(user_frame, text=details, justify="left", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").pack(side=tk.LEFT, padx=10)

                # Button to delete the user with updated style
                tk.Button(user_frame, text="Delete", command=lambda user_id=user['id']: self.delete_user(user_id), 
                        font=("Century Gothic", 15), bg="#EDCC6F", fg="#2B2C41").pack(side=tk.RIGHT, padx=10)
        else:
            tk.Label(self.frame, text="No users found.", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").pack(pady=10)

        # Back button with updated style
        tk.Button(self.frame, text="Back", command=self.load_admin_dashboard, font=("Century Gothic", 15), 
                bg="#EDCC6F", fg="#2B2C41").pack(pady=20)
    
    def manage_all_pets(self):
        # Display and manage all registered pets
        self.clear_frame()
        
        # Title label with updated font and color
        tk.Label(self.frame, text="🐕 MANAGE PETS 🐈", font=("Century Gothic", 20, "bold"), bg="#FFFFED", fg="#2B2C41").pack(pady=20)

        # Create a box frame for pets
        pet_box = tk.Frame(self.frame, bg="#FFFFED", bd=0)  # Create a frame without a border
        pet_box.pack(pady=20, padx=30)

        pets = db.get_all_pets()  # Fetch all pets from the database
        if pets:
            for pet in pets:
                pet_frame = tk.Frame(pet_box, bg="#FFFFED", bd=0)  # Frame for each pet
                pet_frame.pack(fill=tk.X, padx=10, pady=5)

                details = f"Name: {pet['name']}, Species: {pet['species']}, Owner ID: {pet['user_id']}"
                tk.Label(pet_frame, text=details, justify="left", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").pack(side=tk.LEFT, padx=10)

                # Button to delete the pet
                tk.Button(pet_frame, text="Delete", command=lambda pet_name=pet['name'], user_id=pet['user_id']: self.delete_pet(user_id, pet_name), 
                        font=("Century Gothic", 15), bg="#EDCC6F", fg="#2B2C41").pack(side=tk.RIGHT, padx=10)
        else:
            tk.Label(self.frame, text="No pets found.", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").pack(pady=10)

        # Back button
        tk.Button(self.frame, text="Back", command=self.load_admin_dashboard, font=("Century Gothic", 15), 
                bg="#EDCC6F", fg="#2B2C41").pack(pady=20)

    def delete_user(self, user_id):
        # Delete a user by ID
        try:
            db.delete_user(user_id)
            messagebox.showinfo("Success", "User  deleted successfully!")
            self.manage_all_users()  # Refresh the user list
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete user: {e}")

    def delete_pet(self, user_id, pet_name):
        # Delete a pet by name for a specific user
        try:
            db.delete_pet(user_id, pet_name)
            messagebox.showinfo("Success", f"Pet '{pet_name}' deleted successfully!")
            self.manage_all_pets()  # Refresh the pet list
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete pet: {e}")

    def manage_daycare_booking(self):
        """Display and manage daycare bookings."""
        self.clear_frame()
    
        # Title label
        tk.Label(self.frame, text="📖 MANAGE DAYCARE BOOKINGS 📖", font=("Century Gothic", 20, "bold"), bg="#FFFFED", fg="#2B2C41").pack(pady=20)
    
        # Create a scrollable frame for daycare bookings
        self.canvas = tk.Canvas(self.frame, bg="#FFFFED", width=900, height=500)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#FFFFED")
        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
    
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
    
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="n", width=900)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
    
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
    
        # Fetch all daycare bookings with status = 'Pending'
        bookings = db.get_all_daycare_booking()
        pending_bookings = [booking for booking in bookings if booking["status"] == "Pending"]
    
        if pending_bookings:
            for booking in pending_bookings:
                booking_frame = tk.Frame(self.scrollable_frame, bg="#FFFFED", bd=0)  # Frame for each booking
                booking_frame.pack(fill=tk.X, padx=10, pady=5)
    
                details = (
                    f"ID: {booking['id']} | "
                    f"User ID: {booking['user_id']} | "
                    f"Pet: {booking['pet_name']} | "
                    f"Date: {booking['date']} | "
                    f"Drop-off: {booking['drop_off_time']} | "
                    f"Pick-up: {booking['pick_up_time']} | "
                    f"Status: {booking['status']}"
                )
                tk.Label(booking_frame, text=details, justify="left", font=("Century Gothic", 10), bg="#FFFFED", fg="#2B2C41").pack(side=tk.LEFT, padx=10)
    
                # Button to mark the booking as "Done"
                tk.Button(
                    booking_frame,
                    text="Mark as Done",
                    command=lambda booking_id=booking['id']: self.update_daycare_status(booking_id),
                    font=("Century Gothic", 15),
                    bg="#EDCC6F",
                    fg="#2B2C41"
                ).pack(side=tk.RIGHT, padx=10)
        else:
            tk.Label(self.scrollable_frame, text="No pending daycare bookings found.", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").pack(pady=10)
    
        # Back button centered at the bottom
        back_button_frame = tk.Frame(self.scrollable_frame, bg="#FFFFED")  # Create a frame for the back button
        back_button_frame.pack(pady=20)  # Add padding around the button frame
        tk.Button(back_button_frame, text="Back", command=self.load_admin_dashboard, font=("Century Gothic", 15), 
                  bg="#EDCC6F", fg="#2B2C41").pack()  # Center the button in the frame
    
    def manage_grooming_appointments(self):
        # Display and manage grooming appointments
        self.clear_frame()
        
        # Title label
        tk.Label(self.frame, text="📖 MANAGE GROOMING APPOINTMENTS 📖", font=("Century Gothic", 20, "bold"), bg="#FFFFED", fg="#2B2C41").pack(pady=20)

        # Create a scrollable frame for grooming appointments
        self.canvas = tk.Canvas(self.frame, bg="#FFFFED", width=900, height=500)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#FFFFED")
        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="n", width=900)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Fetch all grooming appointments with status = 'Pending'
        appointments = db.get_all_grooming_appointments()
        pending_appointments = [appt for appt in appointments if appt["status"] == "Pending"]

        if pending_appointments:
            for appointment in pending_appointments:
                appointment_frame = tk.Frame(self.scrollable_frame, bg="#FFFFED", bd=0)  # Frame for each appointment
                appointment_frame.pack(fill=tk.X, padx=10, pady=5)

                details = (
                    f"ID: {appointment['id']} | "
                    f"User  ID: {appointment['user_id']} | "
                    f"Pet: {appointment['pet_name']} | "
                    f"Service: {appointment['service_type']} | "
                    f"Date: {appointment['service_date']} | "
                    f"Status: {appointment['status']}"
                )
                tk.Label(appointment_frame, text=details, justify="left", font=("Century Gothic", 10), bg="#FFFFED", fg="#2B2C41").pack(side=tk.LEFT, padx=10)

                # Button to mark the appointment as "Done"
                tk.Button(
                    appointment_frame,
                    text="Mark as Done",
                    command=lambda appointment_id=appointment['id']: self.update_grooming_status(appointment_id),
                    font=("Century Gothic", 10),
                    bg="#EDCC6F",
                    fg="#2B2C41"
                ).pack(side=tk.RIGHT, padx=10)
        else:
            tk.Label(self.scrollable_frame, text="No pending grooming appointments found.", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").pack(pady=10)

        # Back button centered at the bottom
        back_button_frame = tk.Frame(self.scrollable_frame, bg="#FFFFED")  # Create a frame for the back button
        back_button_frame.pack(pady=20)  # Add padding around the button frame
        tk.Button(back_button_frame, text="Back", command=self.load_admin_dashboard, font=("Century Gothic", 15), 
                bg="#EDCC6F", fg="#2B2C41").pack()  # Center the button in the frame

    def update_grooming_status(self, appointment_id):
        # Update the status of a grooming appointment to 'Done'
        try:
            db.update_grooming_status(appointment_id, "Done")
            messagebox.showinfo("Success", "Grooming appointment marked as 'Done'!")
            self.manage_grooming_appointments()  # Refresh the grooming appointments menu
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update appointment status: {e}")

    def update_service_status(self, record_id):
        """Update the status of a daycare booking to 'Done'."""
        try:
            db.update_daycare_status(record_id, "Done")
            messagebox.showinfo("Success", "Daycare booking marked as 'Done'!")
            self.manage_daycare_booking()  # Refresh the daycare bookings menu
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update status: {e}")
    
    def update_daycare_status(self, booking_id):
        """Mark a daycare booking as 'Done'."""
        try:
            db.update_daycare_status(booking_id, "Done")
            messagebox.showinfo("Success", "Daycare booking marked as 'Done'!")
            self.manage_daycare_booking()  # Refresh the daycare bookings menu
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update booking status: {e}")

    def view_service_history(self):
        """Display the service history for all users."""
        self.clear_frame()
        
        # Title label with updated font and color
        tk.Label(self.frame, text="SERVICE HISTORY", font=("Century Gothic", 20, "bold"), bg="#FFFFED", fg="#2B2C41").pack(pady=20)

        # Create a scrollable frame for service history
        self.canvas = tk.Canvas(self.frame, bg="#FFFFED", width=1100, height=500)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#FFFFED")
        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="n", width=1100)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Fetch all service history records
        history = db.get_all_service_history()
        if not history:
            tk.Label(self.scrollable_frame, text="No service history found.", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").pack(pady=10)
        else:
            for record in history:
                details = (
                    f"ID: {record['id']} | "
                    f"Pet: {record['pet_name']} | "
                    f"Service: {record['service_type']} | "
                    f"Date: {record['date']} | "
                    f"Details: {record['details']} | "
                    f"Status: {record['status']}"
                )
                tk.Label(self.scrollable_frame, text=details, justify="left", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").pack(pady=5)

        # Back button centered at the bottom
        back_button_frame = tk.Frame(self.scrollable_frame, bg="#FFFFED")  # Create a frame for the back button
        back_button_frame.pack(pady=20)  # Add padding around the button frame
        tk.Button(back_button_frame, text="Back", command=self.load_admin_dashboard, font=("Century Gothic", 15), 
                bg="#EDCC6F", fg="#2B2C41").pack()  # Center the button in the frame

    def UserLogIn(self):
        # Display the user login interface.
        self.clear_frame()
 
        # Title label
        tk.Label(self.frame, text="🐶 LOGIN 🐶", font=("Century Gothic", 20, "bold"), bg="#FFFFED", fg="#2B2C41").grid(row=0, column=0, padx=5, pady=20, columnspan=2)

        # Username label
        tk.Label(self.frame, text="Username", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").grid(row=1, column=0, padx=5, pady=10)
        username_entry = tk.Entry(self.frame, font=("Century Gothic", 15), bg="#404066", fg="#88cafc", bd=2, relief="groove")  # Entry with border
        username_entry.grid(row=1, column=1, padx=5, pady=5)

        # Password label
        tk.Label(self.frame, text="Password", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").grid(row=2, column=0, padx=5, pady=10)
        password_entry = tk.Entry(self.frame, show="*", font=("Century Gothic", 15), bg="#404066", fg="#88cafc", bd=2, relief="groove")  # Entry with border
        password_entry.grid(row=2, column=1, padx=5, pady=5)

        # Login and Back button
        tk.Button(self.frame, text="Login", command=lambda: self.Login(username_entry.get(), password_entry.get()), 
                bg="#EDCC6F", fg="#2B2C41", font=("Century Gothic", 15), width=15).grid(row=3, column=0, padx=5, pady=10)
        tk.Button(self.frame, text="Back", command=self.User,
                bg="#EDCC6F", fg="#2B2C41", font=("Century Gothic", 15), width=15).grid(row=3, column=1, padx=5, pady=10)

    def UserRegister(self):
        # Display the user registration interface.
        self.clear_frame()

        # Title label
        tk.Label(self.frame, text="🐱 CREATE ACCOUNT 🐱", font=("Century Gothic", 20, "bold"), bg="#FFFFED", fg="#2B2C41").grid(row=0, column=0, padx=5, pady=20, columnspan=2)
        tk.Label(self.frame, text="Username", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").grid(row=1, column=0, padx=5, pady=10)
        
        # Username label
        username_entry = tk.Entry(self.frame, font=("Century Gothic", 15), bg="#404066", fg="#88cafc", bd=2, relief="groove")  # Entry with border
        username_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(self.frame, text="Password", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").grid(row=2, column=0, padx=5, pady=10)
        
        # Password label
        password_entry = tk.Entry(self.frame, show="*", font=("Century Gothic", 15), bg="#404066", fg="#88cafc", bd=2, relief="groove")  # Entry with border
        password_entry.grid(row=2, column=1, padx=5, pady=10)
        
        # Login and Back button
        tk.Button(self.frame, text="Register", command=lambda: self.Register(username_entry.get(), password_entry.get()), 
                bg="#EDCC6F", fg="#2B2C41", font=("Century Gothic", 15), width=15).grid(row=3, column=0, padx=5, pady=10)
        tk.Button(self.frame, text="Back", command=self.User,
                bg="#EDCC6F", fg="#2B2C41", font=("Century Gothic", 15), width=15).grid(row=3, column=1, padx=5, pady=10)

    def Register(self, username, password):
        # Register a new user in the system.
        if username and password:
            try:
                user_id = db.insert_user(username, password)
                messagebox.showinfo("Success", f"User  registered successfully! Your ID is: {user_id}")
                self.UserLogIn()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    def Login(self, username, password):
        # Validate user login credentials.
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
    # Manage the user's pets, including viewing, editing, and deleting pets.
        self.clear_frame()
    
    # Title label with updated font and color
        tk.Label(self.frame, text="MANAGE MY PETS", font=("Century Gothic", 24), bg="#FFFFED", fg="#2B2C41").pack(pady=20)

    # Create a scrollable frame for pets
        self.canvas = tk.Canvas(self.frame, bg="#FFFFED", width=500, height=500, bd=0)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#FFFFED")
        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
    
        self.scrollable_frame.bind(
        "<Configure>",
        lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="n", width=500)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        pets = db.get_user_pets(username)
        if pets:
            for pet in pets:
                pet_frame = tk.Frame(self.scrollable_frame, bg="#FFFFED", bd=1, relief="solid")  # Frame for each pet
                pet_frame.pack(fill=tk.X, padx=10, pady=10)

            # Display pet details
                details_frame = tk.Frame(pet_frame, bg="#FFFFED")
                details_frame.pack(side=tk.LEFT, padx=10, pady=10)

                details = f"Name: {pet['name']}\nSpecies: {pet['species']}\nAge: {pet['age']}"
                tk.Label(details_frame, text=details, justify="left", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").pack(anchor="w")

            # Display pet image
                image_frame = tk.Frame(pet_frame, bg="#FFFFED")
                image_frame.pack(side=tk.RIGHT, padx=10, pady=10)
                try:
                    if pet["picture_path"]:
                        pil_image = Image.open(pet["picture_path"]).resize((100, 100), Image.LANCZOS)
                        image = ImageTk.PhotoImage(pil_image)
                        image_label = tk.Label(image_frame, image=image, bg="#FFFFED")
                        image_label.image = image  # Keep a reference to avoid garbage collection
                        image_label.pack()
                    else:
                        tk.Label(image_frame, text="No Image", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").pack()
                except Exception as e:
                    print(f"Error loading image: {e}")
                    tk.Label(image_frame, text="Error Displaying Image", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").pack()

            # Add Edit and Delete buttons
                button_frame = tk.Frame(pet_frame, bg="#FFFFED")
                button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
                tk.Button(button_frame, text="Edit", command=lambda pet=pet: self.EditPet(username, pet), font=("Century Gothic", 15), bg="#EDCC6F", fg="#2B2C41").pack(side=tk.LEFT, padx=5)
                tk.Button(button_frame, text="Delete", command=lambda pet=pet: self.DeletePet(username, pet['name']), font=("Century Gothic", 15), bg="#EDCC6F", fg="#2B2C41").pack(side=tk.LEFT, padx=5)
        else:
            tk.Label(self.scrollable_frame, text="No pets registered yet.", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").pack(pady=5)

    # Add Pet button
        tk.Button(self.scrollable_frame, text="Add Pet", font=("Century Gothic", 15), command=lambda: self.AddPet(username), bg="#EDCC6F", fg="#2B2C41").pack(pady=10)

    # Back button
        tk.Button(self.scrollable_frame, text="Back", command=lambda: self.load_user_dashboard(username), font=("Century Gothic", 15), 
              bg="#EDCC6F", fg="#2B2C41").pack(pady=10)

    def DeletePet(self, username, pet_name):
        # Delete a pet from the user's account.
        try:
            user_id = db.get_user_id(username)
            if not user_id:
                raise ValueError("User  not found.")
            db.delete_pet(user_id, pet_name)
            messagebox.showinfo("Success", f"Pet '{pet_name}' deleted successfully!")
            self.ManageMyPets(username)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete pet: {e}")

    def EditPet(self, username, pet):
        # Edit the details of a pet.
        self.clear_frame()
        
        # Title label with updated font and color
        tk.Label(self.frame, text="EDIT PET", font=("Century Gothic", 24), bg="#FFFFED", fg="#2B2C41").pack(pady=20)

        # Create a frame for the input fields
        input_frame = tk.Frame(self.frame, bg="#FFFFED")  # Frame for input fields
        input_frame.pack(pady=20, padx=30)  # Add padding around the input frame

        # Name input
        tk.Label(input_frame, text="Name", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        pet_name = tk.Entry(input_frame, font=("Century Gothic", 15))
        pet_name.insert(0, pet['name'])
        pet_name.grid(row=0, column=1, padx=10, pady=5)

        # Species input
        tk.Label(input_frame, text="Species", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        species_options = ["Dog", "Cat"]
        pet_species = Combobox(input_frame, values=species_options, state="readonly", font=("Century Gothic", 15))
        pet_species.set(pet['species'])
        pet_species.grid(row=1, column=1, padx=10, pady=5)

        # Age input
        tk.Label(input_frame, text="Age", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        pet_age = tk.Entry(input_frame, font=("Century Gothic", 15))
        pet_age.insert(0, pet['age'])
        pet_age.grid(row=2, column=1, padx=10, pady=5)

        # Upload Picture
        tk.Label(input_frame, text="Upload Picture", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        picture_path_label = tk.Label(input_frame, text=pet['picture_path'] or "No file selected", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41")
        picture_path_label.grid(row=3, column=1, padx=10, pady=5)
        upload_button = tk.Button(input_frame, text="Upload Picture", command=lambda: self.upload_picture(picture_path_label), font=("Century Gothic", 15), bg="#EDCC6F", fg="#2B2C41")
        upload_button.grid(row=4, column=1, padx=10, pady=5)

        # Save and Cancel buttons
        button_frame = tk.Frame(self.frame, bg="#FFFFED")  # Create a frame for the buttons
        button_frame.pack(pady=20)  # Add padding around the button frame

        save_button = tk.Button(
            button_frame,
            text="Save",
            font=("Century Gothic", 15),
            command=lambda: self.submit_edit_pet(username, pet['name'], pet_name.get(), pet_species.get(), pet_age.get(), picture_path_label.cget("text")),
            bg="#EDCC6F",
            fg="#2B2C41"
        )
        save_button.pack(side=tk.LEFT, padx=10)

        back_button = tk.Button(button_frame, text="Cancel", font=("Century Gothic", 15), command=lambda: self.ManageMyPets(username), bg="#EDCC6F", fg="#2B2C41")
        back_button.pack(side=tk.LEFT, padx=10)

    def submit_edit_pet(self, username, old_name, new_name, new_species, new_age, new_picture_path=None):
        # Submit the edited details of a pet to the database.
        try:
            # Validate input fields
            if not all([username, new_name, new_species, new_age]) or new_picture_path == "No file selected":
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
        # Manage grooming services for the user's pets.
        self.clear_frame()
        
        # Title label with updated font and color
        tk.Label(self.frame, text="GROOMING SERVICES", font=("Century Gothic", 20, "bold"), bg="#FFFFED", fg="#2B2C41").pack(pady=20)

        # Create a scrollable frame for grooming services
        self.canvas = tk.Canvas(self.frame, bg="#FFFFED", width=500, height=500, bd=0)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#FFFFED")
        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="n", width=500)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Fetch user's pets
        pets = db.get_user_pets(username)
        if not pets:
            tk.Label(self.scrollable_frame, text="No pets registered. Please add a pet first.", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").pack(pady=10)
            tk.Button(self.scrollable_frame, text="Back", command=lambda: self.load_user_dashboard(username), font=("Century Gothic", 15), 
                    bg="#EDCC6F", fg="#2B2C41").pack(pady=10)
            return

        # Pet selection dropdown
        tk.Label(self.scrollable_frame, text="Select Pet:", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").pack(pady=5)
        pet_names = [pet["name"] for pet in pets]
        selected_pet = tk.StringVar()
        pet_dropdown = ttk.Combobox(self.scrollable_frame, textvariable=selected_pet, values=pet_names, state="readonly", font=("Century Gothic", 15))
        pet_dropdown.pack(pady=5)

        # Grooming services radio buttons
        tk.Label(self.scrollable_frame, text="Select Service:", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").pack(pady=5)
        selected_service = tk.StringVar()
        services = ["Basic Grooming", "Full Grooming", "Nail Clipping", "Ear Cleaning", "Bath & Blow Dry"]
        for i, service in enumerate(services):
            tk.Radiobutton(self.scrollable_frame, text=service, variable=selected_service, value=service, font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").pack(anchor="w", padx=10)

        # Date selection using Calendar
        tk.Label(self.scrollable_frame, text="Select Date:", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").pack(pady=5)
        calendar = Calendar(self.scrollable_frame, selectmode="day")
        calendar.pack(pady=5)

        # Book button
        tk.Button(self.scrollable_frame, text="Book Service", font=("Century Gothic", 15), 
                command=lambda: self.book_grooming(username, selected_pet.get(), selected_service.get(), calendar.get_date()), 
                bg="#EDCC6F", fg="#2B2C41").pack(pady=10)

        # My grooming appointments
        tk.Label(self.scrollable_frame, text="My Grooming Appointments", font=("Century Gothic", 20), bg="#FFFFED", fg="#2B2C41").pack(pady=20)
        appointments = db.get_grooming_appointments(username, status="Pending")  # Fetch only pending appointments
        if appointments:
            for i, appointment in enumerate(appointments):
                tk.Label(self.scrollable_frame, text=f"{i + 1}. {appointment['pet_name']} - {appointment['service_type']} - {appointment['service_date']}", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").pack(pady=5)
                tk.Button(
                    self.scrollable_frame,
                    text="Cancel",
                    command=lambda appointment_id=appointment['id']: self.cancel_grooming(username, appointment_id),
                    font=("Century Gothic", 15),
                    bg="#EDCC6F",
                    fg="#2B2C41"
                ).pack(pady=5)  # Ensure the button is displayed
        else:
            tk.Label(self.scrollable_frame, text="No grooming appointments found.", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").pack(pady=5)

        # Back button centered at the bottom
        back_button_frame = tk.Frame(self.scrollable_frame, bg="#D2EBFF")  # Create a frame for the back button
        back_button_frame.pack(pady=20)  # Add padding around the button frame
        tk.Button(back_button_frame, text="Back", command=lambda: self.load_user_dashboard(username), font=("Century Gothic", 15), 
                bg="#EDCC6F", fg="#2B2C41").pack()  # Center the button in the frame

    def book_grooming(self, username, pet_name, service_type, service_date):
    # Book a grooming service for a pet.
        try:
            if not pet_name:
                raise ValueError("Please select a pet.")
            if not service_type:
                raise ValueError("Please select a service.")
            if not service_date:
                raise ValueError("Please select a date.")

        # Get user ID from the database
            user_id = db.get_user_id(username)
            if not user_id:
                raise ValueError("User not found.")

        # Add the grooming service to the database
            db.add_grooming_service(user_id, pet_name, service_type, service_date)

        # Show success message and refresh the grooming services screen
            messagebox.showinfo("Success", f"Grooming service booked for {pet_name} on {service_date}.")
            self.GroomingServices(username)
        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to book grooming service: {e}")
            
    def cancel_grooming(self, username, appointment_id):
    # Cancel a grooming appointment by its ID.
        try:
            db.cancel_grooming_appointment(appointment_id)  # Call the database function to delete the appointment
            messagebox.showinfo("Success", "Grooming appointment canceled successfully!")
            self.GroomingServices(username)  # Refresh the grooming services screen
        except Exception as e:
            messagebox.showerror("Error", f"Failed to cancel appointment: {e}")

    def Daycare(self, username):
        # Manage daycare bookings for the user's pets.
        self.clear_frame()
        
        # Title label with updated font and color
        tk.Label(self.frame, text="DAYCARE BOOKING", font=("Century Gothic", 20, "bold"), bg="#FFFFED", fg="#2B2C41").pack(pady=20)

        # Create a scrollable frame for daycare bookings
        self.canvas = tk.Canvas(self.frame, bg="#FFFFED", width=500, height=500, bd=0)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#FFFFED")
        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="n", width=500)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Fetch user's pets
        pets = db.get_user_pets(username)
        if not pets:
            tk.Label(self.scrollable_frame, text="No pets registered. Please add a pet first.", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").pack(pady=10)
            tk.Button(self.scrollable_frame, text="Back", command=lambda: self.load_user_dashboard(username), font=("Century Gothic", 15), 
                    bg="#EDCC6F", fg="#2B2C41").pack(pady=10)
            return

        # Pet selection dropdown
        tk.Label(self.scrollable_frame, text="Select Pet:", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").pack(pady=5)
        pet_names = [pet["name"] for pet in pets]
        selected_pet = tk.StringVar()
        pet_dropdown = Combobox(self.scrollable_frame, textvariable=selected_pet, values=pet_names, state="readonly", font=("Century Gothic", 15))
        pet_dropdown.pack(pady=5)

        # Date selection using Calendar
        tk.Label(self.scrollable_frame, text="Select Date:", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").pack(pady=5)
        calendar = Calendar(self.scrollable_frame, selectmode="day")
        calendar.pack(pady=5)

        # Drop-off time
        tk.Label(self.scrollable_frame, text="Drop-off Time:", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").pack(pady=5)
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
        tk.Label(self.scrollable_frame, text="Pick-up Time:", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").pack(pady=5)
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
            font=("Century Gothic", 15),
            command=lambda: self.submit_daycare_booking(
                username,
                selected_pet.get(),
                calendar.get_date(),
                f"{drop_off_hour.get()}:{drop_off_minute.get()} {drop_off_ampm.get()}",
                f"{pick_up_hour.get()}:{pick_up_minute.get()} {pick_up_ampm.get()}"
            ),
            bg="#EDCC6F",
            fg="#2B2C41"
        ).pack(pady=10)

        # My daycare appointments
        tk.Label(self.scrollable_frame, text="My Daycare Appointments", font=("Century Gothic", 20), bg="#FFFFED", fg="#2B2C41").pack(pady=20)
        appointments = db.get_daycare_appointments(username, status="Pending")  # Fetch only pending appointments
        if appointments:
            for i, appointment in enumerate(appointments):
                tk.Label(self.scrollable_frame, text=f"{i + 1}. {appointment['pet_name']} - {appointment['date']}", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").pack(pady=5)
                tk.Button(
                    self.scrollable_frame,
                    text="Cancel",
                    command=lambda appointment_id=appointment['id']: self.cancel_daycare(username, appointment_id),
                    font=("Century Gothic", 15),
                    bg="#EDCC6F",
                    fg="#2B2C41"
                ).pack(pady=5)  # Ensure the button is displayed
        else:
            tk.Label(self.scrollable_frame, text="No daycare appointments found.", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").pack(pady=5)

        # Back button centered at the bottom
        back_button_frame = tk.Frame(self.scrollable_frame, bg="#FFFFED")  # Create a frame for the back button
        back_button_frame.pack(pady=20)  # Add padding around the button frame
        tk.Button(back_button_frame, text="Back", command=lambda: self.load_user_dashboard(username), font=("Century Gothic", 15), 
                bg="#EDCC6F", fg="#2B2C41").pack()  # Center the button in the frame

    def cancel_daycare(self, username, appointment_id):
        # Cancel a daycare appointment by its ID.
        try:
            db.cancel_daycare_appointment(appointment_id)  # Correct function call
            messagebox.showinfo("Success", "Daycare appointment canceled successfully!")
            self.Daycare(username)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to cancel appointment: {e}")

    def submit_daycare_booking(self, username, pet_name, date, drop_off_time, pick_up_time):
        """Submit a daycare booking for a pet."""
        try:
            if not pet_name:
                raise ValueError("Please select a pet.")
            if not date:
                raise ValueError("Please select a date.")
            if not drop_off_time or not pick_up_time:
                raise ValueError("Please specify both drop-off and pick-up times.")

            # Get user ID from the username
            user_id = db.get_user_id(username)
            if not user_id:
                raise ValueError("User not found.")

            # Save the booking to the daycare_bookings table
            status = "Pending"
            db.add_daycare_booking(user_id, pet_name, date, drop_off_time, pick_up_time, status)

            # Show success message
            messagebox.showinfo("Success", f"Daycare booked for {pet_name} on {date}.\nDrop-off: {drop_off_time}, Pick-up: {pick_up_time}")
            self.Daycare(username)  # Refresh the daycare page
        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to book daycare: {e}")

    def ServiceHistory(self, username):
    # Display the service history for the user, including grooming and daycare services
        self.clear_frame()
    
    # Title label
        tk.Label(self.frame, text="🔎 SERVICE HISTORY 🔍", font=("Century Gothic", 20, "bold"), bg="#FFFFED", fg="#2B2C41").pack(pady=20)

        user_id = db.get_user_id(username)
        if not user_id:
            tk.Label(self.frame, text="User not found.", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").pack(pady=10)
            tk.Button(self.frame, text="Back", command=lambda: self.load_user_dashboard(username), font=("Century Gothic", 15), 
                  bg="#EDCC6F", fg="#2B2C41").pack(pady=20)
            return

    # Create a scrollable frame for service history
        self.canvas = tk.Canvas(self.frame, bg="#FFFFED", width=900, height=500)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#FFFFED")
        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
    
        self.scrollable_frame.bind(
        "<Configure>",
        lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="n", width=900)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    # Fetch grooming and daycare services with status 'Done'
        grooming_history = db.get_grooming_services_done(user_id)
        daycare_history = db.get_daycare_services_done(user_id)

        if not grooming_history and not daycare_history:
            tk.Label(self.scrollable_frame, text="No service history found.", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").pack(pady=10)
        else:
        # Display Grooming Services
            if grooming_history:
                tk.Label(self.scrollable_frame, text="Grooming Services", font=("Century Gothic", 20), bg="#FFFFED", fg="#2B2C41").pack(pady=20, anchor="w")
                for record in grooming_history:
                    details = f"Pet: {record['pet_name']} | Date: {record['date']} | Service: {record['service_type']}"
                    tk.Label(self.scrollable_frame, text=details, justify="left", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").pack(pady=5, anchor="w")
            else:
                tk.Label(self.scrollable_frame, text="No grooming services found.", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").pack(pady=5, anchor="w")

        # Display Daycare Services
            if daycare_history:
                tk.Label(self.scrollable_frame, text="Daycare Services", font=("Century Gothic", 20), bg="#FFFFED", fg="#2B2C41").pack(pady=20, anchor="w")
                for record in daycare_history:
                    details = f"Pet: {record['pet_name']} | Date: {record['date']} | Details: {record['details']}"
                    tk.Label(self.scrollable_frame, text=details, justify="left", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").pack(pady=5, anchor="w")
            else:
                tk.Label(self.scrollable_frame, text="No daycare services found.", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").pack(pady=5, anchor="w")

    # Back button centered at the bottom
        back_button_frame = tk.Frame(self.scrollable_frame, bg="#FFFFED")  # Create a frame for the back button
        back_button_frame.pack(pady=20)  # Add padding around the button frame
        tk.Button(back_button_frame, text="Back", command=lambda: self.load_user_dashboard(username), font=("Century Gothic", 15), 
              bg="#EDCC6F", fg="#2B2C41").pack()  # Center the button in the frame

    def AddPet(self, username):
        # Display the interface for adding a new pet
        self.clear_frame()
        
        # Title label with updated font and color
        tk.Label(self.frame, text="💖 ADD PET 💖", font=("Century Gothic", 20, "bold"), bg="#FFFFED", fg="#2B2C41").pack(pady=20)

        # Create a frame for the input fields
        input_frame = tk.Frame(self.frame, bg="#FFFFED")  # Frame for input fields
        input_frame.pack(pady=20, padx=30)  # Add padding around the input frame

        # Name input
        tk.Label(input_frame, text="Name", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        pet_name = tk.Entry(input_frame, font=("Century Gothic", 15))
        pet_name.grid(row=0, column=1, padx=10, pady=5)

        # Species input
        tk.Label(input_frame, text="Species", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        species_options = ["Dog", "Cat"]
        pet_species = Combobox(input_frame, values=species_options, state="readonly", font=("Century Gothic", 15))
        pet_species.grid(row=1, column=1, padx=10, pady=5)

        # Age input
        tk.Label(input_frame, text="Age", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        pet_age = tk.Entry(input_frame, font=("Century Gothic", 15))
        pet_age.grid(row=2, column=1, padx=10, pady=5)

        # Upload Picture
        tk.Label(input_frame, text="Upload Picture", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        picture_path_label = tk.Label(input_frame, text="No file selected", font=("Century Gothic", 15), bg="#FFFFED", fg="#2B2C41")
        picture_path_label.grid(row=3, column=1, padx=10, pady=5)
        upload_button = tk.Button(input_frame, text="Upload Picture", command=lambda: self.upload_picture(picture_path_label), font=("Century Gothic", 15), bg="#EDCC6F", fg="#2B2C41")
        upload_button.grid(row=4, column=1, padx=10, pady=5)

        # Save and Cancel buttons
        button_frame = tk.Frame(self.frame, bg="#FFFFED")  # Frame for buttons
        button_frame.pack(pady=20)  # Add padding around the button frame

        save_button = tk.Button(
            button_frame,
            text="Save",
            font=("Century Gothic", 15),
            command=lambda: self.submit_pet(username, pet_name.get(), pet_species.get(), pet_age.get(), picture_path_label.cget("text")),
            bg="#EDCC6F",
            fg="#2B2C41"
        )
        save_button.pack(side=tk.LEFT, padx=10)
        back_button = tk.Button(button_frame, text="Cancel", font=("Century Gothic", 15), command=lambda: self.ManageMyPets(username), bg="#EDCC6F", fg="#2B2C41")
        back_button.pack(side=tk.LEFT, padx=10)
        
    def upload_picture(self, label):
        # Open a file dialog to select a picture and update the label with the file path.
        file_path = filedialog.askopenfilename(
            title="Select a Picture",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
        )
        if file_path:
            label.config(text=file_path)

    def submit_pet(self, username, name, species, age, picture_path=None):
        # Submit a new pet to the database.
        try:
            if not all([username, name, species, age]) or picture_path == "No file selected":
                raise ValueError("All fields are required.")
            age = int(age) if age.isdigit() else None
            if age is None:
                raise ValueError("Age must be a number.")
            user_id = db.get_user_id(username)
            if not user_id:
                raise ValueError("User  not found.")
            db.add_pet(user_id, name, species, age, picture_path)
            messagebox.showinfo("Success", "Pet added successfully!")
            self.ManageMyPets(username)
        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add pet: {e}")

# Create the main application window and run the application
window = tk.Tk()
PetServiceManagementSystem(window)
window.mainloop()