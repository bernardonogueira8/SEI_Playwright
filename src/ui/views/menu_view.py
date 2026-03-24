import customtkinter as ctk
from ui.views.task_view import TaskView
from config.settings import save_ass, load_ass


class MenuView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        # Carrega preferências anteriores
        prefs = load_ass()

        # Configuração de tela
        master.attributes("-fullscreen", True)
        master.bind("<Escape>", lambda e: master.attributes("-fullscreen", False))

        # Título
        ctk.CTkLabel(
            self, text="Selecione a Rotina de Automação", font=("Arial", 24, "bold")
        ).pack(pady=(50, 30))

        # Mapeamento de rotinas
        self.opcoes_rotinas = {
            "Criar Processo SEI e Chamado Redmine": TaskView,
            "Outra Automação": None,
        }

        # Criando os botões verticalmente de forma dinâmica
        for nome_rotina, view_class in self.opcoes_rotinas.items():
            btn = ctk.CTkButton(
                self,
                text=nome_rotina,
                font=("Arial", 16),
                width=400,
                height=50,
                corner_radius=10,
                command=lambda v=view_class, n=nome_rotina: self.executar_rotina(v, n),
            )
            btn.pack(pady=10)

            # --- Seção da Assinatura (Usando Pack para manter consistência) ---
        ctk.CTkLabel(self, text="Assinatura:", font=("Arial", 14, "bold")).pack(
            pady=(20, 0), padx=60, anchor="w"
        )

        self.content_ass = ctk.CTkTextbox(
            self, font=("Arial", 16), border_width=2, height=150
        )
        self.content_ass.pack(pady=(5, 20), padx=60, fill="x")

        # Insere o conteúdo carregado (se existir) no Textbox
        if prefs:
            self.content_ass.insert("0.0", prefs)

    def executar_rotina(self, view_class, nome_rotina):
        if view_class:
            # Captura o texto ATUAL do textbox no momento do clique
            texto_assinatura = self.content_ass.get("0.0", "end-1c").strip()
            # Salva usando sua função do config.settings
            # Note: adicionei um placeholder 'True' se sua função exigir o remember_var
            save_ass(texto_assinatura)
            # Armazena no master para uso posterior
            self.master.logged_content_ass = texto_assinatura

            self.focus_set()
            self.after(10, lambda: self.master.switch_frame(view_class))
        else:
            print(f"Rotina '{nome_rotina}' ainda não implementada.")
