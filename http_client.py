import logging

from bs4 import BeautifulSoup

from bolsaprov.bolsa.connector import B3HttpClientConnector

logger = logging.getLogger(__name__)

POOL_CONNECTOR = B3HttpClientConnector()


class B3HttpClient():
    IS_LOGGED = False
    SESSION = None
    LOGIN_URL = 'https://ceiapp.b3.com.br/CEI_Responsivo/login.aspx'

    ASSETS_HOME_URL = (
        'https://cei.b3.com.br/CEI_Responsivo/ConsultarProventos.aspx'
    )
    BROKERS_ACCOUNT_URL = (
        'https://cei.b3.com.br/CEI_Responsivo/ConsultarProventos.aspx'
    )
    ASSETS_URL = (
        'https://cei.b3.com.br/CEI_Responsivo/ConsultarProventos.aspx'
    )

    def __init__(self, username, password, session, captcha_service):
        self.username = username
        self.password = password
        self.session = session
        self.captcha_service = captcha_service

    async def login(self):
        async with self.session.get(
            self.LOGIN_URL
        ) as response:
            loginPageContent = await response.text()
            loginPageParsed = BeautifulSoup(loginPageContent, "html.parser")
            view_state = loginPageParsed.find(id='__VIEWSTATE')['value']
            viewstate_generator = loginPageParsed.find(
                id='__VIEWSTATEGENERATOR'
            )['value']
            event_validation = loginPageParsed.find(
                id='__EVENTVALIDATION'
            )['value']

            solvedcaptcha = None
            if self.captcha_service:
                site_key = loginPageParsed.find(
                    id='ctl00_ContentPlaceHolder1_dvCaptcha'
                ).get(
                    'data-sitekey'
                )
                solvedcaptcha = await self.captcha_service.resolve(
                    site_key,
                    self.LOGIN_URL
                )

        payload = {
            'ctl00$ContentPlaceHolder1$smLoad': (
                'ctl00$ContentPlaceHolder1$UpdatePanel1|ctl00$ContentPlaceHold'
                'er1$btnLogar'
            ),
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATEGENERATOR': viewstate_generator,
            '__EVENTVALIDATION': event_validation,
            '__VIEWSTATE': view_state,
            'ctl00$ContentPlaceHolder1$txtLogin': self.username,
            'ctl00$ContentPlaceHolder1$txtSenha': self.password,
            '__ASYNCPOST': True,
            'g-recaptcha-response': solvedcaptcha,
            'ctl00$ContentPlaceHolder1$btnLogar': 'Entrar'
        }

        headers = {
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'https://cei.b3.com.br/CEI_Responsivo/login.aspx',
            'Origin': 'https://cei.b3.com.br',
            'Host': 'cei.b3.com.br',
            'User-Agent': (
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) '
                'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 '
                'Safari/537.36'
            ),
        }

        logger.info(f'B3HttpClient doing login - username: {self.username}')

        async with self.session.post(
            self.LOGIN_URL,
            data=payload,
            headers=headers,
        ) as response:
            logger.info(f'B3HttpClient login done - username: {self.username}')

            self.IS_LOGGED = True

            return await response.text()

    async def get_brokers(self):
        if not self.IS_LOGGED:
            await self.login()

        logger.info(
            f'B3HttpClient getting brokers - username: {self.username}'
        )

        response = await self.session.get(self.ASSETS_HOME_URL)
        logger.info(
            f'B3HttpClient end getting brokers - username: {self.username}'
        )

        return response

    async def get_broker_accounts(self, broker):
        if not self.IS_LOGGED:
            await self.login()

        default_account = '0'
        data = broker.parse_extra_data.data

        payload = {
            'ctl00$ContentPlaceHolder1$ToolkitScriptManager1': (
                'ctl00$ContentPlaceHolder1$updFiltro|ctl00$ContentPlaceHolder1'
                '$ddlAgentes'
            ),
            '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$ddlAgentes',
            '__VIEWSTATE': (
                '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'
            ),
            '__VIEWSTATEGENERATOR': '60D025E9',
            '__EVENTVALIDATION': (
                '/wEdAAz3Yx2ES4cT5dCIgXUVBTgKSNYuFsig2msCC841hKS1H1GNyhN3N1osqBqqgaNItpdZDO+9C9gz5Aw/AZYSIzXhfk+HLxCXHRClRDm0/iVBUojipT0jOBb54glnPZxI9VIJZJh1VhVVa0UQ15FhckhgY2JNro3bvLeSMJrpn9aSiHkRxwuEE8o8LwrE2E6mACtDmhxe4pZ6Ibt8oBWfF3Ts7H30DjvuZHqRE05bVtqWSPOOFWTf/Hn+MVE/ujXYFJTWLVokCvgbtFxjrfYgYXuQJX3w9w=='
            ),
            'ctl00$ContentPlaceHolder1$ddlAgentes': broker.value,
            'ctl00$ContentPlaceHolder1$ddlContas': default_account,
            'ctl00$ContentPlaceHolder1$txtData': data,
            '__ASYNCPOST': True
        }
        headers = {
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': (
                'https://cei.b3.com.br/CEI_Responsivo/ConsultarProventos.asp'
                'x'
            ),
            'Origin': 'https://cei.b3.com.br',
            'User-Agent': (
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) '
                'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 '
                'Safari/537.36')}

        logger.info(
            f'B3HttpClient getting brokers account - username: {self.username}'
            f' broker_value: {broker.value}'
        )

        response = await self.session.post(
            self.BROKERS_ACCOUNT_URL,
            data=payload,
            headers=headers
        )

        logger.info(
            f'B3HttpClient end getting brokers account - '
            f'username: {self.username} broker_value: {broker.value}'
        )

        return response

    async def get_broker_account_portfolio_assets_extract(
        self,
        account_id,
        broker_value,
        broker_parse_extra_data,
        account_parse_extra_data
    ):
        if not self.IS_LOGGED:
            await self.login()

        data = broker_parse_extra_data.data

        payload = {
            'ctl00$ContentPlaceHolder1$ToolkitScriptManager1': (
                'ctl00$ContentPlaceHolder1$updFiltro|ctl00$ContentPlaceHolder1'
                '$btnConsultar'
            ),
            '__EVENTTARGET': '',
            '__VIEWSTATE': account_parse_extra_data.view_state,
            '__VIEWSTATEGENERATOR': (
                account_parse_extra_data.view_state_generator
            ),
            '__EVENTVALIDATION': account_parse_extra_data.event_validation,
            'ctl00$ContentPlaceHolder1$ddlAgentes': broker_value,
            'ctl00$ContentPlaceHolder1$ddlContas': account_id,
            'ctl00$ContentPlaceHolder1$txtData': data,
            'ctl00$ContentPlaceHolder1$btnConsultar': 'Consultar',
            '__ASYNCPOST': True}

        headers = {
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': (
                'https://cei.b3.com.br/CEI_Responsivo/ConsultarProventos.as'
                'px'
            ),
            'Origin': 'https://cei.b3.com.br',
            'User-Agent': (
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) '
                'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 '
                'Safari/537.36')}

        logger.info(
            f'B3HttpClient getting broker account extract proventos - '
            f'username: {self.username} '
            f'broker_value: {broker_value} '
            f'account_id: {account_id}'
        )

        response = await self.session.post(
            self.ASSETS_URL,
            data=payload,
            headers=headers
        )
        logger.info(
            f'B3HttpClient end getting broker account extract proventos - '
            f'username: {self.username} '
            f'broker_value: {broker_value}'
        )
        return response
