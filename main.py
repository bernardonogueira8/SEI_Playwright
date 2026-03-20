import customtkinter
from playwright.sync_api import sync_playwright
import os
import json

# Variáveis globais para os widgets
user_entry = None
password_entry = None
title_entry = None
content_text = None
app = None
CONFIG_FILE = "config_sei.json"


def main():
    create_window()


def start_automation():
    # Coleta os dados das duas etapas
    usuario = user_entry.get()
    senha = password_entry.get()
    titulo = title_entry.get()
    conteudo = content_text.get("1.0", "end-1c")

    if not all([usuario, senha, titulo, conteudo]):
        print("Erro: Todos os campos são obrigatórios!")
        return

    run_playwright(usuario, senha, titulo, conteudo)


def run_playwright(user, password, title, content):
    try:
        with sync_playwright() as p:
            browser = p.firefox.launch(headless=False, slow_mo=500)
            page = browser.new_page()

            # 1. Login
            page.goto("https://seibahia.ba.gov.br")
            page.get_by_role("textbox", name="Usuário").fill(user)
            page.get_by_role("textbox", name="Senha").fill(password)
            page.locator("#selOrgao").select_option(
                "23")  # Exemplo: CGTICS ou SESAB
            page.get_by_role("button", name="ACESSAR").click()

            # 2. Criar Processo
            page.get_by_role("link", name="Iniciar Processo").click()
            # Ajuste o nome do tipo de processo conforme sua necessidade real
            page.get_by_role(
                "link", name="Documento tramitável: Comunicação Interna").click()
            page.get_by_role("textbox", name="Especificação:").click()
            page.get_by_role("textbox", name="Especificação:").fill(title)
            page.locator("#divInfraBarraComandosSuperior").get_by_role(
                "button", name="Salvar").click()
            page.locator("iframe[name=\"ifrVisualizacao\"]").content_frame.get_by_role(
                "link", name="Incluir Documento").click()
            page.locator("iframe[name=\"ifrVisualizacao\"]").content_frame.get_by_role(
                "link", name="Despacho").click()
            with page.expect_popup() as page1_info:
                page.locator("iframe[name=\"ifrVisualizacao\"]").content_frame.locator(
                    "#divInfraBarraComandosSuperior").get_by_role("button", name="Salvar").click()
            page1 = page1_info.value
            page1.locator("iframe[title=\"Processo e Interessado\"]").content_frame.get_by_text(
                "Insira aqui o órgão").click()
            page1.locator("iframe[title=\"Processo e Interessado\"]").content_frame.get_by_role(
                "cell", name="[Insira aqui o órgão").fill("CGTICS")
            page1.get_by_role("button", name="Salvar").click()
            page1.close()
            page.locator("iframe[name=\"ifrVisualizacao\"]").content_frame.get_by_role(
                "link", name="Incluir em Bloco de Assinatura").click()
            page.locator("iframe[name=\"ifrVisualizacao\"]").content_frame.get_by_role(
                "button", name="Novo Bloco").click()
            page.locator("iframe[name=\"ifrVisualizacao\"]").content_frame.get_by_role(
                "textbox", name="Descrição:").fill(title)
            page.locator("iframe[name=\"ifrVisualizacao\"]").content_frame.get_by_role(
                "button", name="Salvar").click()
            page.locator("iframe[name=\"ifrVisualizacao\"]").content_frame.get_by_role(
                "button", name="Incluir", exact=True).click()
            page.locator("iframe[name=\"ifrArvore\"]").content_frame.get_by_role(
                "link", name="-33").click()

    except Exception as e:
        print(f"Erro: {e}")


def save_prefs(user, remember):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"user": user if remember else "", "remember": remember}, f)


def load_prefs():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"user": "", "remember": False}


def show_second_step():
    # --- MUDANÇA PARA FULLSCREEN AQUI ---
    app.attributes("-fullscreen", True)
    app.bind("<Escape>", lambda e: app.attributes("-fullscreen", False))

    # Limpa a tela de login
    for widget in app.winfo_children():
        widget.destroy()

    # Configuração de Grid para Texto Longo
    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(4, weight=1)  # Faz o Textbox ocupar o centro

    customtkinter.CTkLabel(app, text="REGISTRO DE DESPACHO - SEI BAHIA",
                           font=("Arial", 26, "bold"), text_color="#3b8ed0").grid(row=0, column=0, pady=(30, 20))

    customtkinter.CTkLabel(app, text="Título / Especificação:", font=(
        "Arial", 14, "bold")).grid(row=1, column=0, padx=60, sticky="w")
    global title_entry
    title_entry = customtkinter.CTkEntry(
        app, placeholder_text="Digite o título do processo...", height=40)
    title_entry.grid(row=2, column=0, padx=60, pady=(5, 20), sticky="ew")

    customtkinter.CTkLabel(app, text="Conteúdo do Despacho:", font=(
        "Arial", 14, "bold")).grid(row=3, column=0, padx=60, sticky="w")
    global content_text
    content_text = customtkinter.CTkTextbox(app, font=(
        "Arial", 16), border_width=2, activate_scrollbars=True)
    content_text.grid(row=4, column=0, padx=60, pady=(5, 20), sticky="nsew")

    btn_frame = customtkinter.CTkFrame(app, fg_color="transparent")
    btn_frame.grid(row=5, column=0, pady=(0, 30))

    customtkinter.CTkButton(btn_frame, text="Janela Normal", fg_color="#555555",
                            command=lambda: app.attributes("-fullscreen", False)).pack(side="left", padx=10)

    customtkinter.CTkButton(btn_frame, text="INICIAR AUTOMAÇÃO", font=("Arial", 15, "bold"),
                            width=250, height=45, command=start_automation).pack(side="left", padx=10)


def create_window():
    global user_entry, password_entry, remember_var, app

    customtkinter.set_appearance_mode("Dark")
    app = customtkinter.CTk()

    # --- LOGIN PEQUENO E CENTRALIZADO ---
    app.geometry("400x500")
    app.resizable(False, False)  # Trava o tamanho no login
    app.title("Acesso SEI")

    prefs = load_prefs()

    customtkinter.CTkLabel(app, text="LOGIN", font=(
        "Arial", 22, "bold")).pack(pady=(40, 20))

    customtkinter.CTkLabel(app, text="Usuário:").pack(anchor="w", padx=50)
    user_entry = customtkinter.CTkEntry(app, width=300, height=35)
    user_entry.insert(0, prefs.get("user", ""))
    user_entry.pack(pady=5)

    customtkinter.CTkLabel(app, text="Senha:").pack(anchor="w", padx=50)
    password_entry = customtkinter.CTkEntry(
        app, width=300, height=35, show="*")
    password_entry.pack(pady=5)

    remember_var = customtkinter.BooleanVar(value=prefs.get("remember", False))
    customtkinter.CTkCheckBox(
        app, text="Lembrar usuário", variable=remember_var).pack(pady=15)

    def login_click():
        save_prefs(user_entry.get(), remember_var.get())
        app.resizable(True, True)  # Permite que a próxima tela cresça
        show_second_step()

    customtkinter.CTkButton(app, text="ENTRAR", width=300, height=40,
                            font=("Arial", 13, "bold"), command=login_click).pack(pady=20)

    app.mainloop()


if __name__ == "__main__":
    main()
