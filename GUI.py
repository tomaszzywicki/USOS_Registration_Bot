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
        self.pack(pady=20, padx=60, fill='both', expand=True)
        self.px = 10
        self.py = 12
        self.font = ('Roboto', 12)
        self.checkbox_var = tk.BooleanVar(value=True)
        self.LOGIN = self.PASSWORD = None
        self.CLASS_LINK = self.GROUP_NR = None
        self.create_widgets()
        self.driver = dc.Driver_Logic()
        if os.path.exists('login_password.txt'):
            with open('login_password.txt', 'r', encoding='utf-8') as file:
                data = file.read().splitlines()     
                self.username_entry.insert(0, data[0]) if data[0] else None
                self.password_entry.insert(0, data[1]) if data[0] and data [1] else None
        tk.set_appearance_mode('dark')
        tk.set_default_color_theme('dark-blue')

    def create_widgets(self):
        label = tk.CTkLabel(self, text='Welcome to the USOS auto-register bot!', font=('Roboto', 20))
        label.pack(pady=self.py, padx=self.px)

        self.username_entry = tk.CTkEntry(self, placeholder_text='USOS Username', font=self.font)
        self.username_entry.pack(pady=self.py, padx=self.px)

        self.password_entry = tk.CTkEntry(self, placeholder_text='USOS Password', font=self.font, show='*')
        self.password_entry.pack(pady=self.py, padx=self.px)    

        self.checkbox = tk.CTkCheckBox(self, text='Remember me', variable=self.checkbox_var, font=self.font, )
        self.checkbox.pack(pady=self.py, padx=self.px)

        self.link_entry = tk.CTkEntry(self, placeholder_text='Enter a link to your class here...', width=250, font=self.font)
        self.link_entry.pack(pady=self.py, padx=self.px)

        self.group_nr_entry = NumberEntry(self, placeholder_text='Enter your target group number here...', width=250, font=self.font)
        self.group_nr_entry.pack(pady=self.py, padx=self.px)

        self.confirm_button = tk.CTkButton(self, text='Confirm', command=self.confirm_action, font=self.font)
        self.confirm_button.pack(pady=self.py, padx=self.px)


    def create_login_password_file(self):
        if self.checkbox_var.get():
            with open('login_password.txt', 'w', encoding='utf-8') as file:
                file.write(f'{self.username_entry.get()}\n{self.password_entry.get()}')
        else:
            if os.path.exists('login_password.txt'):
                os.remove('login_password.txt')
        return


    def confirm_action(self):
        self.create_login_password_file()
        self.LOGIN = self.username_entry.get()
        self.PASSWORD = self.password_entry.get()
        self.CLASS_LINK = self.link_entry.get()
        self.GROUP_NR = self.group_nr_entry.get()
        self.driver.login_to_usos(self.LOGIN, self.PASSWORD)
        time.sleep(1)
        self.driver.select_wf(self.CLASS_LINK, self.GROUP_NR)
        self.driver.loop_driver()



# def main():
#     root = tk.CTk()
#     root.geometry('800x600')
#     root.title('USOS auto-register bot')

#     app = Application(root)
#     root.mainloop()


# if __name__ == "__main__":
#     main()