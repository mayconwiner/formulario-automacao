import time,os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def preencher_equipamento(driver, dados, tipo):
    print(f"Preenchendo dados do equipamento {tipo}...")
    print("Maycon Douglas")
    try:
        campo_unidade = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="question-list"]/div[2]/div[2]/div/div/div'))
            )
        ActionChains(driver).move_to_element(campo_unidade).click().perform()
        campo_unidade.click()
        time.sleep(1)
        opcoes = driver.find_elements(By.XPATH, '//div[@role="option"]')
        for opcao in opcoes:
            spans = opcao.find_elements(By.TAG_NAME, 'span')
            if len(spans) >= 2 and spans[1].text.strip() == tipo:
                spans[1].click()
                time.sleep(2)
                break 
    except Exception as e:
        print(f"Erro ao preencher equipamento: {e}")
        return False

def preencher_unidade(driver, dados, tipo):

    print(f"Preenchendo dados da unidade {tipo}...")
    for linha in dados.index:
        unidade = dados.loc[linha, 'UNIDADE']
        sala = dados.loc[linha, 'SALA']
        print(f"Inserindo dados da linha {linha + 1}... unidade: {unidade} sala: {sala}")
        try:
            campo_unidade = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="question-list"]/div[2]/div[2]/div/div/div'))
            )
            ActionChains(driver).move_to_element(campo_unidade).click().perform()
            campo_unidade.click()
            time.sleep(1)
            opcoes = driver.find_elements(By.XPATH, '//div[@role="option"]')
            for opcao in opcoes:
                spans = opcao.find_elements(By.TAG_NAME, 'span')
                if len(spans) >= 2 and spans[1].text.strip() == unidade:
                    spans[1].click()
                    time.sleep(2)
                    break 
        
        except Exception as e:
            print(f"Erro ao preencher unidade: {e}")
            return False
        #preenchendo a sala 
        try:
            campo_sala = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="question-list"]/div[3]/div[2]/div/span/input'))
            )
            ActionChains(driver).move_to_element(campo_sala).click().perform()
            campo_sala.clear()
            campo_sala.click()
            campo_sala = driver.find_element(By.XPATH, '//*[@id="question-list"]/div[3]/div[2]/div/span/input') 
            campo_sala.send_keys(str(sala))
            time.sleep(1)
            break
        except Exception as e:
            print(f"Erro ao preencher sala: {e}")
            return False
    driver.find_element(By.XPATH, '//*[@id="form-main-content1"]/div/div/div[2]/div[3]/div/button[2]').click()
    # equipa = preencher_equipamento(driver, dados, tipo)
    # if not equipa:
    #     print("Erro ao preencher equipamento. Abortando o preenchimento.")
    #     return False

def preenchimento_inicial(driver,dados,tipo):
    
    try:
        campo_estado = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="question-list"]/div[2]/div[2]/div/div/div'))
        )
        ActionChains(driver).move_to_element(campo_estado).click().perform()
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="form-main-content1"]/div/div/div[2]/div[3]/div/button').click()
        opcoes = driver.find_elements(By.XPATH,  '//div[@role="option"]')
        for opcao in opcoes:
            spans = opcao.find_elements(By.TAG_NAME, 'span')
            if len(spans) >= 2 and spans[1].text.strip() == 'Palmas':
                spans[1].click()
                time.sleep(2)
                
    except Exception as e:
        pass
        
def voltar(driver):
    driver.back()
    driver.get(os.getenv("FORM_URL"))
    time.sleep(2)
    try:
        btvoltar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="form-main-content1"]/div/div/div[2]/div[3]/div/button[1]'))
        )
        ActionChains(driver).move_to_element(btvoltar).click().perform()
        btvoltar.click()
        preencher_acess_point(driver)
    except Exception as e:
        print(f"Erro ao voltar: {e}")
        return False

    
def preencher_do_inicio(driver, dados, tipo):
    print(f"Preenchendo dados desde o inicio ESTADO {tipo}...")
    sucesso = preenchimento_inicial(driver,dados,tipo)
    if not sucesso:
        for i in range(3):
            try:
                voltar(driver)
            except Exception as e:
                print(f"Erro ao voltar: {e}")
                continue
                time.sleep(2)
        print("Erro ao preencher o estado. Abortando o preenchimento.")

    #unidade_success = preencher_unidade(driver, dados, tipo)   
    # if not unidade_success:
    #     print("Erro ao preencher a unidade. Abortando o preenchimento.")
    #     return False    
  
    

def preencher_acess_point(driver, dados):
    preencher_do_inicio(driver, dados, "Access Point")

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

