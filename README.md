# SEI_Playwright

## Resumo do Projeto

Este projeto automatiza interações com o sistema SEI (Sistema Eletrônico de Informações) utilizando Playwright, uma biblioteca de automação de navegadores.

### Funcionalidades Principais

- Automação de workflows no SEI
- Navegação e manipulação de elementos web
- Processamento em lote de documentos

### Tecnologias

- **Playwright** - Automação de navegador
- **Python** - Linguagem principal

### Estrutura

```
SEI_Playwright/
── src/
│   ├── main.py                    # Ponto de entrada do sistema
│   ├── config/
│   │   └── settings.py            # Contém save_prefs() e load_prefs()
│   ├── automations/
│   │   └── sei_automation.py      # Lógica do run_playwright() isolada
│   └── ui/
│       ├── app_window.py          # Classe principal (Controller das telas)
│       └── views/
│           ├── login_view.py      # Tela de login
│           ├── menu_view.py       # Seu novo submenu
│           └── task_view.py       # Tela secundária de parâmetros/execução
└── README.md
```

### Como Usar

1. Instale as dependências: `pip install -r requirements.txt`
2. Configure as credenciais do SEI
3. Execute os scripts conforme necessário
