import customtkinter as ctk
from ui.views.login_view import LoginView
from ui.views.menu_view import MenuView


class AppWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Automações SEI")
        self.geometry("400x500")
        self.current_frame = None
        self.show_login()  # Inicia pela tela de login

    def switch_frame(self, frame_class):
        """Destrói a tela atual e renderiza a nova tela na janela principal."""
        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame = frame_class(self)
        # O packer (pack) cuida do preenchimento da tela
        self.current_frame.pack(expand=True, fill="both")

    def show_login(self):
        self.switch_frame(LoginView)

    def show_menu(self):
        self.switch_frame(MenuView)
