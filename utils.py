import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def salvar_progresso(aba, linha_atual):
    with open(f"progresso_{aba}.txt", "w") as f:
        f.write(str(linha_atual))

def carregar_progresso(aba):
    try:
        with open(f"progresso_{aba}.txt", "r") as f:
            return int(f.read())
    except:
        return 0
    

def limpar_progresso(aba):
    try:
        os.remove(f"progresso_{aba}.txt")
    except Exception as e:
        print(f"Erro ao limpar progresso: {e}")
        return False







def limpar_console():
    os.system("cls" if os.name == "nt" else "clear")

def verificar_variaveis_ambiente(variaveis):
    faltantes = [var for var in variaveis if not os.getenv(var)]
    if faltantes:
        raise EnvironmentError(f"Variáveis de ambiente ausentes: {', '.join(faltantes)}")

def setup_driver():
    options = webdriver.ChromeOptions()
    user_data = os.getenv("CHROME_USER_DATA")
    if user_data:
        options.add_argument(f"--user-data-dir={user_data}")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    return driver

def realizar_login(driver):
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "cantAccessAccount"))
        )
        username = os.getenv("HEPTA_USER")
        password = os.getenv("HEPTA_PASS")
        driver.find_element(By.NAME, "loginfmt").send_keys(username)
        driver.find_element(By.ID, "idSIButton9").click()
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "i0118"))
        )
        driver.find_element(By.ID, "i0118").send_keys(password)
        driver.find_element(By.ID, "idSIButton9").click()
        return True
    except:
        return False

def escolher_planilha(caminho, abas):
    print("Selecione uma opção:\n")
    for i, aba in enumerate(abas):
        print(f"{i + 1} - {aba}")

    while True:
        try:
            escolha = int(input("\nDigite o número da opção desejada: "))
            if 1 <= escolha <= len(abas):
                aba_escolhida = abas[escolha - 1]
                print(f"\nVocê escolheu: {aba_escolhida}")
                dados = pd.read_excel(caminho, sheet_name=aba_escolhida)
                return aba_escolhida, dados
            else:
                print("Opção inválida. Tente novamente.")
        except ValueError:
            print("Por favor, digite um número válido.")