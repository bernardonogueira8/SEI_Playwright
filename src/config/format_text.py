# Este módulo contém funções para formatar texto de acordo com as necessidades do sistema SEI.
# Ele é utilizado para garantir que o conteúdo inserido no SEI mantenha a formatação
def formatar_para_sei(content):
    if not content:
        return ""
    # 1. Tratamos os recuos de 4 espaços primeiro
    content = content.replace("    ", "&nbsp;&nbsp;&nbsp;&nbsp;")

    # 2. Dividimos o texto por linhas e limpamos espaços vazios no fim de cada uma
    linhas = content.split("\n")
    # 3. Envolvemos cada linha em um <p> com a classe que o SEI usa
    # Se a linha estiver vazia, colocamos um <br/> dentro do <p> para manter o espaço
    content = ""
    for linha in linhas:
        texto_linha = linha if linha.strip() else "<br/>"
        content += (
            f'<p class="Texto_Justificado_Recuo_Primeira_Linha">{texto_linha}</p>'
        )

    # Retornamos o HTML puro (o json.dumps deve ser usado no momento da injeção no SEI_DMA.py)
    return content
