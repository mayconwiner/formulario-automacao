import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import limpar_console

def preenchimento_inicial(driver, dados, tipo):
    try:
        campo_estado = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="question-list"]/div[2]/div[2]/div/div/div'))
        )
        ActionChains(driver).move_to_element(campo_estado).click().perform()
        
        # Esperar explicitamente pelas opções
        opcoes = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@role="option"]'))
        )
        
        for opcao in opcoes:
            spans = opcao.find_elements(By.TAG_NAME, 'span')
            for i, span in enumerate(spans):
                print(f"span[{i}] = '{span.text.strip()}'")
            if len(spans) >= 2 and spans[1].text.strip() == 'TO':
                driver.execute_script("arguments[0].click();", spans[1])
                print("Clique realizado com sucesso em TO.")
                driver.refresh()
                time.sleep(2)
                driver.find_element(By.XPATH, '//*[@id="form-main-content1"]/div/div/div[2]/div[3]/div/button').click()
                #driver.execute_script("arguments[0].click();", botao)
                limpar_console()
                time.sleep(3)
                driver.find_element(By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "css-187", " " ))]').click()
                return True
    except Exception as e:
        print(f"Erro detalhado: {repr(e)}")
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
    sucesso = preenchimento_inicial(driver,dados,tipo)
    if not sucesso:
        print("Erro ao preencher os dados iniciais.")
        return



def preencher_unidade(driver, dados):
    print(f"preenchendo a unidade...{dados.head()}")
    time.sleep(2)
    for linha in dados.index:
        unidade = dados.loc[linha, 'UNIDADE']
        sala = dados.loc[linha, 'SALA']
        print(f"Inserinod dados da linha {linha}: Unidade {unidade} e Sala {sala}")
        try:
            campo_unidade = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="question-list"]/div[2]/div[2]/div/div/div'))
            )
            ActionChains(driver).move_to_element(campo_unidade).click().perform()
            time.sleep(2)
            campo_unidade = dados.loc[linha, 'UNIDADE']
            opcoes = driver.find_elements(By.XPATH, '//div[@role="option"]')
            for opcao in opcoes:
                spans = opcao.find_elements(By.TAG_NAME, 'span')
                for i, span in enumerate(spans):
                    print(f"span[{i}] = '{span.text.strip()}'")
                if len(spans) >= 2 and spans[1].text.strip() == campo_unidade:
                    driver.execute_script("arguments[0].click();", spans[1])
                    print("Clique realizado com sucesso na unidade.")
                    #break
                    return True
        except Exception as e:
            print(f"Erro ao clicar no campo de estado: {e}")
            return False
    
            






 


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