def run_playwright(user, password, title, content):
    try:
        with sync_playwright() as p:
            browser = p.firefox.launch(headless=False, slow_mo=500)
            page = browser.new_page()

            # 1. Login
            page.goto("https://seibahia.ba.gov.br")
            page.get_by_role("textbox", name="Usuário").fill(user)
            page.get_by_role("textbox", name="Senha").fill(password)
            page.locator("#selOrgao").select_option("23")  # Exemplo: CGTICS ou SESAB
            page.get_by_role("button", name="ACESSAR").click()

            # 2. Criar Processo
            page.get_by_role("link", name="Iniciar Processo").click()
            # Ajuste o nome do tipo de processo conforme sua necessidade real
            page.get_by_role(
                "link", name="Documento tramitável: Comunicação Interna"
            ).click()
            page.get_by_role("textbox", name="Especificação:").click()
            page.get_by_role("textbox", name="Especificação:").fill(title)
            page.locator("#divInfraBarraComandosSuperior").get_by_role(
                "button", name="Salvar"
            ).click()
            page.locator('iframe[name="ifrVisualizacao"]').content_frame.get_by_role(
                "link", name="Incluir Documento"
            ).click()
            page.locator('iframe[name="ifrVisualizacao"]').content_frame.get_by_role(
                "link", name="Despacho"
            ).click()
            with page.expect_popup() as page1_info:
                page.locator('iframe[name="ifrVisualizacao"]').content_frame.locator(
                    "#divInfraBarraComandosSuperior"
                ).get_by_role("button", name="Salvar").click()
            page1 = page1_info.value
            page1.locator(
                'iframe[title="Processo e Interessado"]'
            ).content_frame.get_by_text("Insira aqui o órgão").click()
            page1.locator(
                'iframe[title="Processo e Interessado"]'
            ).content_frame.get_by_role("cell", name="[Insira aqui o órgão").fill(
                "CGTICS"
            )
            page1.get_by_role("button", name="Salvar").click()
            page1.close()
            page.locator('iframe[name="ifrVisualizacao"]').content_frame.get_by_role(
                "link", name="Incluir em Bloco de Assinatura"
            ).click()
            page.locator('iframe[name="ifrVisualizacao"]').content_frame.get_by_role(
                "button", name="Novo Bloco"
            ).click()
            page.locator('iframe[name="ifrVisualizacao"]').content_frame.get_by_role(
                "textbox", name="Descrição:"
            ).fill(title)
            page.locator('iframe[name="ifrVisualizacao"]').content_frame.get_by_role(
                "button", name="Salvar"
            ).click()
            page.locator('iframe[name="ifrVisualizacao"]').content_frame.get_by_role(
                "button", name="Incluir", exact=True
            ).click()
            page.locator('iframe[name="ifrArvore"]').content_frame.get_by_role(
                "link", name="-33"
            ).click()

    except Exception as e:
        print(f"Erro: {e}")


def show_second_step():

    # Configuração de Grid para Texto Longo
    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(4, weight=1)  # Faz o Textbox ocupar o centro

    ctk

    ctk.CTkLabel(app, text="Título / Especificação:", font=("Arial", 14, "bold")).grid(
        row=1, column=0, padx=60, sticky="w"
    )
    global title_entry
    title_entry = ctk.CTkEntry(
        app, placeholder_text="Digite o título do processo...", height=40
    )
    title_entry.grid(row=2, column=0, padx=60, pady=(5, 20), sticky="ew")

    ctk.CTkLabel(app, text="Conteúdo do Despacho:", font=("Arial", 14, "bold")).grid(
        row=3, column=0, padx=60, sticky="w"
    )
    global content_text
    content_text = ctk.CTkTextbox(
        app, font=("Arial", 16), border_width=2, activate_scrollbars=True
    )
    content_text.grid(row=4, column=0, padx=60, pady=(5, 20), sticky="nsew")

    btn_frame = ctk.CTkFrame(app, fg_color="transparent")
    btn_frame.grid(row=5, column=0, pady=(0, 30))
