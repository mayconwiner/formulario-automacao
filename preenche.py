import time,os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import limpar_console, salvar_progresso, carregar_progresso

def preencher_equipamento(driver, dados, tipo):
    limpar_console()
    print(f"Preenchendo dados do Equipamento...{tipo}")
    print(dados.head())
    time.sleep(2)
    #inicio = carregar_progresso("Access Point")

    # for linha in dados.index:
    #     if linha < inicio:
    #         continue # pular linhas já preenchidas
    #     modelo = dados.loc[linha, 'QUAL_O_MODELO']
    # unidade = dados.loc[linha, 'UNIDADE']
    #print(f"Preenchendo dados do equipamento: {tipo} ")
    try:
        campo_equipamento = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="question-list"]/div[2]/div[2]/div/div/div'))
        )
        ActionChains(driver).move_to_element(campo_equipamento).click().perform()
        time.sleep(1)

        opcoes = driver.find_elements(By.XPATH, '//div[@role="option"]')
      
        for opcao in opcoes:
            spans = opcao.find_elements(By.TAG_NAME, 'span')
            if len(spans) >= 2 and spans[1].text.strip() == tipo:
                spans[1].click()
                time.sleep(1)
            driver.find_element(By.XPATH, '//*[@id="form-main-content1"]/div/div/div[2]/div[3]/div/button[2]').click()                    
            
            return True
    except Exception as e:
        print(f"Erro ao preencher equipamento: {e}")
        return False

def preencher_unidade(driver, dados):
    limpar_console()
    print("Preenchendo dados desde o inicio UNIDADE...")
    print(dados.head())

    inicio = carregar_progresso("Access Point")

    for linha in dados.index:
        if linha < inicio:
            continue # pular linhas já preenchidas
        
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
            encontrou = False
            for opcao in opcoes:
                spans = opcao.find_elements(By.TAG_NAME, 'span')

                if len(spans) >= 2 and spans[1].text.strip() == unidade:
                    spans[1].click()
                    time.sleep(1)
                    campo_sala = driver.find_element(By.XPATH, '//*[@id="question-list"]/div[3]/div[2]/div/span/input')
                    campo_sala.clear()
                    time.sleep(1)
                    campo_sala.send_keys(str(sala))
                    time.sleep(1)
                    botao_salvar = driver.find_element(By.XPATH, '//*[@id="form-main-content1"]/div/div/div[2]/div[3]/div/button[2]')
                    botao_salvar.click()
                    print(f"linha {linha + 1} preenchida com sucesso para a sala {str(sala)}")
                    time.sleep(2)
                    encontrou = True
                    break

                if not encontrou:
                    print(f"Unidade {unidade} não encontrada na linha {linha + 1}.")
                    continue
            #salvar_progresso("Access Point", linha + 1)  # Salva o progresso após cada linha preenchida
                
        except Exception as e:
            print(f"Erro ao preencher a linha {linha + 1}: {e}")
            continue

    print("Preenchimento de dados em Lote concluido")
    return True

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
                time.sleep(3)
                #driver.refresh()
                #aguarda, localiza e clica na cidade Palmas
                campo_cidade = WebDriverWait(driver, 10).until(
                 EC.presence_of_element_located((By.XPATH, '//*[@id="question-list"]/div[2]/div[2]/div/div/div'))
                 )
                ActionChains(driver).move_to_element(campo_cidade).click().perform()
                time.sleep(2)
                opcoesCity = driver.find_elements(By.XPATH, '//div[@role="option"]')
                for opcao in opcoesCity:
                    # spans = opcao.find_elements(By.TAG_NAME, 'span')
                    # if len(spans) >= 2 and spans[1].text.strip() == 'Palmas':
                    #     spans[1].click()
                    #     time.sleep(1)
                    if opcao.text == "Palmas":
                        opcao.click()
                        time.sleep(1)
                        break
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
  
    

def preencher_acess_point(driver, dados,tipo):
    preencher_do_inicio(driver, dados, "Access Point")
    preencher_unidade(driver, dados)
    preencher_equipamento(driver, dados, "Access Point")
    limpar_console()

    print(f"Preenchendo o Formulario {tipo}...")
    print(dados.head())

    inicio = carregar_progresso(tipo)

    for linha in dados.index:
        if linha < inicio:
            continue # pular linhas já preenchidas
        unidade = dados.loc[linha, 'UNIDADE']
        temos_na_unidade = dados.loc[linha, 'TEMOS_NA_UNIDADE']
        sala = dados.loc[linha, 'SALA']
        modelo = dados.loc[linha, 'QUAL_O_MODELO']
        qt = dados.loc[linha, 'QUANTIDADE']

        radios = driver.find_elements(By.XPATH, '//input[@role="radio"]')
        for radio in radios:
            if radio.get_attribute('value') == temos_na_unidade.upper():
                radio.click()
                break
        driver.find_element(By.XPATH, '//*[@id="question-list"]/div[3]/div[2]/div/span/input').clear()
        driver.find_element(By.XPATH, '//*[@id="question-list"]/div[3]/div[2]/div/span/input').send_keys(modelo)
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="question-list"]/div[4]/div[2]/div/span/input').clear()
        time.sleep(2)
        driver.find_element(By.XPATH, '//*[@id="question-list"]/div[4]/div[2]/div/span/input').send_keys(str(qt))
        time.sleep(2)
        break
    salvar_progresso(tipo, linha + 1)  # Salva o progresso após cada linha preenchida
    

        

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

