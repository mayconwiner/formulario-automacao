import time,os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import limpar_console, salvar_progresso, carregar_progresso
from selenium.webdriver.common.keys import Keys
from form_helpers import preencher_campos_texto, selecionar_dropdown_por_texto, clicar_radio_por_valor, selecionar_dropdown_modelo

#função generica para preenchimento de campos
def preencher_campos(driver,valores):
    """
    Preenche os campos de texto com os valores fornecidos.
    """
    try:
        # Espera até que o campo esteja presente
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@data-automation-id="textInput"]'))
        )
        
        campos = driver.find_elements(By.XPATH, '//input[@data-automation-id="textInput"]')

        # Preenche os campos com os valores fornecidos
        for campo, valor in zip(campos, valores):
            campo.clear()
            campo.send_keys(str(valor))
            time.sleep(1)

        print("Todos os campos foram preenchidos com sucesso.")

    except Exception as erro:
        print(f"Erro ao preencher campos: {erro}")

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
                print(f"Todos os dados foram preenchidos. {progresso} de {len(dados)} registros preenchidos.")
                return False
            else:
                print(f"Próxima linha a ser preenchida: {progresso + 1}")
                
                return True
    except Exception as e:
        print(f"Erro ao carregar progresso: {e}")

def preencher_equipamento(driver, dados, tipo):
    limpar_console()
    print(f"Preenchendo dados do Equipamento... {tipo}")
    print(dados.head())

    try:
        # Abre o dropdown de equipamentos
        campo_equipamento = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="question-list"]/div[2]/div[2]/div/div/div'))
        )
        campo_equipamento.click()

        # Busca todas as opções visíveis no menu
        opcoes = WebDriverWait(driver, 4).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@role="option"]'))
        )
       
        for opcao in opcoes:
            spans = opcao.find_elements(By.TAG_NAME, 'span')
           
            if len(spans) >= 2:
                texto = spans[1].text.strip()
                
                if texto.lower() == tipo.strip().lower():
                    print(f"Encontrado e selecionando: {texto}")
                    opcao.click()  # ou ActionChains(driver).move_to_element(opcao).click().perform()
                    
                    # Clica imediatamente em "Avançar"
                    WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="form-main-content1"]/div/div/div[2]/div[3]/div/button[2]'))
                    ).click()

                    print("Equipamento selecionado e avançou.")
                    return True

        print(f"Equipamento '{tipo}' não encontrado.")
        return False

    except Exception as e:
        print(f"Erro ao preencher equipamento '{tipo}': {e}")
        return False

def preencher_unidade(driver, dados, tipo):
    limpar_console()
    print("Preenchendo dados de UNIDADE...")
    
    # Correção: Tratamento mais robusto para valores de SALA
    def tratar_sala(x):
        if pd.isnull(x):  # Se for NaN/None
            return ""
        x_str = str(x).strip()  # Converte para string e remove espaços
        if x_str == "" or x_str.lower() == "nan":  # Se for string vazia ou "nan"
            return ""
        try:
            # Tenta converter para float primeiro (caso tenha decimais) e depois para int
            return str(int(float(x_str)))
        except (ValueError, TypeError):
            # Se não conseguir converter, retorna como string
            return x_str
    
    # Aplica o tratamento aos valores de SALA
    dados['SALA'] = dados['SALA'].apply(tratar_sala)
 
    print(dados.head())

    inicio = carregar_progresso(tipo)

    for linha in dados.index:
        if linha < inicio:
            continue

        unidade = str(dados.loc[linha, 'UNIDADE']).strip()
        sala = str(dados.loc[linha, 'SALA']).strip()
        print(f"Preenchendo linha {linha + 1} de {len(dados)} | Unidade: {unidade} | Sala: {sala}")

        try:
            # Abrir o campo de seleção
            campo_unidade = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="question-list"]/div[2]/div[2]/div/div/div'))
            )
            campo_unidade.click()

            # Buscar todas as opções visíveis
            WebDriverWait(driver, 4).until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[@role="option"]'))
            )
            opcoes = driver.find_elements(By.XPATH, '//div[@role="option"]')
            
            for opcao in opcoes:
                texto = opcao.text.strip()
                print(f"→ Verificando: {texto}")
                if texto.lower() == unidade.lower():
                    opcao.click()
                    print(f"✓ Unidade selecionada: {texto}")
                    break
            else:
                print(f"⚠ Unidade '{unidade}' não encontrada na linha {linha + 1}.")
                continue

            # Preencher o campo de sala
            campo_sala = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="question-list"]/div[3]/div[2]/div/span/input'))
            )
            campo_sala.clear()
            campo_sala.send_keys(sala)
            
            # Clicar em salvar/avançar
            WebDriverWait(driver, 4).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="form-main-content1"]/div/div/div[2]/div[3]/div/button[2]'))
            ).click()

            print(f"✔ Linha {linha + 1} preenchida com sucesso.\n")

        except Exception as e:
            print(f"❌ Erro na linha {linha + 1}: {e}")
            import traceback
            traceback.print_exc()
            continue

    print("✅ Preenchimento de todas as unidades concluído.")
    return True

def preenchimento_inicial(driver):
    try:
        # Seleciona o estado "TO"
        campo_estado = WebDriverWait(driver, 8).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="question-list"]/div[2]/div[2]/div/div/div'))
        )
        campo_estado.click()

        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@role="option"]'))
        )
        opcoes_estado = driver.find_elements(By.XPATH, '//div[@role="option"]')
        time.sleep(2)
        selecionou_estado = False
        for opcao in opcoes_estado:
            texto = opcao.text.strip()
            if texto.upper() == "TO":
                opcao.click()
                selecionou_estado = True
                print("Estado 'TO' selecionado.")
                break

        if not selecionou_estado:
            print("Estado 'TO' não encontrado.")
            return False

        # Clica em "Avançar"
        WebDriverWait(driver, 4).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="form-main-content1"]/div/div/div[2]/div[3]/div/button'))
        ).click()

        # Seleciona a cidade "Palmas"
        campo_cidade = WebDriverWait(driver, 8).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="question-list"]/div[2]/div[2]/div/div/div'))
        )
        campo_cidade.click()

        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@role="option"]'))
        )
        opcoes_cidade = driver.find_elements(By.XPATH, '//div[@role="option"]')

        selecionou_cidade = False
        for opcao in opcoes_cidade:
            texto = opcao.text.strip()
            if texto.lower() == "palmas":
                opcao.click()
                selecionou_cidade = True
                print("Cidade 'Palmas' selecionada.")
                break

        if not selecionou_cidade:
            print("Cidade 'Palmas' não encontrada.")
            return False

        # Clica em "Avançar"
        WebDriverWait(driver, 4).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="form-main-content1"]/div/div/div[2]/div[3]/div/button[2]'))
        ).click()

        print("Preenchimento inicial concluído.")
        return True

    except Exception as e:
        print(f"Erro no preenchimento inicial: {e}")
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


def preencher_notebook(driver, dados, tipo):
    preencher_do_inicio(driver, dados, tipo)
    preencher_unidade(driver, dados, tipo)
    preencher_equipamento(driver, dados, tipo)
    limpar_console()

    inicio = carregar_progresso(tipo)
    print(f"Preenchendo o Formulário {tipo} na linha {inicio + 1} de {len(dados)} registros:\n")
    print(dados.head())

    limpar_campos_texto(driver, tempo_espera=2)

    for linha in dados.index:
        if linha < inicio:
            continue  # Pula linhas já preenchidas

        try:
            # Extrai os dados da planilha
            login = dados.loc[linha, 'NOTEBOOK_LOGIN']
            marca = dados.loc[linha, 'NOTEBOOK_MARCA']
            modelo = dados.loc[linha, 'NOTEBOOK_MODELO']
            hostname = dados.loc[linha, 'NOTEBOOK_HOSTNAME']
            so = dados.loc[linha, 'NOTEBOOK_SO']
            num_serie = dados.loc[linha, 'NOTEBOOK_NUM_SERIE']
            patrimonio = dados.loc[linha, 'NOTEBOOK_PATRIMONIO']
            funciona = str(dados.loc[linha, 'NOTEBOOK_FUNCIONA']).strip().upper()
            time.sleep(1)
            limpar_console()
            print(f"**** Preenchendo linha {linha + 1}: Login={login}, Marca={marca}, Modelo={modelo} ****")
            time.sleep(2)
            # Preenche os campos de texto: login, hostname, so, num_serie, patrimonio
            preencher_campos_texto(driver, [login, hostname, so, num_serie, patrimonio])

            # Seleciona a MARCA no primeiro dropdown
            print(f"Selecionando marca: {marca}")
            try:
                dropdown_marca = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '(//div[@role="button" and @aria-haspopup="listbox"])[1]'))
                )
                dropdown_marca.click()
                time.sleep(1)
                
                # Busca e seleciona a marca
                opcoes_marca = WebDriverWait(driver, 5).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//div[@role="option"]'))
                )
                
                marca_encontrada = False
                for opcao in opcoes_marca:
                    texto_opcao = opcao.text.strip()
                    if texto_opcao.lower() == marca.strip().lower():
                        opcao.click()
                        print(f"✓ Marca selecionada: {texto_opcao}")
                        marca_encontrada = True
                        break
                
                if not marca_encontrada:
                    print(f"⚠ Marca '{marca}' não encontrada")
                    continue
                    
            except Exception as e:
                print(f"❌ Erro ao selecionar marca: {e}")
                continue
            
            # Aguarda um pouco para o segundo dropdown ficar disponível
            time.sleep(2)
            limpar_console()
            # Seleciona o MODELO no segundo dropdown
            print(f"Selecionando modelo: {modelo}")
            time.sleep(2)
            try:
                dropdown_modelo = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '(//div[@role="button" and @aria-haspopup="listbox"])[2]'))
                )
                dropdown_modelo.click()
                time.sleep(1)
                
                # Busca e seleciona o modelo
                opcoes_modelo = WebDriverWait(driver, 5).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//div[@role="option"]'))
                )
                
                modelo_encontrado = False
                for opcao in opcoes_modelo:
                    texto_opcao = opcao.text.strip()
                    if texto_opcao.lower() == modelo.strip().lower():
                        opcao.click()
                        print(f"✓ Modelo selecionado: {texto_opcao}")
                        modelo_encontrado = True
                        break
                
                if not modelo_encontrado:
                    print(f"⚠ Modelo '{modelo}' não encontrado")
                    continue
                    
            except Exception as e:
                print(f"❌ Erro ao selecionar modelo: {e}")
                continue

            time.sleep(1)

            # Seleciona o radio button para "Funciona" (SIM/NÃO)
            print(f"Selecionando funciona: {funciona}")
            try:
                clicar_radio_por_valor(driver, funciona)
                print(f"✓ Radio button selecionado: {funciona}")
            except Exception as e:
                print(f"❌ Erro ao selecionar radio button: {e}")

            time.sleep(1)

            # Aguarda o botão "Enviar" e clica
            botao_enviar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="form-main-content1"]/div/div/div[2]/div[3]/div/button[2]'))
            )
            
            # Para testes, comente a linha abaixo para não enviar
            # botao_enviar.click()
            print(f"✔ Formulário pronto para envio. Botão: {botao_enviar.text}")
            print(f"✔ Linha {linha + 1} processada com sucesso.")

            # Salva o progresso
            salvar_progresso(tipo, linha + 1)

            time.sleep(2)
            
            # Volta para o início do formulário para próximo preenchimento
            voltar_inicio(driver, dados)
            time.sleep(2)
            
            # Processa apenas UMA linha por chamada da função
            # O loop principal em main.py controlará as próximas chamadas
            break

        except Exception as e:
            print(f"❌ Erro na linha {linha + 1}: {e}")
            import traceback
            traceback.print_exc()
            continue
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
            #botao_enviar.click()
            print(botao_enviar.text)

            salvar_progresso(tipo, linha + 1)  # Salva o progresso após cada linha preenchida
            time.sleep(3)

            #usado para voltar para o inicio, fim de testes comente o  botao_enviar.click()
            voltar_inicio(driver,dados)    
            #time.sleep(3)   
            # link_enviar = WebDriverWait(driver, 10).until(
            #      EC.presence_of_element_located((By.XPATH, '//*[@id="form-main-content1"]/div/div/div[2]/div[1]/div[2]/div[5]/span'))
            #      )
            # ActionChains(driver).move_to_element(link_enviar).click().perform()
            # time.sleep(3)
            break

        except Exception as e:
            print(f"Erro ao acessar dados da linha {linha + 1}: {e}")
            # continue
   


def preencher_switch(driver, dados,tipo):
    preencher_do_inicio(driver, dados,tipo)
    preencher_unidade(driver, dados,tipo)
    preencher_equipamento(driver, dados, tipo)
    limpar_console()
    inicio = carregar_progresso(tipo)
    print(f"Preenchendo o Formulario {tipo} na linha...{inicio + 1} de {len(dados)} registros : ")
    #print(f"Preenchendo o Formulario {tipo}...")
    time.sleep(2)
    print(dados.head())

    for linha in dados.index:
        if linha < inicio:
            continue # pular linhas já preenchidas
        try:
            marca = dados.loc[linha, 'SWITCH_MARCA']
            modelo = dados.loc[linha, 'SWITCH_MODELO']
            num_serie = dados.loc[linha, 'SWITCH_NUM_SERIE']
            patrimonio = dados.loc[linha, 'SWITCH_PATRIMONIO']

            #espera e coleta todos os campos de texto da tela  
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@data-automation-id="textInput"]'))
            )  
            
            campos = driver.find_elements(By.XPATH, '//input[@data-automation-id="textInput"]')

            #limpa e preenche na ordem correta
            valores = [marca, modelo, num_serie, patrimonio]

            # for campo, valor in zip(campos, valores):
            #     campo.clear()
            #     campo.send_keys(str(valor))
            #     time.sleep(1)
            # botao_enviar = WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.XPATH, '//*[@id="form-main-content1"]/div/div/div[2]/div[3]/div/button[2]'))
            # )

            preencher_campos(driver,valores)

            botao_enviar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="form-main-content1"]/div/div/div[2]/div[3]/div/button[2]'))
            )
           
            #Envia o preenchimento do formulario  
            botao_enviar.click()
            print(botao_enviar.text)

            salvar_progresso(tipo, linha + 1)  # Salva o progresso após cada linha preenchida

            #usado para voltar para o inicio, fim de testes comente o  botao_enviar.click()
            # time.sleep(3)

            #para fins de testes, volta o form antes de enviar
            # voltar_inicio(driver,dados)    

            time.sleep(3)   
            link_enviar = WebDriverWait(driver, 10).until(
                 EC.presence_of_element_located((By.XPATH, '//*[@id="form-main-content1"]/div/div/div[2]/div[1]/div[2]/div[5]/span'))
                 )
            ActionChains(driver).move_to_element(link_enviar).click().perform()
            time.sleep(3)
            break

        except Exception as e:
            print(f"Erro ao acessar dados da linha {linha + 1}: {e}")
            # continue



def preencher_impressora(driver, dados, tipo):
    preencher_do_inicio(driver, dados,tipo)
    preencher_unidade(driver, dados,tipo)
    preencher_equipamento(driver, dados, tipo)
    limpar_console()
    inicio = carregar_progresso(tipo)
    print(f"Preenchendo o Formulario {tipo} na linha...{inicio + 1} de {len(dados)} registros : \n")
    #print(f"Preenchendo o Formulario {tipo}...")
    time.sleep(2)
    print(dados.head())
    #limpa os campos de texto antes de iniciar o preenchimento
    limpar_campos_texto(driver, tempo_espera=2)
    for linha in dados.index:
        if linha < inicio:
            continue # pular linhas já preenchidas
        try:
            origem = dados.loc[linha, 'IMPRESSORA_ORIGEM']
            mono_cor = dados.loc[linha, 'IMPRESSORA_MONO_COR']
            marca = dados.loc[linha, 'IMPRESSORA_MARCA']
            modelo = dados.loc[linha, 'IMPRESSORA_MODELO']
            ip_impressora = dados.loc[linha, 'IMPRESSORA_IP']
            hostname = dados.loc[linha, 'IMPRESSORA_HOSTNAME']
            patrimonio = dados.loc[linha, 'IMPRESSORA_PATRIMONIO']
            #espera e coleta todos os campos de texto da tela  
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@data-automation-id="textInput"]'))
            )  
            
            campos = driver.find_elements(By.XPATH, '//input[@data-automation-id="textInput"]')

            #limpa e preenche na ordem correta
            valores = [origem, mono_cor, marca, modelo, ip_impressora, hostname, patrimonio]

            # for campo, valor in zip(campos, valores):
            #     campo.clear()
            #     campo.send_keys(str(valor))
            #     time.sleep(1)
            # botao_enviar = WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.XPATH, '//*[@id="form-main-content1"]/div/div/div[2]/div[3]/div/button[2]'))
            # )
            
            preencher_campos(driver,valores)

            botao_enviar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="form-main-content1"]/div/div/div[2]/div[3]/div/button[2]'))
            )
           
            #Envia o preenchimento do formulario  
            botao_enviar.click()
            print(botao_enviar.text)

            salvar_progresso(tipo, linha + 1)  # Salva o progresso após cada linha preenchida
            #para fins de testes, volta o form antes de enviar
            # voltar_inicio(driver,dados)    

            time.sleep(3)   
            link_enviar = WebDriverWait(driver, 10).until(
                 EC.presence_of_element_located((By.XPATH, '//*[@id="form-main-content1"]/div/div/div[2]/div[1]/div[2]/div[5]/span'))
                 )
            ActionChains(driver).move_to_element(link_enviar).click().perform()
            time.sleep(3)
            break
        except Exception as e:
            print(f"Erro ao acessar dados da linha {linha + 1}: {e}")
            # continue

   


    
