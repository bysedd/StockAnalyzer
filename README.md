# Analisador de Cotações de Ações com Envio de Email

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