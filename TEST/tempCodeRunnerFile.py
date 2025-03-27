    def AddPet(self, username):
        # Display the interface for adding a new pet.
        self.clear_frame()
        
        # Title label with updated font and color
        tk.Label(self.frame, text="Add Pet", font=("Century Gothic", 24), bg="#88CAFC", fg="#2B2C41").pack(pady=20)

        # Create a frame for the input fields
        input_frame = tk.Frame(self.frame, bg="#D2EBFF")  # Frame for input fields
        input_frame.pack(pady=20, padx=30)  # Add padding around the input frame

        # Name input
        tk.Label(input_frame, text="Name", font=("Century Gothic", 15), bg="#D2EBFF", fg="#2B2C41").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        pet_name = tk.Entry(input_frame, font=("Century Gothic", 15))
        pet_name.grid(row=0, column=1, padx=10, pady=5)

        # Species input
        tk.Label(input_frame, text="Species", font=("Century Gothic", 15), bg="#D2EBFF", fg="#2B2C41").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        species_options = ["Dog", "Cat"]
        pet_species = Combobox(input_frame, values=species_options, state="readonly", font=("Century Gothic", 15))
        pet_species.grid(row=1, column=1, padx=10, pady=5)

        # Age input
        tk.Label(input_frame, text="Age", font=("Century Gothic", 15), bg="#D2EBFF", fg="#2B2C41").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        pet_age = tk.Entry(input_frame, font=("Century Gothic", 15))
        pet_age.grid(row=2, column=1, padx=10, pady=5)

        # Upload Picture
        tk.Label(input_frame, text="Upload Picture", font=("Century Gothic", 15), bg="#D2EBFF", fg="#2B2C41").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        picture_path_label = tk.Label(input_frame, text="No file selected", font=("Century Gothic", 15), bg="#D2EBFF", fg="#2B2C41")
        picture_path_label.grid(row=3, column=1, padx=10, pady=5)
        upload_button = tk.Button(input_frame, text="Upload Picture", command=lambda: self.upload_picture(picture_path_label), font=("Century Gothic", 15), bg="#EDCC6F", fg="#2B2C41")
        upload_button.grid(row=4, column=1, padx=10, pady=5)

        # Save and Cancel buttons
        button_frame = tk.Frame(self.frame, bg="#D2EBFF")  # Frame for buttons
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