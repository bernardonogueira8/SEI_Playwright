import logging
from playwright.sync_api import sync_playwright

# Configuração de um logger para rastrear os passos da automação
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def run_playwright(user, pwd, title, content, content_ass):
    """
    Executa a rotina de automação no sistema SEI.

    Esta função recebe apenas dados puros (strings, dicionários, etc.)
    e não tem NENHUMA dependência da interface gráfica (Tkinter).
    """
    logger.info(f"Iniciando automação no SEI para o usuário: {user} | Título: {title}")

    try:
        # Inicializa o Playwright de forma síncrona
        with sync_playwright() as p:
            browser = p.firefox.launch(headless=False, slow_mo=500)
            page = browser.new_page()  # [1]
            logger.info("Navegador aberto. Acessando a página de login...")

            open_browser(page, user, pwd)
            create_process(page, title)
            edit_despacho(page, content, content_ass)

            browser.close()

    except Exception as e:
        logger.error(f"Erro crítico durante a execução da automação no SEI: {e}")


def open_browser(page, user, pwd):
    # 1. Login
    page.goto("https://seibahia.ba.gov.br")
    page.get_by_role("textbox", name="Usuário").fill(user)
    page.get_by_role("textbox", name="Senha").fill(pwd)
    page.locator("#selOrgao").select_option("23")  # Exemplo: CGTICS ou SESAB
    page.get_by_role("button", name="ACESSAR").click()


def create_process(page, title):
    # 2. Criar Processo
    page.get_by_role("link", name="Iniciar Processo").click()
    # Ajuste o nome do tipo de processo conforme sua necessidade real
    page.get_by_role("link", name="Documento tramitável: Comunicação Interna").click()
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


def edit_despacho(page1, content, content_ass):
    # 3. Editando o Despacho
    page1 = page1_info.value
    page1.locator('iframe[title="Processo e Interessado"]').content_frame.get_by_text(
        "Insira aqui o órgão"
    ).click()
    page1.locator('iframe[title="Processo e Interessado"]').content_frame.get_by_role(
        "cell", name="[Insira aqui o órgão"
    ).fill("CGTICS")
    page1.locator('iframe[title="Corpo do Texto"]').content_frame.locator(
        "html"
    ).click()
    page1.locator('iframe[title="Corpo do Texto"]').content_frame.locator("html").fill(
        content + "\n\n" + content_ass
    )
    page1.locator('iframe[title="Corpo do Texto"]').content_frame.locator(
        "html"
    ).click()
    try:
        page1.get_by_role("button", name="Estilo").click()
    except:
        page1.get_by_role(
            "button", name="Texto_Justificado_Recuo_Primeira_Linha, Estilo"
        ).click()
    else:
        pass
    page1.get_by_role("button", name="Salvar").click()
    page1.close()


def download_file(page):
    # 4. Baixar o arquivo
    page.locator('iframe[name="ifrVisualizacao"]').content_frame.get_by_role(
        "link", name="Gerar Arquivo PDF do Documento"
    ).click()
    page.locator('iframe[name="ifrVisualizacao"]').content_frame.get_by_role(
        "button", name="Gerar"
    ).click

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
