import threading
import customtkinter as ctk
from automations.SEI_DMA import run_playwright


class TaskView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        # Configuração de Grid: A coluna 0 expande, a linha 4 (textbox) também.
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        # Título Principal
        ctk.CTkLabel(
            self,
            text="REGISTRO DE DESPACHO - SEI BAHIA",
            font=("Arial", 21, "bold"),
            text_color="#3b8ed0",
        ).grid(row=0, column=0, pady=(30, 20))
        # Label de erro
        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.grid(row=1, column=0, pady=5)

        # Label Título
        ctk.CTkLabel(
            self, text="Título / Especificação:", font=("Arial", 14, "bold")
        ).grid(row=1, column=0, padx=60, sticky="w")

        # Entrada do Título
        self.title_entry = ctk.CTkEntry(
            self, placeholder_text="Digite o título do processo...", height=40
        )
        self.title_entry.grid(row=2, column=0, padx=60, pady=(5, 20), sticky="ew")

        # Label Conteúdo
        ctk.CTkLabel(
            self, text="Conteúdo do Despacho:", font=("Arial", 14, "bold")
        ).grid(row=3, column=0, padx=60, sticky="w")

        # Textbox do Conteúdo
        self.content_text = ctk.CTkTextbox(
            self, font=("Arial", 16), border_width=2, activate_scrollbars=True
        )
        self.content_text.grid(row=4, column=0, padx=60, pady=(5, 20), sticky="nsew")

        # Botão de Iniciar
        self.btn_start = ctk.CTkButton(
            self,
            text="Iniciar Automação",
            font=("Arial", 15, "bold"),
            command=self.start_automation,
        )
        self.btn_start.grid(row=5, column=0, pady=20)

        # Botão Voltar (Importante para UX)
        ctk.CTkButton(
            self,
            text="Voltar ao Menu",
            fg_color="transparent",
            border_width=1,
            command=lambda: self.master.show_menu(),
        ).grid(row=6, column=0, pady=(0, 20))

    def start_automation(self):
        # Coleta de dados correta dos widgets
        title = self.title_entry.get()
        content = self.content_text.get("1.0", "end-1c")  # Pega todo o texto do Textbox

        if not title.strip():
            self.error_label.configure(text="Erro: Título vazio")
            return

        self.btn_start.configure(state="disabled", text="Executando...")
        self.error_label.configure(text="")

        # Dispara o worker
        # Pegamos as credenciais que salvamos no master durante o login
        user = getattr(self.master, "logged_user", "")
        pwd = getattr(self.master, "logged_pwd", "")
        content_ass = getattr(self.master, "logged_content_ass", "")

        t = threading.Thread(
            target=self._worker, args=(user, pwd, title, content), daemon=True
        )
        t.start()

    def _worker(self, user, pwd, title, content, content_ass):
        try:
            run_playwright(user, pwd, title, content, content_ass)
        except Exception as e:
            self.error_label.configure(text=f"Erro na automação: {e}")
        finally:
            # Para mexer na UI de dentro de um thread, o ideal é usar after()
            self.after(0, self._reset_button)

    def _reset_button(self):
        self.btn_start.configure(state="normal", text="Iniciar Automação")
