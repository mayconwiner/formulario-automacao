import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils import setup_driver, realizar_login, escolher_planilha, limpar_console, verificar_variaveis_ambiente
from preenche import preencher_acess_point, preencher_desktop, preencher_monitor, preencher_notebook, preencher_scanner, preencher_servidor, preencher_switch, preencher_impressora, preencher_unidade

abas = [
    "Access Point", "Desktop", "Monitor", "Notebook",
    "Scanner", "Servidor", "Switch", "Impressora"
]

def main():
    load_dotenv()
    limpar_console()
    verificar_variaveis_ambiente(["FORM_URL", "CHROME_USER_DATA"])
    navegador = setup_driver()

    navegador.get(os.getenv("FORM_URL"))
    time.sleep(3)

    if realizar_login(navegador):
        print("Login realizado com sucesso!")
    else:
        print("Login não requerido ou falhou. Continuando...")

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


#####

main()

load_dotenv()
limpar_console()
verificar_variaveis_ambiente(["FORM_URL", "CHROME_USER_DATA"])
navegador = setup_driver()
navegador.get(os.getenv("FORM_URL"))
planilha, dados = escolher_planilha("Levantamento.xlsx", abas)

navegador.find_element(By.XPATH, '//*[@id="question-list"]/div[2]/div[2]/div/div/div').click()
opcoes = navegador.find_elements(By.XPATH, '//div[@role="option"]')
for opcao in opcoes:
    spans = opcao.find_elements(By.TAG_NAME, 'span')
    if len(spans) >= 2 and spans[1].text.strip() == 'TO':
        spans[1].click()
        break


preencher_acess_point(navegador, dados)

preencher_unidade(navegador, dados)


btcity = navegador.find_element(By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "css-187", " " ))]')
navegador.execute_script("arguments[0].click();", btcity)
