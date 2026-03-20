import customtkinter as ctk
from ui.views.task_view import TaskView


class MenuView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.attributes("-fullscreen", True)
        master.bind("<Escape>", lambda e: master.attributes("-fullscreen", False))

        ctk.CTkLabel(
            self, text="Selecione a Rotina de Automação", font=("Arial", 24, "bold")
        ).pack(pady=(50, 30))

        # Mapeamento de nomes para as classes de View
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

    def executar_rotina(self, view_class, nome_rotina):
        if view_class:
            self.master.switch_frame(view_class)
        else:
            print(f"Rotina '{nome_rotina}' ainda não implementada.")
