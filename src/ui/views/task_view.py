import threading
import customtkinter as ctk
from automations.SEI_DMA import run_playwright
from config.format_text import formatar_para_sei


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
        ).grid(row=2, column=0, padx=60, sticky="w")

        # Entrada do Título
        self.title_entry = ctk.CTkEntry(
            self, placeholder_text="Digite o título do processo...", height=40
        )
        self.title_entry.grid(row=3, column=0, padx=60, pady=(5, 20), sticky="ew")

        # Label Conteúdo
        ctk.CTkLabel(
            self, text="Conteúdo do Despacho:", font=("Arial", 14, "bold")
        ).grid(row=4, column=0, padx=60, sticky="w")

        # Textbox do Conteúdo
        self.content_text = ctk.CTkTextbox(
            self, font=("Arial", 16), border_width=2, activate_scrollbars=True
        )
        self.content_text.grid(row=5, column=0, padx=60, pady=(5, 20), sticky="nsew")

        # Botão de Iniciar
        self.btn_start = ctk.CTkButton(
            self,
            text="Iniciar Automação",
            font=("Arial", 15, "bold"),
            command=self.start_automation,
        )
        self.btn_start.grid(row=7, column=0, pady=20)

        # Botão Voltar (Importante para UX)
        ctk.CTkButton(
            self,
            text="Voltar ao Menu",
            fg_color="transparent",
            border_width=1,
            command=lambda: self.master.show_menu(),
        ).grid(row=8, column=0, pady=(0, 20))

        # Botão de Copiar Número SEI (Inicialmente invisível, só aparece após a automação)
        self.btn_copy = ctk.CTkButton(
            self,
            text="Copiar Número SEI",
            font=("Arial", 13, "bold"),
            fg_color="#2b719e",
            hover_color="#1d4e6d",
            width=150,
            command=self.copy_to_clipboard,
        )
        self.last_sei_number = ""  # Variável para guardar o número

    def copy_to_clipboard(self):
        if self.last_sei_number:
            self.clipboard_clear()
            self.clipboard_append(self.last_sei_number)
            # Feedback visual rápido no botão
            old_text = self.btn_copy.cget("text")
            self.btn_copy.configure(text="✅ Copiado!", fg_color="green")
            self.after(
                2000, lambda: self.btn_copy.configure(text=old_text, fg_color="#2b719e")
            )

    def start_automation(self):
        # Coleta de dados correta dos widgets e Pegar as credenciais que salvamos no master durante o login
        user = getattr(self.master, "logged_user", "")
        pwd = getattr(self.master, "logged_pwd", "")

        title = self.title_entry.get()
        # Pega todo o texto do Textbox
        content_text = self.content_text.get("1.0", "end-1c")
        content_ass = getattr(self.master, "logged_content_ass", "")

        # juntar e processar dados para colocar no SEI
        content = content_text + "\n\n" + content_ass
        content = formatar_para_sei(content)

        if not title.strip():
            self.error_label.configure(text="Erro: Título vazio")
            return

        self.btn_start.configure(state="disabled", text="Executando...")
        self.error_label.configure(text="")

        t = threading.Thread(
            target=self._worker,
            args=(user, pwd, title, content),
            daemon=True,
        )
        t.start()

    def _worker(self, user, pwd, title, content):
        numero_sei = "Não capturado"
        try:
            numero_sei = run_playwright(user, pwd, title, content)
            self.last_sei_number = numero_sei  # Salva para a função de copiar

            self.after(
                0,
                lambda: self.error_label.configure(
                    text="Processando finalização...", text_color="blue"
                ),
            )

        except Exception as e:
            self.after(
                0,
                lambda: self.error_label.configure(
                    text=f"Erro na automação: {e}", text_color="red"
                ),
            )
            return

        finally:
            if numero_sei != "Não capturado":
                text_result = f"{numero_sei}"
                self.after(0, lambda: self._show_success_ui(text_result))

            self.after(0, self._reset_button)

    def _show_success_ui(self, message):
        """Atualiza a label e mostra o botão de cópia"""
        text_label = f"Automação concluída com sucesso!\nNúmero SEI: {message}"
        self.error_label.configure(text=text_label, text_color="green")
        # Faz o botão de copiar aparecer logo abaixo da label de sucesso
        self.btn_copy.grid(row=6, column=0, pady=(0, 20))
        # Salva o número para a função de cópia
        # (Lembre-se de definir self.last_sei_number no __init__)
        self.last_sei_number = message.split("\n")[-1]

    def _reset_button(self):
        self.btn_start.configure(state="normal", text="Iniciar Automação")
