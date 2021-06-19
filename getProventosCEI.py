#!/usr/bin/python3.8
import asyncio
import logging
import mysql.connector
from datetime import datetime
from mysql.connector import Error
from bolsaprov import B3AsyncBackend
import base64
import sys

# dados da b3
b3User = 'seu CPF'
b3Pwd = 'sua senha' # senha da b3

logging.basicConfig(
    format=(
        '%(asctime)s.%(msecs)03d %(levelname)s {%(module)s} [%(funcName)s] '
        '%(message)s'
    ),
    datefmt='%Y-%m-%d,%H:%M:%S',
    level=logging.DEBUG
)


async def main():

    start_datetime = datetime.now()
    logging.info(f'Starting... {start_datetime}')
    b3_httpclient = B3AsyncBackend(
        username=b3User,
        password=b3Pwd,
        captcha_service=None  # captcha_service is not required yet
    )
    brokers = await b3_httpclient.get_brokers_with_accounts()
    assets_extract = (
        await b3_httpclient.get_brokers_account_portfolio_assets_extract(
            brokers=brokers
        )
    )

    try:
        for dados in assets_extract:
            for d in dados:
                # raw_negotiation_name, asset_specification, raw_negotiation_code, operation_date, event_type, unit_amount, quotation_factor, bruto_price, liquido_price
                raw_negotiation_name = vars(d)['raw_negotiation_name'] # nome do ativo
                asset_specification = vars(d)['asset_specification'] # especificacao: CI, ON ou REC
                raw_negotiation_code = vars(d)['raw_negotiation_code'] # TICKER do ativo
                operation_date = vars(d)['operation_date'] # data da operacao
                event_type = vars(d)['event_type'] # evento: RENDIMENTO, JUROS...
                unit_amount = vars(d)['unit_amount'] # quantidade
                quotation_factor = vars(d)['quotation_factor'] # fator...
                bruto_price = vars(d)['bruto_price'] # valor bruto
                liquido_price = vars(d)['liquido_price'] # valor liquido
                
                print(raw_negotiation_name, asset_specification, raw_negotiation_code, operation_date, event_type, unit_amount, quotation_factor, bruto_price, liquido_price)
                
    except Exception as e: 
        print(e)

    await b3_httpclient.session_close()
    await b3_httpclient.connection_close()

    logging.info(f'Finish script... {datetime.now() - start_datetime}')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


