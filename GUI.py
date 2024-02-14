import customtkinter as tk

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
        self.padx = 10
        self.pady = 12
        super(Application, self).__init__(master)
        self.pack(pady=20, padx=60, fill='both', expand=True)
        self.create_widgets()
        tk.set_appearance_mode('dark')
        tk.set_default_color_theme('dark-blue')

    def create_widgets(self):
        label = tk.CTkLabel(self, text='Welcome to the USOS auto-register bot!', font=('Roboto', 20))
        label.pack(pady=12, padx=10)

        self.username_entry = tk.CTkEntry(self, placeholder_text='Username')
        self.username_entry.pack(pady=12, padx=10)

        self.password_entry = tk.CTkEntry(self, placeholder_text='Password')
        self.password_entry.pack(pady=12, padx=10)

        self.checkbox = tk.CTkCheckBox(self, text='Remember me')
        self.checkbox.pack(pady=12, padx=10)

        self.link_entry = tk.CTkEntry(self, placeholder_text='Enter a link to your class here...', width=200)
        self.link_entry.pack(pady=12, padx=10)

        self.group_nr_entry = NumberEntry(self, placeholder_text='Your target group number', width=200)
        self.group_nr_entry.pack(pady=12, padx=10)

        self.confirm_button = tk.CTkButton(self, text='Confirm')
        self.confirm_button.pack(pady=12, padx=10)


def main():
    root = tk.CTk()
    root.geometry('800x600')
    root.title('USOS auto-register bot')

    app = Application(root)
    root.mainloop()


if __name__ == "__main__":
    main()