import customtkinter as tk

from GUI import Application

def main():
    tk.set_appearance_mode('dark')
    tk.set_default_color_theme('dark-blue')
    root = tk.CTk()
    root.geometry('800x600')
    root.title('USOS auto-register bot')

    app = Application(root)
    root.mainloop()

if __name__ == "__main__":
    main()