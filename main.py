import os
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict

from dotenv import load_dotenv
from yfinance import Ticker

# Carregar variáveis de ambiente e definir credenciais
load_dotenv()
my_email = os.environ["MY_EMAIL"]
password = os.environ["PASSWORD"]

if not my_email or not password:
    print("Email or password not found in environment variables!")
    exit(1)


def collect_data(ticker: str, start: str, end: str) -> Dict[str, float]:
    """
    Função para coletar dados de fechamento de uma ação

    :param ticker: Código da ação
    :param start: Período de início
    :param end: Período de fim
    :return: Dicionário com os valores de fechamento
    """
    try:
        df = Ticker(ticker).history(start=start, end=end)
        close = df["Close"]
        if close.empty:
            raise ValueError("Dados de fechamento não encontrados")
        return {
            "max": round(close.max(), 2),
            "min": round(close.min(), 2),
            "medium": round(close.mean(), 2),
        }
    except Exception as e:
        print(f"Ocorreu um erro ao coletar os dados: {e}")
        return {}


ticker = input("Digite o código da ação desejada: ")  # example: BBAS3.SA
start = input("Digite a data de início (yyyy-mm-dd): ")
end = input("Digite a data de fim (yyyy-mm-dd): ")

try:
    datetime.strptime(start, "%Y-%m-%d")
    datetime.strptime(end, "%Y-%m-%d")
except ValueError:
    print("Formato de data inválido. Use (yyyy-mm-dd)")
    exit(1)

closure = collect_data(ticker, start, end)


def send_email(subject: str, message: str, to: str) -> bool:
    """
    Função para enviar email usando o Gmail como servidor SMTP

    :param subject: Assunto, título do email
    :param message: Mensagem, corpo do email
    :param to: Destinatário do email
    :return: True se o email foi enviado com sucesso, False caso contrário
    """
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(my_email, password)

        msg = MIMEMultipart()
        msg["From"] = my_email
        msg["To"] = to
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        server.sendmail(my_email, to, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return False


subject = "Relatório de Análise Financeira"
message = f"""
Prezado,

Segue abaixo um resumo das informações coletadas referentes ao ticker {ticker}:

- Cotação Máxima: R$ {closure["max"]}
- Cotação Mínima: R$ {closure["min"]}
- Valor Médio: R$ {closure["medium"]}

Agradeço a sua atenção.

Atenciosamente,
[Seu Nome]
"""

if send_email(subject, message, my_email):
    print("E-mail enviado com sucesso!")
