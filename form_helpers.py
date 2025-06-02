
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def preencher_campos_texto(driver, valores, tempo_espera=5):
    """
    Preenche automaticamente os campos de texto visíveis no formulário.

    Parâmetros:
    - driver: instância do WebDriver.
    - valores: lista de valores a serem preenchidos, na ordem dos campos.
    - tempo_espera: tempo de espera máximo em segundos para localização dos campos.
    """
    WebDriverWait(driver, tempo_espera).until(
        EC.presence_of_all_elements_located((By.XPATH, '//input[@data-automation-id="textInput"]'))
    )
    campos = driver.find_elements(By.XPATH, '//input[@data-automation-id="textInput"]')

    if len(campos) < len(valores):
        raise Exception(f"Número de campos encontrados ({len(campos)}) é menor que o número de valores fornecidos ({len(valores)}).")

    for campo, valor in zip(campos, valores):
        campo.clear()
        campo.send_keys(str(valor).strip())
        time.sleep(0.5)  # Simula preenchimento humano


def selecionar_dropdown_por_texto(driver, texto_desejado, tempo_espera=5):
    """
    Seleciona uma opção de um campo dropdown com base no texto visível.

    Parâmetros:
    - driver: instância do WebDriver.
    - texto_desejado: texto da opção a ser selecionada.
    - tempo_espera: tempo máximo de espera para localizar os elementos.

    Retorna:
    - True se selecionado com sucesso, False caso contrário.
    """
    try:
        dropdown = WebDriverWait(driver, tempo_espera).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@role="button" and @aria-haspopup="listbox"]'))
        )
        dropdown.click()

        opcoes = WebDriverWait(driver, tempo_espera).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@role="option"]'))
        )
        for opcao in opcoes:
            texto = opcao.text.strip()
            if texto.lower() == texto_desejado.strip().lower():
                opcao.click()
                print(f"✓ Dropdown selecionado: {texto}")
                return True

        print(f"⚠ Opção '{texto_desejado}' não encontrada no dropdown.")
        return False

    except Exception as e:
        print(f"Erro ao selecionar dropdown: {e}")
        return False


def clicar_radio_por_valor(driver, valor_desejado, tempo_espera=5):
    """
    Seleciona uma opção de botão rádio com base no valor atribuído (ex: 'SIM', 'NÃO').

    Parâmetros:
    - driver: instância do WebDriver.
    - valor_desejado: texto do valor a ser comparado com o atributo 'value' dos botões.
    - tempo_espera: tempo máximo de espera para garantir o carregamento.

    Retorna:
    - True se clicado com sucesso, False caso contrário.
    """
    valor_desejado = str(valor_desejado).strip().upper()

    WebDriverWait(driver, tempo_espera).until(
        EC.presence_of_all_elements_located((By.XPATH, '//input[@type="radio"]'))
    )
    radios = driver.find_elements(By.XPATH, '//input[@type="radio"]')

    for radio in radios:
        valor_radio = radio.get_attribute("value").strip().upper()
        if valor_radio == valor_desejado:
            driver.execute_script("arguments[0].click();", radio)
            print(f"✓ Botão rádio selecionado: {valor_radio}")
            return True

    print(f"⚠ Valor '{valor_desejado}' não encontrado entre os botões rádio.")
    return False
