import os
from datetime import datetime

from dotenv import load_dotenv

import util


def main() -> None:
    # Carregar variáveis de ambiente e definir credenciais
    load_dotenv()
    my_email = os.environ["MY_EMAIL"]
    password = os.environ["PASSWORD"]
    name = os.environ["NAME"]
    login = (my_email, password)

    if not all(login):
        print("Email or password not found in environment variables!")
        exit(1)

    ticker = input("Digite o código da ação desejada: ")  # example: BBAS3.SA
    if not util.validate_ticker(ticker):
        exit(1)

    start = input("Digite a data de início (yyyy-mm-dd): ")
    end = input("Digite a data de fim (yyyy-mm-dd): ")
    try:
        datetime.strptime(start, "%Y-%m-%d")
        datetime.strptime(end, "%Y-%m-%d")
    except ValueError:
        print("Formato de data inválido. Use (yyyy-mm-dd)")
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
