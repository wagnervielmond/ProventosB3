import logging
from bs4 import BeautifulSoup

from bolsaprov.models import (
    Broker,
    BrokerAccount,
    BrokerAccountParseExtraData,
    BrokerAssetExtract,
    BrokerParseExtraData
)

logger = logging.getLogger(__name__)


class GetBrokersResponse():
    BROKERS_SELECT_ID = 'ctl00_ContentPlaceHolder1_ddlAgentes'
    DEFAULT_INVALID_BROKER_VALUE = '-1'

    def __init__(self, response):
        self.response = response

    async def data(self):
        html = await self.response.text()
        return self._parse_get_brokers(html)

    def _parse_get_brokers(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        brokers_select = soup.find('select', id=self.BROKERS_SELECT_ID)
        # logging.warning(brokers_select)
        # if not brokers_select:
        #     return []
        brokers_option = brokers_select.find_all('option')

        data = soup.find(
            id='ctl00_ContentPlaceHolder1_txtData'
        )['value']

        return [
            Broker(
                name=broker_option.text,
                value=broker_option['value'],
                parse_extra_data=BrokerParseExtraData(data)
            )
            for broker_option in brokers_option
            if broker_option['value'] != self.DEFAULT_INVALID_BROKER_VALUE
        ]


class GetBrokerAccountResponse():
    ACCOUNT_SELECT_ID = 'ctl00_ContentPlaceHolder1_ddlContas'
    BROKERS_SELECT_ID = 'ctl00_ContentPlaceHolder1_ddlAgentes'

    def __init__(self, response, broker):
        self.response = response
        self.broker = broker

    async def data(self):
        html = await self.response.text()

        self.broker.accounts = self._parse_get_accounts(html)

        return self.broker

    def _parse_get_accounts(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        brokers_select = soup.find('select', id=self.ACCOUNT_SELECT_ID)
        if not brokers_select:
            return []

        brokers_option = brokers_select.find_all('option')

        view_state = soup.find(id='__VIEWSTATE')['value']
        view_state_generator = soup.find(id='__VIEWSTATEGENERATOR')['value']
        event_validation = soup.find(id='__EVENTVALIDATION')['value']

        parse_extra_data = BrokerAccountParseExtraData(
            view_state=view_state,
            view_state_generator=view_state_generator,
            event_validation=event_validation,
        )

        return [
            BrokerAccount(
                id=broker_option['value'],
                parse_extra_data=parse_extra_data
            )
            for broker_option in brokers_option
        ]


class GetBrokerAccountResponse():
    ACCOUNT_SELECT_ID = 'ctl00_ContentPlaceHolder1_ddlContas'
    BROKERS_SELECT_ID = 'ctl00_ContentPlaceHolder1_ddlAgentes'

    def __init__(self, response, broker):
        self.response = response
        self.broker = broker

    async def data(self):
        html = await self.response.text()

        self.broker.accounts = self._parse_get_accounts(html)

        return self.broker

    def _parse_get_accounts(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        brokers_select = soup.find('select', id=self.ACCOUNT_SELECT_ID)
        if not brokers_select:
            return []

        brokers_option = brokers_select.find_all('option')

        view_state = soup.find(id='__VIEWSTATE')['value']
        view_state_generator = soup.find(id='__VIEWSTATEGENERATOR')['value']
        event_validation = soup.find(id='__EVENTVALIDATION')['value']

        parse_extra_data = BrokerAccountParseExtraData(
            view_state=view_state,
            view_state_generator=view_state_generator,
            event_validation=event_validation,
        )

        return [
            BrokerAccount(
                id=broker_option['value'],
                parse_extra_data=parse_extra_data
            )
            for broker_option in brokers_option
        ]


# ctl00_ContentPlaceHolder1_rptAgenteProventos_ctl00_rptContasProventos_ctl00_lblConta
# ctl00_ContentPlaceHolder1_rptAgenteProventos_ctl00_lblAgenteProventos
class GetBrokerAccountAssetExtractResponse:
    ASSETS_TABLE_ID = (
        'ctl00_ContentPlaceHolder1_updFiltro'
    )

    def __init__(self, response, broker_value):
        self.response = response
        self.broker_value = broker_value

    async def data(self):
        html = await self.response.text()

        assets_extract = await self._parse_get_assets_extract(html)
        return assets_extract

    async def _parse_get_assets_extract(self, html):
        assets_extract = []
        soup = BeautifulSoup(html, 'html.parser')
        assets_table = soup.find(id=self.ASSETS_TABLE_ID)

        logger.debug(
            f'GetBrokerAccountAssetExtractResponse start parsing asset extract'
            f' - broker value: {self.broker_value}'
        )

        if not assets_table:
            return assets_extract

        tables_body = assets_table.find_all('tbody') # Pega os tbody da pagina 
        
        # faz um loop enquanto existir tbody 
        for index, item in enumerate(tables_body):
            # procura os tr de cada tabela
            rows = item.find_all('tr')
            # lista todos os TR das tabelas
            for row in rows:
                raw_negotiation_name, asset_specification, raw_negotiation_code, operation_date, event_type, unit_amount, quotation_factor, bruto_price, liquido_price = row.find_all(  # NOQA
                    'td'
                )
                # insere em cada coluna um nome para que possa ser possivel pegar os dados
                asset_extract = BrokerAssetExtract.create_from_response_fields(
                    raw_negotiation_name=raw_negotiation_name.get_text(strip=True),
                    asset_specification=asset_specification.get_text(strip=True),
                    raw_negotiation_code=raw_negotiation_code.get_text(strip=True),
                    operation_date=operation_date.get_text(strip=True),
                    event_type=event_type.get_text(strip=True),
                    unit_amount=unit_amount.get_text(strip=True),
                    quotation_factor=quotation_factor.get_text(strip=True),
                    bruto_price=bruto_price.get_text(strip=True),
                    liquido_price=liquido_price.get_text(strip=True)
                )
                assets_extract.append(asset_extract)

            # a pagina dos proventos contem mais de uma tabela, a ultima tabela contem mais colunas. Esse break pega apenas a tabela 1 (provisoes) e a tabela 2 (creditados)
            if index == 1:
                break

        logger.debug(
            f'GetBrokerAccountAssetExtractResponse end parsing asset extract '
            f'- broker value: {self.broker_value}'
        )

        return assets_extract
