import customtkinter as ctk
from config.settings import save_prefs
from config.settings import load_prefs


class LoginView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master  # Referência para o AppWindow
        self.master.resizable(False, False)
        prefs = load_prefs()
        # Variáveis exclusivas à instância, eliminando "global"
        self.login_label = ctk.CTkLabel(self, text="LOGIN", font=("Arial", 22, "bold"))
        self.login_label.pack(pady=(40, 20))
        ctk.CTkLabel(self, text="Usuário:").pack(anchor="w", padx=50)
        self.user_entry = ctk.CTkEntry(self, width=300, height=35)
        self.user_entry.insert(0, prefs.get("user", ""))
        self.user_entry.pack(pady=5)

        self.password_label = ctk.CTkLabel(self, text="Senha:").pack(
            anchor="w", padx=50
        )
        self.password_entry = ctk.CTkEntry(self, width=300, height=35, show="*")
        self.password_entry.pack(pady=5)

        self.remember_var = ctk.BooleanVar(value=prefs.get("remember", False))
        ctk.CTkCheckBox(self, text="Lembrar usuário", variable=self.remember_var).pack(
            pady=15
        )

        self.btn_login = ctk.CTkButton(self, text="Entrar", command=self.do_login)
        self.btn_login.pack(pady=20)

    def do_login(self):
        save_prefs(self.user_entry.get(), self.remember_var.get())
        self.master.resizable(True, True)  # Permite que a próxima tela cresça
        self.master.show_menu()
