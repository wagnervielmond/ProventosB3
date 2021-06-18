#!/usr/bin/python3.8
import asyncio
import logging

from bolsaprov.bolsa import B3AsyncBackend

logging.basicConfig(
    format=(
        '%(asctime)s.%(msecs)03d %(levelname)s {%(module)s} [%(funcName)s] '
        '%(message)s'
    ),
    datefmt='%Y-%m-%d,%H:%M:%S',
    level=logging.DEBUG
)


async def main():
    from datetime import datetime
    start_datetime = datetime.now()
    logging.info(f'Starting... {start_datetime}')
    b3_httpclient = B3AsyncBackend(
        username='user',
        password='senha',
        captcha_service=None  # captcha_service is not required yet
    )
    brokers = await b3_httpclient.get_brokers_with_accounts()
    assets_extract = (
        await b3_httpclient.get_brokers_account_portfolio_assets_extract(
            brokers=brokers
        )
    )
    print(assets_extract)
    await b3_httpclient.session_close()
    await b3_httpclient.connection_close()

    logging.info(f'Finish script... {datetime.now() - start_datetime}')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())









# user = sys.argv[1] # usuario da B3
# pwd = sys.argv[2] # senha da B3
# idUsuario = sys.argv[3]
# idCarteira = sys.argv[4]
# idCorretora = sys.argv[5]

# dbPwd = (base64.b64decode("Q1BEYWRtaW4wISE=".encode('ascii'))).decode('ascii') # password da conexao com o mariaDB 
# b3pass = (base64.b64decode("R2VGaWlzMjAyMSEhIQ==".encode('ascii'))).decode('ascii') # senha criptogradafa da b3

# CONNECT
# mydb = mysql.connector.connect(
#   host="localhost",
#   user="gefiis",
# #   password=dbPwd,
#   password="GeFiis2021!!!",
#   database="gefiis"
# )

# abre o cursor para atualizar a lista de ativos direto na B3 - 08-06-2021
# mycursor = mydb.cursor()

#dados de acesso ao CEI da B3
# user = '00781605024'
# pwd = message

# logging.basicConfig(
#     format=(
#         '%(asctime)s.%(msecs)03d %(levelname)s {%(module)s} [%(funcName)s] '
#         '%(message)s'
#     ),
#     datefmt='%Y-%m-%d,%H:%M:%S',
#     level=logging.DEBUG
# )


# async def main():
#     from datetime import datetime
#     start_datetime = datetime.now()
#     logging.info(f'Starting... {start_datetime}')
#     b3_httpclient = B3AsyncBackend(
#         username='00781605024',
#         password=b3pass,
#         captcha_service=None  # captcha_service is not required yet
#     )
#     brokers = await b3_httpclient.get_brokers_with_accounts()
#     assets_extract = (
#         await b3_httpclient.get_brokers_account_portfolio_assets_extract(
#             brokers=brokers
#         )
#     )

# 	print(assets_extract)

#     # try:
#     #     for dados in assets_extract:
#     #         for d in dados:
#     #             codigo_negociacao = vars(d)['raw_negotiation_name']
#     #             especificacao_ativo = vars(d)['asset_specification']
#     #             codigo_negociacao = vars(d)['raw_negotiation_code']
#     #             data_operacao = vars(d)['operation_date']
#     #             tipo = vars(d)['event_type']
#     #             quantidade = vars(d)['unit_amount']
#     #             fator_cotacao = vars(d)['quotation_factor']
#     #             valor_bruto = vars(d)['bruto_price']
#     #             valor_liquido = vars(d)['liqudo_price']

#     #             cod = codigo_negociacao[len(codigo_negociacao) -1]
#     #             if cod == 'F':
#     #                 retornoNegociacao = codigo_negociacao[0: -1]
#     #             else:
#     #                 retornoNegociacao = codigo_negociacao

#     #             # try:
#     #             #     sqlID = "SELECT id_ativo FROM ativos WHERE ticker = %s"
#     #             #     mycursor.execute(sqlID, (retornoNegociacao))
#     #             #     idTicker = mycursor.fetchall()

#     #             #     tipoop = ''
#     #             #     if acao == 'buy':
#     #             #         tipoop = 'C'
#     #             #     else:
#     #             #         tipoop = 'V'

#     #             #     # sql = "INSERT INTO `ativos_carteira`(`id_ativo_fk`, `id_carteira_fk`, `id_corretora_fk`, `id_usuario_fk`, `data`, `tipo`, `quantidade`, `valor`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
#     #             #     # mycursor.execute(sql, (idTicker, 1, 1, 1, data_operacao, acao, quantidade, valor_unit))

#     #             #     print(idTicker, idCarteira, idCorretora, idUsuario, data_operacao, tipoop, quantidade, valor_unit)

#     #             # except mysql.connector.Error as err:
#     #             #     print(err)
#     #             #     print("Error Code:", err.errno)
#     #             #     print("SQLSTATE", err.sqlstate)
#     #             #     print("Message", err.msg)
                
#     #             print(data_operacao, tipo, retornoNegociacao, especificacao_ativo, quantidade, valor_bruto, valor_liquido, fator_cotacao)

#     # except Exception as e: 
#     #     print(e)

# 	await b3_httpclient.session_close()
# 	await b3_httpclient.connection_close()

# 	logging.info(f'Finish script... {datetime.now() - start_datetime}')

# # mydb.commit()
# # mydb.close()  ## close db connection

# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())















# import csv
# import requests
# import time
# import urllib3
# from datetime import datetime
# from bs4 import BeautifulSoup
# import base64
# import yaml

# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# print("Starting...{}".format(datetime.now()))

# with open("config_skeleton.yaml", 'r') as stream:
#     try:
#         config = yaml.safe_load(stream)

#     except yaml.YAMLError as exc:
#         print(exc)

# cpf = config['cpf']
# senha = config['senha']

# login_url = "https://cei.b3.com.br/CEI_Responsivo/login.aspx"
# home_url = "https://cei.b3.com.br/CEI_Responsivo/home.aspx"
# # negociacao_url = "https://cei.b3.com.br/CEI_Responsivo/negociacao-de-ativos.aspx"
# proventos_url = "https://cei.b3.com.br/CEI_Responsivo/ConsultarProventos.aspx"

# session_requests = requests.session()

# #abre login para caturar tokens
# result = session_requests.get(login_url,verify=False)

# print(result.text)

# soup = BeautifulSoup(result.text, "html.parser")

# view_state = soup.find(id='__VIEWSTATE')['value']
# viewstate_generator = soup.find(id='__VIEWSTATEGENERATOR')['value']
# event_validation = soup.find(id='__EVENTVALIDATION')['value']

# payload = {
# 	"__EVENTTARGET": "",
# 	"__EVENTARGUMENT": "",
# 	"ctl00$ContentPlaceHolder1$txtLogin": cpf, 
# 	"ctl00$ContentPlaceHolder1$txtSenha": senha, 
# 	"__VIEWSTATEGENERATOR": viewstate_generator,
# 	"__EVENTVALIDATION": event_validation,
# 	"__VIEWSTATE": view_state,
# 	"ctl00$ContentPlaceHolder1$btnLogar": "Entrar"
# }

# #efetua login
# result = session_requests.post(
# 	login_url, 
# 	data = payload,
# 	headers = dict(referer=login_url)
# )

# #abre Consultar Proventos
# result = session_requests.get(
# 	proventos_url,
# 	headers = dict(referer=home_url)
# )

# soup = BeautifulSoup(result.text, "html.parser")

# # pega a data do periodo dos proventos
# data = soup.find(id='ctl00_ContentPlaceHolder1_txtData')['value']
# # print(data)
# # data_fim = soup.find(id='ctl00_ContentPlaceHolder1_txtDataAteBolsa')['value']
# conta = "0"

# #percorre todos os agentes (corretoras)
# agentes = soup.find(id='ctl00_ContentPlaceHolder1_ddlAgentes').find_all('option')

# for agente_aux in agentes:

# 	view_state = soup.find(id='__VIEWSTATE')['value']
# 	viewstate_generator = soup.find(id='__VIEWSTATEGENERATOR')['value']
# 	event_validation = soup.find(id='__EVENTVALIDATION')['value']

# 	agente = agente_aux['value']

# 	print("Mudando agente => agente: " + agente)

# 	payload = {
# 		"ctl00$ContentPlaceHolder1$ToolkitScriptManager1": "ctl00$ContentPlaceHolder1$updFiltro|ctl00$ContentPlaceHolder1$ddlAgentes",
# 		"ctl00_ContentPlaceHolder1_ToolkitScriptManager1_HiddenField": "",
# 		"__EVENTTARGET": "ctl00$ContentPlaceHolder1$ddlAgentes",
# 		"__EVENTARGUMENT": "",
# 		"__LASTFOCUS": "",
# 		# "ctl00$ContentPlaceHolder1$hdnPDF_EXCEL": "",
# 		"__VIEWSTATEGENERATOR": viewstate_generator,
# 		"__EVENTVALIDATION": event_validation,
# 		"__VIEWSTATE": view_state,
# 		"ctl00$ContentPlaceHolder1$txtData": data,
# 		# "ctl00$ContentPlaceHolder1$txtDataAteBolsa": data_fim,
# 		"ctl00$ContentPlaceHolder1$ddlContas": conta,
# 		"ctl00$ContentPlaceHolder1$ddlAgentes": agente
# 	}

# 	#seleciona agente (corretora)
# 	result = session_requests.post(
# 		proventos_url,
# 		data = payload,
# 		headers = dict(referer=proventos_url)
# 	)

# 	soup = BeautifulSoup(result.text, "html.parser")

# 	#percorre todas as contas
# 	contas = soup.find(id='ctl00_ContentPlaceHolder1_ddlContas').find_all('option')

# 	for conta_aux in contas:

# 		view_state = soup.find(id='__VIEWSTATE')['value']
# 		viewstate_generator = soup.find(id='__VIEWSTATEGENERATOR')['value']
# 		event_validation = soup.find(id='__EVENTVALIDATION')['value']

# 		conta = conta_aux['value']

# 		print("Mudando conta => agente: " + agente + " | conta: " + conta)

# 		payload = {
# 			"ctl00$ContentPlaceHolder1$ToolkitScriptManager1": "ctl00$ContentPlaceHolder1$updFiltro|ctl00$ContentPlaceHolder1$ddlAgentes",
# 			"ctl00_ContentPlaceHolder1_ToolkitScriptManager1_HiddenField": "",
# 			"__EVENTTARGET": "ctl00$ContentPlaceHolder1$ddlAgentes",
# 			"__EVENTARGUMENT": "",
# 			"__LASTFOCUS": "",
# 			# "ctl00$ContentPlaceHolder1$hdnPDF_EXCEL": "",
# 			"__VIEWSTATEGENERATOR": viewstate_generator,
# 			"__EVENTVALIDATION": event_validation,
# 			"__VIEWSTATE": view_state,
# 			"ctl00$ContentPlaceHolder1$txtData": data,
# 			# "ctl00$ContentPlaceHolder1$txtDataAteBolsa": data_fim,
# 			"ctl00$ContentPlaceHolder1$ddlContas": conta,
# 			"ctl00$ContentPlaceHolder1$ddlAgentes": agente,
# 			"ctl00$ContentPlaceHolder1$btnConsultar": "Consultar"
# 		}

# 		#seleciona conta e retorna resultado da busca
# 		result = session_requests.post(
# 			proventos_url,
# 			data = payload,
# 			headers = dict(referer=proventos_url)
# 		)

# 		soup = BeautifulSoup(result.text, "html.parser")

# ##### GRAVAR AQUI O RESULTADO

# 		data = []
# 		table = soup.find(id="ctl00_ContentPlaceHolder1_rptAgenteProventos_ctl00_lblAgenteProventos")

# 		if table != None:

# 			table_body = table.find('tbody')

# 			rows = table_body.find_all('tr')
# 			for row in rows:
# 			    cols = row.find_all('td')
# 			    colsd = [ele.text.replace('.','').replace(',','.').strip() for ele in cols]
# 			    colsd.append(agente)
# 			    colsd.append(conta)
# 			    data.append([ele for ele in colsd])

# 			file = open("CEIHIST-" + agente + "_" + conta + ".csv", "w")

# 			wtr = csv.writer(file, delimiter=';', lineterminator='\n')
# 			for x in data : wtr.writerow(x)

# 			file.close()

        
# #####


# 		#reinicializa busca
# 		view_state = soup.find(id='__VIEWSTATE')['value']
# 		viewstate_generator = soup.find(id='__VIEWSTATEGENERATOR')['value']
# 		event_validation = soup.find(id='__EVENTVALIDATION')['value']

# 		payload = {
# 			"ctl00$ContentPlaceHolder1$ToolkitScriptManager1": "ctl00$ContentPlaceHolder1$updFiltro|ctl00$ContentPlaceHolder1$btnConsultar",
# 			"ctl00$ContentPlaceHolder1$btnConsultar": "Consultar",
# 			"ctl00_ContentPlaceHolder1_ToolkitScriptManager1_HiddenField": "",
# 			"__EVENTTARGET": "",
# 			"__EVENTARGUMENT": "",
# 			"__LASTFOCUS": "",
# 			# "ctl00$ContentPlaceHolder1$hdnPDF_EXCEL": "",
# 			"__VIEWSTATEGENERATOR": viewstate_generator,
# 			"__EVENTVALIDATION": event_validation,
# 			"__VIEWSTATE": view_state,
# 			"ctl00$ContentPlaceHolder1$txtData": data,
# 			# "ctl00$ContentPlaceHolder1$txtDataAteBolsa": data_fim,
# 			"ctl00$ContentPlaceHolder1$ddlContas": conta,
# 			"ctl00$ContentPlaceHolder1$ddlAgentes": agente,
# 			"ctl00$ContentPlaceHolder1$btnConsultar": "Consultar"
# 		}

# 		result = session_requests.post(
# 			proventos_url,
# 			data = payload,
# 			headers = dict(referer=proventos_url)
# 		)

# 		soup = BeautifulSoup(result.text, "html.parser")


# print("Finish...{}".format(datetime.now()))

# time.sleep(1)