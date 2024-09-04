import os

from dotenv import load_dotenv

import util


def main() -> None:
    load_dotenv()
    my_email = os.environ["MY_EMAIL"]
    password = os.environ["PASSWORD"]
    name = os.environ["NAME"]

    login = (my_email, password)
    if not util.validate_login((my_email, password)):
        exit(1)

    ticker = input("Digite o código da ação desejada: ")  # example: BBAS3.SA
    if not util.validate_ticker(ticker):
        exit(1)

    start = input("Digite a data de início (yyyy-mm-dd): ")
    end = input("Digite a data de fim (yyyy-mm-dd): ")
    datetime_format = "%Y-%m-%d"
    if not util.validate_interval(start, end, datetime_format):
        exit(1)

    closure = util.collect_data(ticker, start, end)
    subject = "Relatório de Análise Financeira"
    message = f"""
    Prezado,

    Segue abaixo um resumo das informações coletadas referentes ao ticker {ticker}:

    - Cotação Máxima: R$ {closure["max"]}
    - Cotação Mínima: R$ {closure["min"]}
    - Valor Médio: R$ {closure["medium"]}

    Agradeço a sua atenção.

    Atenciosamente,
    {name}
    """
    if util.send_email(login, subject, message, to=my_email):
        print("E-mail enviado com sucesso!")


if __name__ == "__main__":
    main()
