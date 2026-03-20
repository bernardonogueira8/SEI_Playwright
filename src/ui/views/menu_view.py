import customtkinter as ctk
from ui.views.task_view import TaskView


class MenuView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        ctk.CTkLabel(
            self, text="Selecione a Rotina de Automação", font=("Arial", 20)
        ).pack(pady=30)

        # Cada botão troca o frame para uma tela secundária específica
        btn_redmine = ctk.CTkButton(
            self,
            text="Criar Processo SEI e Chamado Redmine",
            command=lambda: self.master.switch_frame(TaskView),
        )
        btn_redmine.pack(pady=10)

        btn_outra = ctk.CTkButton(self, text="Outra Automação", command=...)
        btn_outra.pack(pady=10)
