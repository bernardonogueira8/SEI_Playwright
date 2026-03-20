import threading
import customtkinter as ctk
from automations.sei_automation import run_playwright


class TaskView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.title_entry = ctk.CTkEntry(self, placeholder_text="Título do Processo")
        self.title_entry.pack(pady=10)

        self.btn_start = ctk.CTkButton(
            self, text="Iniciar Automação", command=self.start_automation
        )
        self.btn_start.pack(pady=20)

    def start_automation(self):
        title = self.title_entry.get()
        # Coleta os demais dados...

        # Opcional: Modificar a tela para mostrar "Carregando"
        self.btn_start.configure(state="disabled", text="Executando...")

        # Dispara a rotina pesada fora do Thread Principal da interface
        t = threading.Thread(
            target=self._worker, args=("usuario", "senha", title, "conteudo")
        )
        t.start()

    def _worker(self, user, pwd, title, content):
        try:
            run_playwright(user, pwd, title, content)
        finally:
            # Reabilita a UI no final da operação.
            self.btn_start.configure(state="normal", text="Iniciar Automação")
