import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict

from yfinance import Ticker


def validate_ticker(ticker: str) -> bool:
    """
    Função para verificar se o código da ação é válido

    :param ticker: Código da ação
    :return: True se o código é válido, False caso contrário
    """
    if not ticker:
        raise ValueError("Código da ação não informado")

    try:
        data = Ticker(ticker)
        if not data.calendar:
            raise ValueError("Dados da ação não encontrados")
        return True
    except ValueError as e:
        print(f"Erro ao validar o código da ação: {e}")
        return False


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


def send_email(login: tuple[str, str], subject: str, message: str, *, to: str) -> bool:
    """
    Função para enviar email usando o Gmail como servidor SMTP

    :param login: Tupla contendo email e senha
    :param subject: Assunto, título do email
    :param message: Mensagem, corpo do email
    :param to: Destinatário do email
    :return: True se o email foi enviado com sucesso, False caso contrário
    """
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        my_email, password = login

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
