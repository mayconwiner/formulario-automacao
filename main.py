import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from utils import setup_driver, realizar_login, escolher_planilha, limpar_console, verificar_variaveis_ambiente
from preenche import preencher_acess_point, preencher_desktop, preencher_monitor, preencher_notebook, preencher_scanner, preencher_servidor, preencher_switch, preencher_impressora

#remover
from selenium.webdriver.common.by import By
abas = [
    "Access Point", "Desktop", "Monitor", "Notebook",
    "Scanner", "Servidor", "Switch", "Impressora"
]

def main():
    load_dotenv()
    limpar_console()
    verificar_variaveis_ambiente(["FORM_URL", "CHROME_USER_DATA"])
    navegador = setup_navegador()

    navegador.get(os.getenv("FORM_URL"))
    time.sleep(3)

    if realizar_login(navegador):
        print("Login realizado com sucesso!")
    else:
        print("Login não requerido ou falhou. Continuando...")
# 
    planilha, dados = escolher_planilha("Levantamento.xlsx", abas)
    if planilha == "Access Point":
        preencher_acess_point(navegador, dados)
    elif planilha == "Desktop":
        preencher_desktop(navegador, dados)
    elif planilha == "Monitor":
        preencher_monitor(navegador, dados)
    elif planilha == "Notebook":
        preencher_notebook(navegador, dados)
    elif planilha == "Scanner":
        preencher_scanner(navegador, dados)
    elif planilha == "Servidor":
        preencher_servidor(navegador, dados)
    elif planilha == "Switch":
        preencher_switch(navegador, dados)
    elif planilha == "Impressora":
        preencher_impressora(navegador, dados)
    elif planilha == "Iniciar":
            preencher_impressora(navegador, dados)

    print("Processo finalizado.")

if __name__ == "__main__":
    main()

