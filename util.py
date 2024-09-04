import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import yfinance as yf  # type: ignore


def validate_ticker(ticker: str) -> bool:
    """
    Validates the given ticker symbol.

    Args:
        ticker (str): The ticker symbol to be validated.

    Returns:
        bool: True if the ticker symbol is valid, False otherwise.

    Raises:
        ValueError: If the ticker symbol is not provided or \
        if the data for the ticker symbol is not found.
    """
    if not ticker:
        raise ValueError("Código da ação não informado")

    try:
        data = yf.Ticker(ticker)
        if not data.calendar:
            raise ValueError("Dados da ação não encontrados")
        return True
    except ValueError as e:
        print(f"Erro ao validar o código da ação: {e}")
        return False


def validate_login(login: tuple[str, str]) -> bool:
    """
    Validates the login credentials.

    Args:
        login (tuple[str, str]): A tuple containing the email and password.

    Returns:
        bool: True if the login credentials are valid, False otherwise.
    """
    if not all(login):
        print("Email or password not found in environment variables!")
        return False
    return True


def validate_interval(start: str, end: str, datetime_format: str) -> bool:
    """
    Validates the interval between two dates.

    Args:
        start (str): The start date of the interval.
        end (str): The end date of the interval.
        datetime_format (str): The format of the dates.

    Returns:
        bool: True if the interval is valid, False otherwise.
    """
    try:
        datetime.strptime(start, datetime_format)
        datetime.strptime(end, datetime_format)
        return True
    except ValueError:
        print("Formato de data inválido. Use (yyyy-mm-dd)")
        return False


def collect_data(ticker: str, start: str, end: str) -> dict[str, float]:
    """
    Collects stock data for a given ticker symbol within a specified date range.

    Args:
        ticker (str): The ticker symbol of the stock.
        start (str): The start date of the data collection period.
        end (str): The end date of the data collection period.

    Returns:
        dict[str, float]: A dictionary containing the maximum, minimum, and average
        closing prices of the stock within the specified date range.

    Raises:
        ValueError: If no closing data is found for the specified stock and date range.
    """
    try:
        df = yf.Ticker(ticker).history(start=start, end=end)
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
    Sends an email using the provided login credentials.

    Args:
        login (tuple[str, str]): A tuple containing the email address \
            and password for authentication.
        subject (str): The subject of the email.
        message (str): The content of the email.
        to (str): The recipient's email address.

    Returns:
        bool: True if the email was sent successfully, False otherwise.
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
