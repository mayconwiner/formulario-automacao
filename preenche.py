import time,os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import limpar_console



def preencher_unidade(driver, dados):
    limpar_console()
    print("Preenchendo dados desde o inicio UNIDADE...")
    print(dados.head())

    for linha in dados.index:
        unidade = dados.loc[linha, 'UNIDADE']
        sala = dados.loc[linha, 'SALA']
        print(f"Preenchendo linha {linha + 1} de {len(dados)} para a sala {str(sala)} ")
        try:
            campo_unidade = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="question-list"]/div[2]/div[2]/div/div/div'))
            )
            ActionChains(driver).move_to_element(campo_unidade).click().perform()
            time.sleep(1)
            opcoes = driver.find_elements(By.XPATH, '//div[@role="option"]')
            for opcao in opcoes:
                spans = opcao.find_elements(By.TAG_NAME, 'span')

                if len(spans) >= 2 and spans[1].text.strip() == unidade:
                    spans[1].click()
                    time.sleep(1)
                    driver.find_element(By.XPATH, '//*[@id="question-list"]/div[3]/div[2]/div/span/input').clear()
                    time.sleep(1)
                    driver.find_element(By.XPATH, '//*[@id="question-list"]/div[3]/div[2]/div/span/input').send_keys(str(sala))
                    time.sleep(1)
                    driver.find_element(By.XPATH, '//*[@id="form-main-content1"]/div/div/div[2]/div[3]/div/button[2]').click()
        
                    return True
        except Exception as e:
            print(f"Erro ao selecionar unidade: {e}")
            return False

def preenchimento_inicial(driver):
    
    try:
        campo_estado = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="question-list"]/div[2]/div[2]/div/div/div'))
        )
        ActionChains(driver).move_to_element(campo_estado).click().perform()
        time.sleep(1)
        opcoes = driver.find_elements(By.XPATH, '//div[@role="option"]')
        for opcao in opcoes:
            spans = opcao.find_elements(By.TAG_NAME, 'span')
            if len(spans) >= 2 and spans[1].text.strip() == 'TO':
                spans[1].click()
                time.sleep(1)
                driver.find_element(By.XPATH, '//*[@id="form-main-content1"]/div/div/div[2]/div[3]/div/button').click()
                time.sleep(2)
                driver.refresh()
                time.sleep(2)
                driver.find_element(By.XPATH, '//*[@id="form-main-content1"]/div/div/div[2]/div[3]/div/button[2]').click()
                return True
                #break
    except Exception as e:
        print(f"Erro ao selecionar unidade: {e}")
        return False
 

    
def preencher_do_inicio(driver, dados, tipo):
    print(f"Preenchendo dados desde o inicio ESTADO {tipo}...")
    sucesso = preenchimento_inicial(driver)
    if not sucesso:
        print("Falha ao preencher o estado. Encerrando.")
        return
  
    

def preencher_acess_point(driver, dados):
    preencher_do_inicio(driver, dados, "Access Point")
    preencher_unidade(driver, dados)
    


def preencher_desktop(driver, dados):
    preencher_do_inicio(driver, dados, "Desktop")

def preencher_monitor(driver, dados):
    preencher_do_inicio(driver, dados, "Monitor")

def preencher_notebook(driver, dados):
    preencher_do_inicio(driver, dados, "Notebook")

def preencher_scanner(driver, dados):
    preencher_do_inicio(driver, dados, "Scanner")

def preencher_servidor(driver, dados):
    preencher_do_inicio(driver, dados, "Servidor")

def preencher_switch(driver, dados):
    preencher_do_inicio(driver, dados, "Switch")

def preencher_impressora(driver, dados):
    preencher_do_inicio(driver, dados, "Impressora")

