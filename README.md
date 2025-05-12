# 🧾 Automação de Preenchimento de Formulários com Selenium

Este projeto automatiza o preenchimento de formulários no Microsoft Forms utilizando o Selenium WebDriver, com base em dados de uma planilha Excel contendo o inventário de equipamentos.

## 📁 Estrutura do Projeto

```
projeto/
├── main.py
├── preenche.py
├── utils.py
├── .env
├── Levantamento.xlsx  ← agora atualizado e corrigido
├── requirements.txt
├── .gitignore
├── README.md
```

## ⚙️ Pré-requisitos

- Python 3.8+
- Google Chrome instalado
- ChromeDriver compatível (instalado automaticamente)
- Conta Microsoft válida (se necessário login)
- Ambiente virtual (recomendado)

## 📦 Instalação

1. Clone o repositório:

```bash

git clone https://github.com/mayconwiner/formulario-automacao.git
cd formulario-automacao

git remote add origin https://github.com/mayconwiner/formulario-automacao.git
git branch -M main
git push -u origin main
```

2. Crie um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate   # Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

## 🔐 Configuração do `.env`

Crie um arquivo `.env` com as seguintes variáveis:

```env
FORM_URL=https://forms.office.com/pages/responsepage.aspx?id=SEU_FORMULARIO
CHROME_USER_DATA=C:\Users\seu.usuario\AppData\Local\Google\Chrome\User Data\Profile Selenium
HEPTA_USER=seu.email@dominio.com
HEPTA_PASS=sua_senha_segura
```

## 📊 Prepare sua planilha

- Nome: `Levantamento.xlsx`
- Abas esperadas: `AcessPoint`, `Desktop`, `Monitor`, `Notebook`, `Scanner`, `Servidor`, `Switch`, `Impressora`
- Todas as abas agora padronizadas com as colunas obrigatórias `UNIDADE` e `SALA`

## ▶️ Execução

Com o ambiente ativado, rode:

```bash
python main.py
```

Siga as instruções no terminal para escolher o tipo de equipamento e aguarde o preenchimento automático no navegador.

## 👨‍🔧 Suporte e Manutenção

- Código modular e de fácil extensão.
- Para adicionar campos específicos por tipo de equipamento, edite o arquivo `preenche.py`.

## 🛡️ Segurança

- Nunca compartilhe seu `.env` publicamente.
- Utilize variáveis de ambiente para armazenar credenciais com segurança.
