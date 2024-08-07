# Analisador de Cotações

Este projeto Python automatiza a coleta e análise de dados de cotações de ações, enviando um relatório por e-mail.

## Descrição

Este script permite:

- Coleta de dados: Obtém dados históricos de cotações de ações usando a biblioteca yfinance.
- Cálculo de métricas: Calcula a cotação máxima, mínima e média do período especificado.
- Envio de relatório: Envia um e-mail formatado com as métricas calculadas, utilizando o Gmail como servidor SMTP.

## Funcionalidades

- Coleta dados de cotações de ações do Yahoo Finance.
- Calcula cotação máxima, mínima e média.
- Envia relatório por e-mail com os resultados.
- Personalização do período de análise.

## Tecnologias Utilizadas

- Python: Linguagem de programação principal.
- yfinance: Biblioteca para coleta de dados financeiros.
- smtplib: Biblioteca para envio de e-mails.
- dotenv: Biblioteca para gerenciar variáveis de ambiente.

## Instalação e Uso

1. Clone o repositório:

    ```bash
    git clone https://github.com/bysedd/StockAnalyzer.git
    ```

2. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

3. Configure as variáveis de ambiente:

   - Crie um arquivo .env na raiz do projeto.
   - Copie as variáveis do arquivo .env-example para o arquivo `.env`.
   - Altere os valores das variáveis conforme as suas credenciais.

4. Execute o script:

    ```bash
    python main.py
    ```

   - Siga as instruções para inserir o código da ação e o período de análise.

**Observações:**

- Certifique-se de ter as credenciais do Gmail configuradas corretamente no arquivo `.env`.
- Para usar outros provedores de e-mail, ajuste a configuração do servidor SMTP em `send_email()`.