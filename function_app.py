import logging
import azure.functions as func
import os
import urllib.request
import urllib.parse
import pyodbc

app = func.FunctionApp()

#chamado
@app.timer_trigger(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False,
                use_monitor=False)
def extract_chamado(myTimer: func.TimerRequest) -> None:
    #importar variáveis de ambiente
    user_sql = os.getenv("USER")
    database_sql = os.getenv("DATABASE")
    host_sql = os.getenv("HOST")
    password_sql = os.getenv("PASSWORD")
    
    #como criar uma connection string usando pyodbc
    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={host_sql};"
        f"DATABASE={database_sql};"
        f"UID={user_sql};"
        f"PWD={{{password_sql}}};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;" 
        "Connection Timeout=30;"
    )
    try:
        # Criar a conexao com o banco 
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            
            # fazer um select * na tabela 
            cursor.execute("SELECT * FROM itsm.chamado")
            rows = cursor.fetchall()
            
            # imprimir os dados da tabela usando logging.info()
            if not rows:
                logging.info("A consulta não retornou nenhum dado.")
            else:
                for row in rows:
                    logging.info(f"Registro encontrado: {row}")
                    
    except pyodbc.Error as e:
        logging.error(f"Erro ao conectar ou consultar o banco de dados: {e}")

    print(host_sql)
    logging.info(user_sql)
    logging.info(database_sql)
    logging.info(host_sql)
    logging.info(password_sql)

    #Criar a conexão com o banco de dados
    #Fazer um select * na tabela
    #Imprimir os dados da tabela usando logging.info

#Chamado_sla
@app.timer_trigger(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False,
                use_monitor=False)
def extract_chamado_sla(myTimer: func.TimerRequest) -> None:
    #importar variáveis de ambiente
    user_sql = os.getenv("USER")
    database_sql = os.getenv("DATABASE")
    host_sql = os.getenv("HOST")
    password_sql = os.getenv("PASSWORD")
    
    #como criar uma connection string usando pyodbc
    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={host_sql};"
        f"DATABASE={database_sql};"
        f"UID={user_sql};"
        f"PWD={{{password_sql}}};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;" 
        "Connection Timeout=30;"
    )
    try:
        # Criar a conexao com o banco 
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            
            # fazer um select * na tabela 
            cursor.execute("SELECT * FROM itsm.chamado_sla")
            rows = cursor.fetchall()
            
            # imprimir os dados da tabela usando logging.info()
            if not rows:
                logging.info("A consulta não retornou nenhum dado.")
            else:
                for row in rows:
                    logging.info(f"Registro encontrado: {row}")
                    
    except pyodbc.Error as e:
        logging.error(f"Erro ao conectar ou consultar o banco de dados: {e}")

    print(host_sql)
    logging.info(user_sql)
    logging.info(database_sql)
    logging.info(host_sql)
    logging.info(password_sql)

    #analista

    #categoria

    #chamado_status_historico

    #cliente_organizacao

    #csat_avaliacao

    #fila

    #sla

    #solicitante

@app.schedule(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def timer_trigger_turmac(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Hello Word!')

@app.route(route="http_trigger", auth_level=func.AuthLevel.ANONYMOUS)
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

@app.route(route="http_trigger_v3", auth_level=func.AuthLevel.ANONYMOUS)
def http_trigger_v3(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Valor recebido: {name}. - respondido pela http_trigger_v3.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

@app.schedule(schedule="0 */2 * * * *", arg_name="callTimer", run_on_startup=True,
              use_monitor=False)
def timer_trigger_chama_http(callTimer: func.TimerRequest) -> None:
    if callTimer.past_due:
        logging.info('O timer (chamador) esta atrasado!')

    base_url = os.environ.get(
        "ECHO_FUNCTION_URL",
        "https://funcapp-giovana001-hzhvefgud6e2hyc6.canadacentral-01.azurewebsites.net/api/http_trigger_v3"
    )
    name = "ola-do-timer"
    url = f"{base_url}?{urllib.parse.urlencode({'name': name})}"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            resposta = response.read().decode("utf-8")
            logging.info(f"Resposta da http_trigger_v3: {resposta}")
    except Exception as e:
        logging.error(f"Erro ao chamar a http_trigger_v3: {e}")
