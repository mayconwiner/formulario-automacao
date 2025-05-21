import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from utils import setup_driver, realizar_login, escolher_planilha, limpar_console, verificar_variaveis_ambiente,limpar_progresso,carregar_progresso
from selenium.webdriver.common.by import By
from preenche import preencher_acess_point, preencher_desktop, preencher_monitor, preencher_notebook, preencher_scanner, preencher_servidor, preencher_switch, preencher_impressora,preencher_unidade,preencher_equipamento,verificador_progresso,limpar_campos_texto,voltar_inicio
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

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
# 
    planilha, dados = escolher_planilha("Levantamento.xlsx", abas)
    #chama a função para retornar o inicio do form
    voltar_inicio(navegador,dados)
    if planilha == "Access Point":
        preencher_acess_point(navegador, dados,planilha)
        
    elif planilha == "Desktop":
        preencher_desktop(navegador, dados)

    elif planilha == "Monitor":
        preencher_monitor(navegador, dados)
    elif planilha == "Notebook":
        preencher_notebook(navegador, dados)
    elif planilha == "Scanner":
        preencher_scanner(navegador, dados)

    #chama a função Servidor
    elif planilha == "Servidor":
        #verifica se inicia com algum botão de voltar o que significa que não esta no inicio
        if voltar_inicio(navegador,dados):
            #limpa os campos de texto
            try:
                    
                limpar_campos_texto(navegador)
                #limpa os campos de texto
                limpar_campos_texto(navegador)
            except Exception as e:
                pass
        # preencher_servidor(navegador, dados,planilha)
        if verificador_progresso(navegador,dados,'Servidor',preencher_servidor):
            preencher_servidor(navegador, dados,planilha)
        print("Dados inseridos com sucesso em: ",planilha)
        time.sleep(8)
        progresso = carregar_progresso('Servidor')
        #loop para verificar se existe mais informações para adicionar e chama a função
        while verificador_progresso(navegador,dados,'Servidor',preencher_servidor):
            limpar_console()
            print(f"Analisando proximos registros ..... percorrendo a base de dados de  {planilha} : {len(dados)} registros encontrados")
            print("*************************************************")
            print(f'****** Progresso: {progresso} de {len(dados)} ****** ')
            print("*************************************************")

            time.sleep(8)
            limpar_console()
            # Preencher o servidor novamente
            preencher_servidor(navegador, dados,planilha)
            print("Preencheu o servidor novamente")
            if verificador_progresso(navegador,dados,'Servidor',preencher_servidor) == False:
                print("Quantidade de registros preenchidos: ",progresso)
                break


    elif planilha == "Switch":
        preencher_switch(navegador, dados)
    elif planilha == "Impressora":
        preencher_impressora(navegador, dados)
    

    print("Processo finalizado.")

if __name__ == "__main__":
    main()

