import customtkinter as tk
import os, time
import driver_logic as dc


class NumberEntry(tk.CTkEntry):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(validate="key")
        self.configure(validatecommand=(self.register(self.validate_input), "%P"))

    def validate_input(self, new_text):
        if new_text.isdigit() or new_text == "":
            return True
        else:
            self.bell()
            return False


class Application(tk.CTkFrame):
    def __init__(self, master):
        super(Application, self).__init__(master)
        self.pack(pady=20, padx=60, fill="both", expand=True)
        self.inner_frame = tk.CTkFrame(self)
        self.inner_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.px = 10
        self.py = 12
        self.font = ("Roboto", 12)
        self.checkbox_var = tk.BooleanVar(value=True)
        self.LOGIN = self.PASSWORD = None
        self.CLASS_LINK = self.GROUP_NR = None
        self.HOUR = self.MINUTE = None
        self.create_widgets()
        self.driver = dc.DriverLogic()
        if os.path.exists("login_password.txt"):
            with open("login_password.txt", "r", encoding="utf-8") as file:
                data = file.read().splitlines()
                self.username_entry.insert(0, data[0]) if data[0] else None
                self.password_entry.insert(0, data[1]) if data[0] and data[1] else None
        tk.set_appearance_mode("dark")
        tk.set_default_color_theme("dark-blue")

    def create_widgets(self):
        self.label = tk.CTkLabel(
            self.inner_frame,
            text="Welcome to the USOS auto-register bot!",
            font=("Roboto", 20),
        )
        self.label.grid(row=0, column=0, columnspan=2, pady=self.py, padx=self.px)

        self.username_entry = tk.CTkEntry(
            self.inner_frame, placeholder_text="USOS Username", font=self.font
        )
        self.username_entry.grid(
            row=1, column=0, columnspan=2, pady=self.py, padx=self.px
        )

        self.password_entry = tk.CTkEntry(
            self.inner_frame, placeholder_text="USOS Password", font=self.font, show="*"
        )
        self.password_entry.grid(
            row=2, column=0, columnspan=2, pady=self.py, padx=self.px
        )

        self.checkbox = tk.CTkCheckBox(
            self.inner_frame,
            text="Remember me",
            variable=self.checkbox_var,
            font=self.font,
        )
        self.checkbox.grid(row=3, column=0, columnspan=2, pady=self.py, padx=self.px)

        self.uni_label = tk.CTkLabel(
            self.inner_frame, text="Choose your university: ", font=self.font
        )
        self.uni_label.grid(row=4, column=0)
        self.uni_picker = tk.CTkOptionMenu(
            self.inner_frame,
            values=["Politechnika Warszawska", "Uniwersytet Warszawski"],
            font=self.font,
            width=200,
            command=self.update_uni_fields,
        )
        self.uni_picker.grid(row=4, column=1, columnspan=2, pady=self.py, padx=self.px)

        # PW - link
        self.link_entry = tk.CTkEntry(
            self.inner_frame,
            placeholder_text="Enter a link to your course here...",
            width=250,
            font=self.font,
        )
        self.link_entry.grid(row=5, column=0, columnspan=2, pady=self.py, padx=self.px)

        # UW - course name
        self.course_name_entry = tk.CTkEntry(
            self.inner_frame,
            placeholder_text="Enter a course name here ... ",
            width=250,
            font=self.font,
        )

        self.group_nr_entry = NumberEntry(
            self.inner_frame,
            placeholder_text="Enter your target group number here...",
            width=250,
            font=self.font,
        )
        self.group_nr_entry.grid(
            row=6, column=0, columnspan=2, pady=self.py, padx=self.px
        )

        self.hour_label = tk.CTkLabel(
            self.inner_frame, text="Hour of registration start:", font=self.font
        )
        self.hour_label.grid(row=7, column=0, pady=self.py, padx=self.px)

        self.hour_picker = tk.CTkOptionMenu(
            self.inner_frame,
            values=[str(i) for i in range(24)],
            font=self.font,
            width=50,
        )
        self.hour_picker.grid(row=7, column=1, pady=self.py, padx=self.px)

        self.minute_label = tk.CTkLabel(
            self.inner_frame, text="Minute of registration start:", font=self.font
        )
        self.minute_label.grid(row=8, column=0, pady=self.py, padx=self.px)

        self.minute_picker = tk.CTkOptionMenu(
            self.inner_frame,
            values=[str(i) for i in range(60)],
            font=self.font,
            width=50,
        )
        self.minute_picker.grid(row=8, column=1, pady=self.py, padx=self.px)

        self.confirm_button = tk.CTkButton(
            self.inner_frame,
            text="Confirm",
            command=self.confirm_action,
            font=self.font,
        )
        self.confirm_button.grid(
            row=9, column=0, columnspan=2, pady=self.py, padx=self.px
        )

    def create_login_password_file(self):
        if self.checkbox_var.get():
            with open("login_password.txt", "w", encoding="utf-8") as file:
                file.write(f"{self.username_entry.get()}\n{self.password_entry.get()}")
        else:
            if os.path.exists("login_password.txt"):
                os.remove("login_password.txt")
        return

    def confirm_action(self):
        self.create_login_password_file()
        self.LOGIN = self.username_entry.get()
        self.PASSWORD = self.password_entry.get()
        self.UNIVERSITY = self.uni_picker.get()
        self.GROUP_NR = self.group_nr_entry.get()
        self.HOUR = int(self.hour_picker.get())
        self.MINUTE = int(self.minute_picker.get())

        if self.UNIVERSITY == "Politechnika Warszawska":
            self.CLASS_LINK = self.link_entry.get()
            print(f"[INFO] Wybrano PW, link: {self.CLASS_LINK}, grupa: {self.GROUP_NR}")
        elif self.UNIVERSITY == "Uniwersytet Warszawski":
            self.COURSE_NAME = self.course_name_entry.get()
            print(
                f"[INFO] Wybrano UW, kurs: {self.COURSE_NAME}, grupa: {self.GROUP_NR}"
            )

        print("[INFO] Logowanie do USOS...")
        self.driver.login_to_usos(self.LOGIN, self.PASSWORD, self.UNIVERSITY)
        time.sleep(1)

        print("[INFO] Oczekiwanie na moment rejestracji...")
        if self.UNIVERSITY == "Politechnika Warszawska":
            self.driver.select_course_pw(
                self.CLASS_LINK, self.GROUP_NR, self.HOUR, self.MINUTE
            )
        elif self.UNIVERSITY == "Uniwersytet Warszawski":
            self.driver.select_course_uw(
                self.COURSE_NAME, self.GROUP_NR, self.HOUR, self.MINUTE
            )

    def update_uni_fields(self, choice: str):
        if choice == "Politechnika Warszawska":
            self.course_name_entry.grid_forget()
            self.link_entry.grid(
                row=5, column=0, columnspan=2, pady=self.py, padx=self.px
            )
        elif choice == "Uniwersytet Warszawski":
            self.link_entry.grid_forget()
            self.course_name_entry.grid(
                row=5, column=0, columnspan=2, pady=self.py, padx=self.px
            )
