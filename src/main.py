import customtkinter as ctk
from ui.app_window import AppWindow

# Variáveis globais para os widgets
user_entry = None
password_entry = None
title_entry = None
content_text = None
app = None


def main():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = AppWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
