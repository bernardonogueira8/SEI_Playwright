import os
import json

CONFIG_FILE = "config_sei.json"


def _load_full_config():
    """Função interna para ler todo o arquivo de uma vez."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def _save_full_config(config):
    """Função interna para salvar o dicionário completo."""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)


def save_prefs(user, pwd, remember):
    config = _load_full_config()
    config["user"] = user if remember else ""
    config["pwd"] = pwd if remember else ""
    config["remember"] = remember
    _save_full_config(config)


def load_prefs():
    config = _load_full_config()
    return {
        "user": config.get("user", ""),
        "pwd": config.get("pwd", ""),
        "remember": config.get("remember", False),
    }


def save_ass(content_ass):
    config = _load_full_config()
    config["content_ass"] = content_ass
    _save_full_config(config)


def load_ass():
    config = _load_full_config()
    # Retorna apenas a string da assinatura para facilitar o uso no seu código
    return config.get("content_ass", "")
