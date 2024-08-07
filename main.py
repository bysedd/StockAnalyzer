import os
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from textwrap import dedent
from typing import Dict

from yfinance import Ticker
from dotenv import load_dotenv

# Carregar variáveis de ambiente e definir credenciais
load_dotenv()
my_email = os.environ["MY_EMAIL"]
password = os.environ["PASSWORD"]


def collect_data(ticker: str, start: str, end: str) -> Dict[str, float]:
    """
    Função para coletar dados de fechamento de uma ação

    :param ticker: Código da ação
    :param start: Período de início
    :param end: Período de fim
    :return: Dicionário com os valores de fechamento
    """
    df = Ticker(ticker=ticker).history(start=start, end=end)
    close = df["Close"]

    closure = {
        "max": round(close.max(), 2),
        "min": round(close.min(), 2),
        "medium": round(close.mean(), 2),
    }

    return closure


ticker = input("Digite o código da ação desejada: ")  # example: BBAS3.SA
start = input("Digite a data de início (yyyy-mm-dd): ")
end = input("Digite a data de fim (yyyy-mm-dd): ")

closure = collect_data(ticker, start, end)


def send_email(subject: str, message: str, to: str) -> None:
    """
    Função para enviar email usando o Gmail como servidor SMTP

    :param subject: Assunto, título do email
    :param message: Mensagem, corpo do email
    :param to: Destinatário do email
    """
    global my_email, password

    server = smtplib.SMTP("smtp.gmail.com", port=587)
    server.starttls()
    server.login(my_email, password)

    msg = MIMEMultipart()
    msg["From"] = my_email
    msg["To"] = to
    msg["Subject"] = Header(subject, "utf-8")

    msg.attach(MIMEText(message, "plain", "utf-8"))

    server.sendmail(
        from_addr=my_email,
        to_addrs=to,
        msg=dedent(msg.as_string())
    )

    server.quit()


try:
    subject = "Análises do Projeto 2020"
    message = f"""
    Prezado gestor,
    
    Seguem as análises solicitadas da ação {ticker}
    
    Cotação máxima: R${closure["max"]}
    Cotação mínima: R${closure["min"]}
    Valor médio: R${closure["medium"]}
    
    Qualquer dúvida estou a disposição!
    
    Atte.
    """
    send_email(subject, message, to=my_email)
    print("Email enviado com sucesso!")
except Exception as e:
    print(f"Erro ao enviar email: {e}")
