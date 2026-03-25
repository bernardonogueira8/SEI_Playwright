import logging
import json
import os
from playwright.sync_api import sync_playwright

# Configuração de um logger para rastrear os passos da automação
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def run_playwright(user, pwd, title, content):
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
            numero_sei = create_process(page, title, content)
            download_file(page)
            browser.close()
            return numero_sei  # Retorna o número do processo/Documento criado para exibir na UI

    except Exception as e:
        logger.error(f"Erro: {e}")
        raise e


def open_browser(page, user, pwd):
    # 1. Login
    page.goto("https://seibahia.ba.gov.br")
    page.get_by_role("textbox", name="Usuário").fill(user)
    page.get_by_role("textbox", name="Senha").fill(pwd)
    page.locator("#selOrgao").select_option("23")  # Exemplo: CGTICS ou SESAB
    page.get_by_role("button", name="ACESSAR").click()


def create_process(page, title, content):
    # 2. Criar Processo
    page.get_by_role("link", name="Iniciar Processo").click()
    # Ajuste o nome do tipo de processo conforme sua necessidade real
    page.get_by_role("link", name="Documento tramitável: Comunicação Interna").click()
    page.get_by_role("textbox", name="Especificação:").click()
    page.get_by_role("textbox", name="Especificação:").fill(title)
    page.locator("#divInfraBarraComandosSuperior").get_by_role(
        "button", name="Salvar"
    ).click()
    # 2. Incluir em Tag
    page.locator('iframe[name="ifrVisualizacao"]').content_frame.get_by_role(
        "link", name="Gerenciar Marcador"
    ).click()
    page.locator('iframe[name="ifrVisualizacao"]').content_frame.locator("a").nth(
        1
    ).click()
    page.locator('iframe[name="ifrVisualizacao"]').content_frame.locator("a").filter(
        has_text="TI/DMA"
    ).click()
    page.locator('iframe[name="ifrVisualizacao"]').content_frame.get_by_role(
        "button", name="Salvar"
    ).click()

    # Capturar o número do SEI
    tree_frame = page.frame_locator("#ifrArvore")
    span_processo = tree_frame.locator(".infraArvoreNoSelecionado")
    numero_sei = span_processo.inner_text()

    print(f"Processo/Documento identificado: {numero_sei}")
    # Clicar no link (<a>) que contém esse número
    tree_frame.locator("a:has(.infraArvoreNoSelecionado)").click()

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

    # 3. Editando o Despacho
    page1 = page1_info.value
    page1.locator('iframe[title="Processo e Interessado"]').content_frame.get_by_text(
        "Insira aqui o órgão"
    ).click()
    page1.locator('iframe[title="Processo e Interessado"]').content_frame.get_by_role(
        "cell", name="[Insira aqui o órgão"
    ).fill("CGTICS")
    page1.locator('iframe[title="Corpo do Texto"]').content_frame.get_by_text(
        "[Insira aqui o conteúdo do"
    ).click()
    content = json.dumps(content)
    page1.locator('iframe[title="Corpo do Texto"]').content_frame.get_by_text(
        "[Insira aqui o conteúdo do"
    ).evaluate(f"(el) => el.innerHTML = {content}")
    page1.get_by_role("button", name="Salvar").click()
    page1.close()
    # Clicar no link (<a>) que contém esse número
    tree_frame.locator("a:has(.infraArvoreNoSelecionado)").click()

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
    # Clicar no link (<a>) que contém esse número
    tree_frame.locator("a:has(.infraArvoreNoSelecionado)").click()

    return numero_sei


def download_file(page, save_path="downloads/"):
    # Garante que a pasta de destino existe (bom para o seu projeto de TI)
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # 1. Localiza a árvore e garante que o documento certo está clicado
    tree_frame = page.frame_locator("#ifrArvore")
    tree_frame.locator("a:has(.infraArvoreNoSelecionado)").click()

    # 2. Acessa o frame de visualização
    visualizacao_frame = page.locator('iframe[name="ifrVisualizacao"]').content_frame

    # 3. Clica para abrir a tela de geração de PDF
    visualizacao_frame.get_by_role(
        "link", name="Gerar Arquivo PDF do Documento"
    ).click()

    # 4. processar o PDF
    try:
        with page.expect_download(timeout=60000) as download_info:
            visualizacao_frame.get_by_role(
                "button", name="Gerar"
            ).click()  # Corrigido: adicionado ()

        download = download_info.value

        # Salva o arquivo
        final_path = os.path.join(save_path, download.suggested_filename)
        download.save_as(final_path)

        print(f"PDF salvo com sucesso em: {final_path}")
        return final_path

    except Exception as e:
        print(f"Erro ao baixar o PDF: {e}")
        return None
