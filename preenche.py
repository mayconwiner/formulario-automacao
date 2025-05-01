import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def preenchimento_inicial(driver):
    
    try:
        campo_estado = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="question-list"]/div[2]/div[2]/div/div/div'))
        )
        ActionChains(driver).move_to_element(campo_estado).click().perform()
        time.sleep(1)
        opcoes = driver.find_elements(By.XPATH, '//div[@role="button" and @aria-expanded="true"]')
        for opcao in opcoes:
            spans = opcao.find_elements(By.TAG_NAME, 'span')
            if len(spans) >= 2 and spans[1].text.strip() == 'TO':
                spans[1].click()
                return True
                break
    except Exception as e:
        print(f"Erro ao selecionar unidade: {e}")
        return False

    # try:
    #     input_sala = WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.XPATH, '//*[@id="question-list"]/div[3]/div[2]/div/span/input'))
    #     )
    #     input_sala.clear()
    #     input_sala.send_keys(str(sala))
    # except Exception as e:
    #     print(f"Erro ao preencher sala: {e}")
    #     return False

    # try:
    #     botao_avancar = driver.find_element(By.XPATH, '//*[@id="form-main-content1"]/div/div/div[2]/div[3]/div/button[2]')
    #     botao_avancar.click()
    #     time.sleep(2)
    # except Exception as e:
    #     print(f"Erro ao clicar em avançar: {e}")
    #     return False

    # return True

def preencher_do_inicio(driver, dados, tipo):
    print(f"Preenchendo dados desde o inicio ESTADO {tipo}...")
    sucesso = preenchimento_inicial(driver)
  
    

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