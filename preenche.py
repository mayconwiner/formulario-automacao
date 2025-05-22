import time,os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import limpar_console, salvar_progresso, carregar_progresso
from selenium.webdriver.common.keys import Keys

#metodo para retornar o formulario para o inicio 
def voltar_inicio(driver,dados):
    # while True:
            
    #     try:
    #         voltar = WebDriverWait(driver, 10).until(
    #             EC.presence_of_element_located((By.XPATH, '//*[@id="form-main-content1"]/div/div/div[2]/div[3]/div/button[1]'))
    #         )
    #         ActionChains(driver).move_to_element(voltar).click().perform()
    #         time.sleep(1)
    #         return True
    #     except Exception as e:
    #         print(f"Erro ao clicar no botão de voltar: {e}")
    #         return False
    
    # while len(driver.find_elements(By.XPATH, '//*[@id="form-main-content1"]/div/div/div[2]/div[3]/div/button[1]')) < 1:
    #     time.sleep(1)
    # time.sleep(1)
    limpar_console()
    for i in range(4):
        try:
            botao1 = driver.find_element(By.XPATH, '//*[@id="form-main-content1"]/div/div/div[2]/div[3]/div/button[1]')
            botao2 = driver.find_element(By.XPATH, '//*[@id="form-main-content1"]/div/div/div[2]/div[3]/div/button[2]')
            if botao1.is_displayed() and botao2.is_displayed():
                botao1.click()
                limpar_console()
                time.sleep(1)
                print(dados.head())
                print(f'Ops!!!! Voltando {i+1} vez')
            else:
                print(f"Botão de voltar não encontrado na tentativa {i+1}.")
                time.sleep(1)
                break
        except Exception as e:
            print(f"Erro ao clicar no botão de voltar: {e}")
            time.sleep(1)
            return False
    return True

        



#verifica se existe mais informações para adicionar e chama a função 
def limpar_campos_texto(driver, tempo_espera=10):
    """
    Limpa todos os campos de texto com data-automation-id="textInput" (Texto de linha única).
    """
    try:
        WebDriverWait(driver, tempo_espera).until(
            EC.presence_of_element_located((By.XPATH, '//input[@data-automation-id="textInput"]'))
        )

        campos_texto = driver.find_elements(By.XPATH, '//input[@data-automation-id="textInput"]')

        print(f"Encontrados {len(campos_texto)} campos de texto com 'data-automation-id=textInput'. Limpando...")

        for campo in campos_texto:
            try:
                campo.clear()
            except Exception as e:
                print(f"Erro ao limpar campo: {e}")

        print("Todos os campos de texto foram limpos com sucesso.")

    except Exception as erro:
        print(f"Erro ao localizar campos: {erro}")

def verificador_progresso(driver, dados, tipo,funcao):
    limpar_console()
    print(f"{dados.head()}")
    # Verifica se o progresso foi salvo corretamente
    try:
        progresso = carregar_progresso(tipo)
        if progresso is not None:
            print(f"Progresso salvo: {progresso}")
            if progresso >= len(dados):
                print("Todos os dados foram preenchidos.")
                return False
            else:
                print(f"Próxima linha a ser preenchida: {progresso + 1}")
                
                return True
    except Exception as e:
        print(f"Erro ao carregar progresso: {e}")


def preencher_equipamento(driver, dados, tipo):
    limpar_console()
    print(f"Preenchendo dados do Equipamento...{tipo}")
    print(dados.head())
    #time.sleep(0.5)

    try:
        campo_equipamento = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="question-list"]/div[2]/div[2]/div/div/div'))
        )
        ActionChains(driver).move_to_element(campo_equipamento).click().perform()
        time.sleep(0.5)
        
        opcoes = driver.find_elements(By.XPATH, '//div[@role="option"]')
        encontrou = False
        for opcao in opcoes:
            spans = opcao.find_elements(By.TAG_NAME, 'span')
            if len(spans) >= 2 and spans[1].text.strip() == tipo:
                spans[1].click()
                time.sleep(0.5)
                Keys.TAB
                time.sleep(0.5)
                driver.find_element(By.XPATH, '//*[@id="form-main-content1"]/div/div/div[2]/div[3]/div/button[2]').click()
                encontrou = True
                break
            if not encontrou:
                print(f"Equipamento {tipo} não encontrado.")
                limpar_console()
                continue
    except Exception as e:
        print(f"Erro ao selecionar unidade: {e}")
    print(f"Preenchimento de equipamento do {tipo} concluido")
    #time.sleep(1)

   
  

def preencher_unidade(driver, dados,tipo):
    limpar_console()
    print("Preenchendo dados de UNIDADE...")
    print(dados.head())
    
    inicio = carregar_progresso(tipo)

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
                    time.sleep(1)
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
    print(f"Preenchendo da base de dados:  {tipo}...")
    sucesso = preenchimento_inicial(driver)
    if not sucesso:
        print("Falha ao preencher o estado. Encerrando.")
        return
  
    

def preencher_acess_point(driver, dados,tipo):
    preencher_do_inicio(driver, dados, tipo)
    preencher_unidade(driver, dados,tipo)
    preencher_equipamento(driver, dados, tipo)
    limpar_console()
    progresso = carregar_progresso(tipo)

    print(f"Preenchendo o Formulario {tipo} na linha...{progresso + 1} de len(dados) registros : ")
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
        time.sleep(5)
        btn_enviar = driver.find_element(By.XPATH, '//*[@id="form-main-content1"]/div/div/div[2]/div[3]/div/button[2]')
        #btn_enviar.click()
        break
    salvar_progresso(tipo, linha + 1)  # Salva o progresso após cada linha preenchida
    time.sleep(3)
        
    try:
        link_enviar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="form-main-content1"]/div/div/div[2]/div[1]/div[2]/div[5]/span'))
            )
        ActionChains(driver).move_to_element(link_enviar).click().perform()
        time.sleep(1)
    except Exception as e:
            print(f"Erro ao clicar em Enivar outra resposta: {e}")
            

        

def preencher_desktop(driver, dados):
    preencher_do_inicio(driver, dados, "Desktop")

def preencher_monitor(driver, dados):
    preencher_do_inicio(driver, dados, "Monitor")

def preencher_notebook(driver, dados):
    preencher_do_inicio(driver, dados, "Notebook")

def preencher_scanner(driver, dados):
    preencher_do_inicio(driver, dados, "Scanner")

def preencher_servidor(driver, dados, tipo):
    preencher_do_inicio(driver, dados,tipo)
    preencher_unidade(driver, dados,tipo)
    preencher_equipamento(driver, dados, tipo)
    limpar_console()
    inicio = carregar_progresso(tipo)
    print(f"Preenchendo o Formulario {tipo} na linha...{inicio + 1} de {len(dados)} registros : ")
    #print(f"Preenchendo o Formulario {tipo}...")
    time.sleep(2)
    print(dados.head())

    #inicio = carregar_progresso(tipo)

    for linha in dados.index:
        if linha < inicio:
            continue # pular linhas já preenchidas
        try:
            marca = dados.loc[linha, 'SERVIDOR_MARCA']
            modelo = dados.loc[linha, 'SERVIDOR_MODELO']
            hostname = dados.loc[linha, 'SERVIDOR_HOSTNAME']
            servidor_os = dados.loc[linha, 'SERVIDOR_SO']
            num_serie = dados.loc[linha, 'SERVIDOR_NUM_SERIE']
            patrimonio = dados.loc[linha, 'SERVIDOR_PATRIMONIO']

            #espera e coleta todos os campos de texto da tela  
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@data-automation-id="textInput"]'))
            )  
            campos = driver.find_elements(By.XPATH, '//input[@data-automation-id="textInput"]')

            #limpa e preenche na ordem correta
            valores = [marca, modelo, hostname, servidor_os, num_serie, patrimonio]
            for campo, valor in zip(campos, valores):
                campo.clear()
                campo.send_keys(str(valor))
                time.sleep(1)
            botao_enviar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="form-main-content1"]/div/div/div[2]/div[3]/div/button[2]'))
            )
            #Envia o preenchimento do formulario  
            botao_enviar.click()
            print(botao_enviar.text)

            salvar_progresso(tipo, linha + 1)  # Salva o progresso após cada linha preenchida
            time.sleep(3)

            #usado para voltar para o inicio, fim de testes comente o  botao_enviar.click()
            #voltar_inicio(driver,dados)    
            #time.sleep(3)   
            link_enviar = WebDriverWait(driver, 10).until(
                 EC.presence_of_element_located((By.XPATH, '//*[@id="form-main-content1"]/div/div/div[2]/div[1]/div[2]/div[5]/span'))
                 )
            ActionChains(driver).move_to_element(link_enviar).click().perform()
            time.sleep(3)
            break

        except Exception as e:
            print(f"Erro ao acessar dados da linha {linha + 1}: {e}")
            # continue
   


def preencher_switch(driver, dados):
    preencher_do_inicio(driver, dados, "Switch")

def preencher_impressora(driver, dados):
    preencher_do_inicio(driver, dados, "Impressora")

