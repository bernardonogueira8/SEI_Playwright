import logging
from playwright.sync_api import sync_playwright

# Configuração de um logger para rastrear os passos da automação
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def run_playwright(user, password, title, content):
    """
    Executa a rotina de automação no sistema SEI.

    Esta função recebe apenas dados puros (strings, dicionários, etc.)
    e não tem NENHUMA dependência da interface gráfica (Tkinter).
    """
    logger.info(f"Iniciando automação no SEI para o usuário: {user} | Título: {title}")

    try:
        # Inicializa o Playwright de forma síncrona
        with sync_playwright() as p:
            # Lançando o Firefox conforme o seu código original, com slow_mo para visualização
            browser = p.firefox.launch(headless=False, slow_mo=500)  # [1]

            # Recomenda-se criar um contexto para isolar cookies e sessões
            context = browser.new_context()
            page = context.new_page()  # [1]

            logger.info("Navegador aberto. Acessando a página de login...")

            # --- SUA LÓGICA DE NAVEGAÇÃO ENTRA AQUI ---
            # Exemplo de preenchimento (substitua pelos seletores reais do SEI):
            # page.goto("https://url-do-sei.gov.br")
            # page.fill("input[name='usuario']", user)
            # page.fill("input[name='senha']", password)
            # page.click("button[id='btn-entrar']")

            # page.wait_for_load_state("networkidle")

            logger.info("Preenchendo o formulário de processo...")
            # page.fill("input[id='titulo']", title)
            # page.fill("textarea[id='conteudo']", content)

            # ------------------------------------------

            logger.info("Automação do SEI finalizada com sucesso.")

            # Fecha o contexto e o navegador
            context.close()
            browser.close()

    except Exception as e:
        logger.error(f"Erro crítico durante a execução da automação no SEI: {e}")
        # Lançar a exceção novamente é vital para que a Thread na interface
        # (TaskView) capture o erro e exiba um popup (ex: messagebox) avisando o usuário.
        raise e
