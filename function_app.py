import csv
import io
import logging
import os
from datetime import datetime, timezone

import pyodbc
import azure.functions as func
from azure.storage.filedatalake import DataLakeServiceClient

app = func.FunctionApp()

@app.timer_trigger(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def extract_chamado(myTimer: func.TimerRequest) -> None:
    logging.info('tabela chamado')
    
    sql_server = os.getenv("HOST")
    sql_database = os.getenv("DATABASE")
    sql_user = os.getenv("USER")
    sql_pass = os.getenv("PASSWORD")

    logging.info(f'servidor={sql_server}, banco de dados={sql_database}, usuario={sql_user}, senha={sql_pass} ')

    # Configura a string de conexão para o banco de dados SQL Server
    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={sql_server};"
        f"DATABASE={sql_database};"
        f"UID={sql_user};"
        f"PWD={sql_pass};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    try:
        # Estabelece a conexão com o banco de dados usando pyodbc
        with pyodbc.connect(conn_str) as conn:
            # Cria um cursor para executar a consulta
            cursor = conn.cursor()
            
            query = "select * from itsm.chamado"

            # Executa a consulta SQL
            cursor.execute(query)

            # Busca todos os resultados da consulta
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]

            logging.info(f'{len(rows)} linhas lidas de itsm.chamado')

        # Cria um buffer de memória para armazenar os dados CSV
        buffer = io.StringIO()
        # Cria um objeto CSV writer e escreve os dados no buffer
        writer = csv.writer(buffer)
        # Escreve o cabeçalho e as linhas no buffer CSV
        writer.writerow(columns)
        # Escreve todas as linhas no buffer CSV
        writer.writerows(rows)

        # Grava o arquivo no contêiner bronze do Data Lake, particionado por data
        now = datetime.now(timezone.utc)
        file_path = f"chamado/{now:%Y/%m/%d}/chamado_{now:%Y%m%d_%H%M%S}.csv"

        #itsm/chamado/year=2024/month=06/day=05/chamado_20240605_123456.csv
        #file_path = f"itsm/chamado/year={now:%Y}/month={now:%m}/day={now:%d}/chamado_{now:%Y%m%d_%H%M%S}.csv"

        # Cria o cliente do Data Lake e grava o arquivo no contêiner bronze
        datalake = DataLakeServiceClient.from_connection_string(os.getenv("DATALAKE_CONNECTION_STRING"))
        # Cria o cliente do sistema de arquivos e grava o arquivo no contêiner bronze
        file_client = datalake.get_file_system_client("bronze").get_file_client(file_path)
        # Grava os dados do buffer no arquivo do Data Lake, sobrescrevendo se já existir
        file_client.upload_data(buffer.getvalue().encode("utf-8"), overwrite=True)

        logging.info(f'Arquivo gravado em bronze/{file_path}')

    except Exception as e:
        logging.error(f"Erro ao ler itsm.chamado: {str(e)}")
        raise

@app.timer_trigger(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def extract_chamado_sla(myTimer: func.TimerRequest) -> None:
    logging.info('tabela chamado_sla')
    
    sql_server = os.getenv("HOST")
    sql_database = os.getenv("DATABASE")
    sql_user = os.getenv("USER")
    sql_pass = os.getenv("PASSWORD")

    logging.info(f'servidor={sql_server}, banco de dados={sql_database}, usuario={sql_user}, senha={sql_pass} ')

    # Configura a string de conexão para o banco de dados SQL Server
    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={sql_server};"
        f"DATABASE={sql_database};"
        f"UID={sql_user};"
        f"PWD={sql_pass};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    try:
        # Estabelece a conexão com o banco de dados usando pyodbc
        with pyodbc.connect(conn_str) as conn:
            # Cria um cursor para executar a consulta
            cursor = conn.cursor()
            
            query = "select * from itsm.chamado_sla"

            # Executa a consulta SQL
            cursor.execute(query)

            # Busca todos os resultados da consulta
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]

            logging.info(f'{len(rows)} linhas lidas de itsm.chamado_sla')

        # Cria um buffer de memória para armazenar os dados CSV
        buffer = io.StringIO()
        # Cria um objeto CSV writer e escreve os dados no buffer
        writer = csv.writer(buffer)
        # Escreve o cabeçalho e as linhas no buffer CSV
        writer.writerow(columns)
        # Escreve todas as linhas no buffer CSV
        writer.writerows(rows)

        # Grava o arquivo no contêiner bronze do Data Lake, particionado por data
        now = datetime.now(timezone.utc)
        file_path = f"chamado_sla/{now:%Y/%m/%d}/chamado_sla_{now:%Y%m%d_%H%M%S}.csv"

        #itsm/chamado_sla/year=2024/month=06/day=05/chamado_sla_20240605_123456.csv
        #file_path = f"itsm/chamado_sla/year={now:%Y}/month={now:%m}/day={now:%d}/chamado_sla_{now:%Y%m%d_%H%M%S}.csv"

        # Cria o cliente do Data Lake e grava o arquivo no contêiner bronze
        datalake = DataLakeServiceClient.from_connection_string(os.getenv("DATALAKE_CONNECTION_STRING"))
        # Cria o cliente do sistema de arquivos e grava o arquivo no contêiner bronze
        file_client = datalake.get_file_system_client("bronze").get_file_client(file_path)
        # Grava os dados do buffer no arquivo do Data Lake, sobrescrevendo se já existir
        file_client.upload_data(buffer.getvalue().encode("utf-8"), overwrite=True)

        logging.info(f'Arquivo gravado em bronze/{file_path}')

    except Exception as e:
        logging.error(f"Erro ao ler itsm.chamado_sla: {str(e)}")
        raise

@app.timer_trigger(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def extract_chamado_status_historico(myTimer: func.TimerRequest) -> None:
    logging.info('tabela chamado_status_historico')
    
    sql_server = os.getenv("HOST")
    sql_database = os.getenv("DATABASE")
    sql_user = os.getenv("USER")
    sql_pass = os.getenv("PASSWORD")

    logging.info(f'servidor={sql_server}, banco de dados={sql_database}, usuario={sql_user}, senha={sql_pass} ')

    # Configura a string de conexão para o banco de dados SQL Server
    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={sql_server};"
        f"DATABASE={sql_database};"
        f"UID={sql_user};"
        f"PWD={sql_pass};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    try:
        # Estabelece a conexão com o banco de dados usando pyodbc
        with pyodbc.connect(conn_str) as conn:
            # Cria um cursor para executar a consulta
            cursor = conn.cursor()
            
            query = "select * from itsm.chamado_status_historico"

            # Executa a consulta SQL
            cursor.execute(query)

            # Busca todos os resultados da consulta
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]

            logging.info(f'{len(rows)} linhas lidas de itsm.chamado_status_historico')

        # Cria um buffer de memória para armazenar os dados CSV
        buffer = io.StringIO()
        # Cria um objeto CSV writer e escreve os dados no buffer
        writer = csv.writer(buffer)
        # Escreve o cabeçalho e as linhas no buffer CSV
        writer.writerow(columns)
        # Escreve todas as linhas no buffer CSV
        writer.writerows(rows)

        # Grava o arquivo no contêiner bronze do Data Lake, particionado por data
        now = datetime.now(timezone.utc)
        file_path = f"chamado_status_historico/{now:%Y/%m/%d}/chamado_status_historico_{now:%Y%m%d_%H%M%S}.csv"

        #itsm/chamado_status_historico/year=2024/month=06/day=05/chamado_status_historico_20240605_123456.csv
        #file_path = f"itsm/chamado_status_historico/year={now:%Y}/month={now:%m}/day={now:%d}/chamado_status_historico_{now:%Y%m%d_%H%M%S}.csv"

        # Cria o cliente do Data Lake e grava o arquivo no contêiner bronze
        datalake = DataLakeServiceClient.from_connection_string(os.getenv("DATALAKE_CONNECTION_STRING"))
        # Cria o cliente do sistema de arquivos e grava o arquivo no contêiner bronze
        file_client = datalake.get_file_system_client("bronze").get_file_client(file_path)
        # Grava os dados do buffer no arquivo do Data Lake, sobrescrevendo se já existir
        file_client.upload_data(buffer.getvalue().encode("utf-8"), overwrite=True)

        logging.info(f'Arquivo gravado em bronze/{file_path}')

    except Exception as e:
        logging.error(f"Erro ao ler itsm.chamado_status_historico: {str(e)}")
        raise

@app.timer_trigger(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def extract_cliente_organizacao(myTimer: func.TimerRequest) -> None:
    logging.info('tabela cliente_organizacao')
    
    sql_server = os.getenv("HOST")
    sql_database = os.getenv("DATABASE")
    sql_user = os.getenv("USER")
    sql_pass = os.getenv("PASSWORD")

    logging.info(f'servidor={sql_server}, banco de dados={sql_database}, usuario={sql_user}, senha={sql_pass} ')

    # Configura a string de conexão para o banco de dados SQL Server
    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={sql_server};"
        f"DATABASE={sql_database};"
        f"UID={sql_user};"
        f"PWD={sql_pass};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    try:
        # Estabelece a conexão com o banco de dados usando pyodbc
        with pyodbc.connect(conn_str) as conn:
            # Cria um cursor para executar a consulta
            cursor = conn.cursor()
            
            query = "select * from itsm.cliente_organizacao"

            # Executa a consulta SQL
            cursor.execute(query)

            # Busca todos os resultados da consulta
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]

            logging.info(f'{len(rows)} linhas lidas de itsm.cliente_organizacao')

        # Cria um buffer de memória para armazenar os dados CSV
        buffer = io.StringIO()
        # Cria um objeto CSV writer e escreve os dados no buffer
        writer = csv.writer(buffer)
        # Escreve o cabeçalho e as linhas no buffer CSV
        writer.writerow(columns)
        # Escreve todas as linhas no buffer CSV
        writer.writerows(rows)

        # Grava o arquivo no contêiner bronze do Data Lake, particionado por data
        now = datetime.now(timezone.utc)
        file_path = f"cliente_organizacao/{now:%Y/%m/%d}/cliente_organizacao_{now:%Y%m%d_%H%M%S}.csv"

        #itsm/cliente_organizacao/year=2024/month=06/day=05/cliente_organizacao_20240605_123456.csv
        #file_path = f"itsm/cliente_organizacao/year={now:%Y}/month={now:%m}/day={now:%d}/cliente_organizacao_{now:%Y%m%d_%H%M%S}.csv"

        # Cria o cliente do Data Lake e grava o arquivo no contêiner bronze
        datalake = DataLakeServiceClient.from_connection_string(os.getenv("DATALAKE_CONNECTION_STRING"))
        # Cria o cliente do sistema de arquivos e grava o arquivo no contêiner bronze
        file_client = datalake.get_file_system_client("bronze").get_file_client(file_path)
        # Grava os dados do buffer no arquivo do Data Lake, sobrescrevendo se já existir
        file_client.upload_data(buffer.getvalue().encode("utf-8"), overwrite=True)

        logging.info(f'Arquivo gravado em bronze/{file_path}')

    except Exception as e:
        logging.error(f"Erro ao ler itsm.cliente_organizacao: {str(e)}")
        raise

@app.timer_trigger(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def extract_analista(myTimer: func.TimerRequest) -> None:
    logging.info('tabela analista')
    
    sql_server = os.getenv("HOST")
    sql_database = os.getenv("DATABASE")
    sql_user = os.getenv("USER")
    sql_pass = os.getenv("PASSWORD")

    logging.info(f'servidor={sql_server}, banco de dados={sql_database}, usuario={sql_user}, senha={sql_pass} ')

    # Configura a string de conexão para o banco de dados SQL Server
    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={sql_server};"
        f"DATABASE={sql_database};"
        f"UID={sql_user};"
        f"PWD={sql_pass};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    try:
        # Estabelece a conexão com o banco de dados usando pyodbc
        with pyodbc.connect(conn_str) as conn:
            # Cria um cursor para executar a consulta
            cursor = conn.cursor()
            
            query = "select * from itsm.analista"

            # Executa a consulta SQL
            cursor.execute(query)

            # Busca todos os resultados da consulta
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]

            logging.info(f'{len(rows)} linhas lidas de itsm.analista')

        # Cria um buffer de memória para armazenar os dados CSV
        buffer = io.StringIO()
        # Cria um objeto CSV writer e escreve os dados no buffer
        writer = csv.writer(buffer)
        # Escreve o cabeçalho e as linhas no buffer CSV
        writer.writerow(columns)
        # Escreve todas as linhas no buffer CSV
        writer.writerows(rows)

        # Grava o arquivo no contêiner bronze do Data Lake, particionado por data
        now = datetime.now(timezone.utc)
        file_path = f"analista/{now:%Y/%m/%d}/analista_{now:%Y%m%d_%H%M%S}.csv"

        #itsm/analista/year=2024/month=06/day=05/analista_20240605_123456.csv
        #file_path = f"itsm/analista/year={now:%Y}/month={now:%m}/day={now:%d}/analista_{now:%Y%m%d_%H%M%S}.csv"

        # Cria o cliente do Data Lake e grava o arquivo no contêiner bronze
        datalake = DataLakeServiceClient.from_connection_string(os.getenv("DATALAKE_CONNECTION_STRING"))
        # Cria o cliente do sistema de arquivos e grava o arquivo no contêiner bronze
        file_client = datalake.get_file_system_client("bronze").get_file_client(file_path)
        # Grava os dados do buffer no arquivo do Data Lake, sobrescrevendo se já existir
        file_client.upload_data(buffer.getvalue().encode("utf-8"), overwrite=True)

        logging.info(f'Arquivo gravado em bronze/{file_path}')

    except Exception as e:
        logging.error(f"Erro ao ler itsm.analista: {str(e)}")
        raise

@app.timer_trigger(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def extract_categoria(myTimer: func.TimerRequest) -> None:
    logging.info('tabela categoria')
    
    sql_server = os.getenv("HOST")
    sql_database = os.getenv("DATABASE")
    sql_user = os.getenv("USER")
    sql_pass = os.getenv("PASSWORD")

    logging.info(f'servidor={sql_server}, banco de dados={sql_database}, usuario={sql_user}, senha={sql_pass} ')

    # Configura a string de conexão para o banco de dados SQL Server
    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={sql_server};"
        f"DATABASE={sql_database};"
        f"UID={sql_user};"
        f"PWD={sql_pass};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    try:
        # Estabelece a conexão com o banco de dados usando pyodbc
        with pyodbc.connect(conn_str) as conn:
            # Cria um cursor para executar a consulta
            cursor = conn.cursor()
            
            query = "select * from itsm.categoria"

            # Executa a consulta SQL
            cursor.execute(query)

            # Busca todos os resultados da consulta
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]

            logging.info(f'{len(rows)} linhas lidas de itsm.categoria')

        # Cria um buffer de memória para armazenar os dados CSV
        buffer = io.StringIO()
        # Cria um objeto CSV writer e escreve os dados no buffer
        writer = csv.writer(buffer)
        # Escreve o cabeçalho e as linhas no buffer CSV
        writer.writerow(columns)
        # Escreve todas as linhas no buffer CSV
        writer.writerows(rows)

        # Grava o arquivo no contêiner bronze do Data Lake, particionado por data
        now = datetime.now(timezone.utc)
        file_path = f"categoria/{now:%Y/%m/%d}/categoria_{now:%Y%m%d_%H%M%S}.csv"

        #itsm/categoria/year=2024/month=06/day=05/categoria_20240605_123456.csv
        #file_path = f"itsm/categoria/year={now:%Y}/month={now:%m}/day={now:%d}/categoria_{now:%Y%m%d_%H%M%S}.csv"

        # Cria o cliente do Data Lake e grava o arquivo no contêiner bronze
        datalake = DataLakeServiceClient.from_connection_string(os.getenv("DATALAKE_CONNECTION_STRING"))
        # Cria o cliente do sistema de arquivos e grava o arquivo no contêiner bronze
        file_client = datalake.get_file_system_client("bronze").get_file_client(file_path)
        # Grava os dados do buffer no arquivo do Data Lake, sobrescrevendo se já existir
        file_client.upload_data(buffer.getvalue().encode("utf-8"), overwrite=True)

        logging.info(f'Arquivo gravado em bronze/{file_path}')

    except Exception as e:
        logging.error(f"Erro ao ler itsm.categoria: {str(e)}")
        raise

@app.timer_trigger(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def extract_csat_avaliacao(myTimer: func.TimerRequest) -> None:
    logging.info('tabela csat_avaliacao')
    
    sql_server = os.getenv("HOST")
    sql_database = os.getenv("DATABASE")
    sql_user = os.getenv("USER")
    sql_pass = os.getenv("PASSWORD")

    logging.info(f'servidor={sql_server}, banco de dados={sql_database}, usuario={sql_user}, senha={sql_pass} ')

    # Configura a string de conexão para o banco de dados SQL Server
    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={sql_server};"
        f"DATABASE={sql_database};"
        f"UID={sql_user};"
        f"PWD={sql_pass};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    try:
        # Estabelece a conexão com o banco de dados usando pyodbc
        with pyodbc.connect(conn_str) as conn:
            # Cria um cursor para executar a consulta
            cursor = conn.cursor()
            
            query = "select * from itsm.csat_avaliacao"

            # Executa a consulta SQL
            cursor.execute(query)

            # Busca todos os resultados da consulta
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]

            logging.info(f'{len(rows)} linhas lidas de itsm.csat_avaliacao')

        # Cria um buffer de memória para armazenar os dados CSV
        buffer = io.StringIO()
        # Cria um objeto CSV writer e escreve os dados no buffer
        writer = csv.writer(buffer)
        # Escreve o cabeçalho e as linhas no buffer CSV
        writer.writerow(columns)
        # Escreve todas as linhas no buffer CSV
        writer.writerows(rows)

        # Grava o arquivo no contêiner bronze do Data Lake, particionado por data
        now = datetime.now(timezone.utc)
        logger.error(f"Erro ao conectar ou consultar a tabela solicitante: {e}")

        #itsm/csat_avaliacao/year=2024/month=06/day=05/csat_avaliacao_20240605_123456.csv
        #file_path = f"itsm/csat_avaliacao/year={now:%Y}/month={now:%m}/day={now:%d}/csat_avaliacao_{now:%Y%m%d_%H%M%S}.csv"

        # Cria o cliente do Data Lake e grava o arquivo no contêiner bronze
        datalake = DataLakeServiceClient.from_connection_string(os.getenv("DATALAKE_CONNECTION_STRING"))
        # Cria o cliente do sistema de arquivos e grava o arquivo no contêiner bronze
        file_client = datalake.get_file_system_client("bronze").get_file_client(file_path)
        # Grava os dados do buffer no arquivo do Data Lake, sobrescrevendo se já existir
        file_client.upload_data(buffer.getvalue().encode("utf-8"), overwrite=True)

        logging.info(f'Arquivo gravado em bronze/{file_path}')

    except Exception as e:
        logging.error(f"Erro ao ler itsm.csat_avaliacao: {str(e)}")
        raise

@app.timer_trigger(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def extract_fila(myTimer: func.TimerRequest) -> None:
    logging.info('tabela fila')
    
    sql_server = os.getenv("HOST")
    sql_database = os.getenv("DATABASE")
    sql_user = os.getenv("USER")
    sql_pass = os.getenv("PASSWORD")

    logging.info(f'servidor={sql_server}, banco de dados={sql_database}, usuario={sql_user}, senha={sql_pass} ')

    # Configura a string de conexão para o banco de dados SQL Server
    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={sql_server};"
        f"DATABASE={sql_database};"
        f"UID={sql_user};"
        f"PWD={sql_pass};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )


    try:
        # Estabelece a conexão com o banco de dados usando pyodbc
        with pyodbc.connect(conn_str) as conn:
            # Cria um cursor para executar a consulta
            cursor = conn.cursor()
            
            query = "select * from itsm.fila"

            # Executa a consulta SQL
            cursor.execute(query)

            # Busca todos os resultados da consulta
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]

            logging.info(f'{len(rows)} linhas lidas de itsm.fila')

        # Cria um buffer de memória para armazenar os dados CSV
        buffer = io.StringIO()
        # Cria um objeto CSV writer e escreve os dados no buffer
        writer = csv.writer(buffer)
        # Escreve o cabeçalho e as linhas no buffer CSV
        writer.writerow(columns)
        # Escreve todas as linhas no buffer CSV
        writer.writerows(rows)

        # Grava o arquivo no contêiner bronze do Data Lake, particionado por data
        now = datetime.now(timezone.utc)
        file_path = f"fila/{now:%Y/%m/%d}/fila_{now:%Y%m%d_%H%M%S}.csv"

        #itsm/fila/year=2024/month=06/day=05/fila_20240605_123456.csv
        #file_path = f"itsm/fila/year={now:%Y}/month={now:%m}/day={now:%d}/fila_{now:%Y%m%d_%H%M%S}.csv"

        # Cria o cliente do Data Lake e grava o arquivo no contêiner bronze
        datalake = DataLakeServiceClient.from_connection_string(os.getenv("DATALAKE_CONNECTION_STRING"))
        # Cria o cliente do sistema de arquivos e grava o arquivo no contêiner bronze
        file_client = datalake.get_file_system_client("bronze").get_file_client(file_path)
        # Grava os dados do buffer no arquivo do Data Lake, sobrescrevendo se já existir
        file_client.upload_data(buffer.getvalue().encode("utf-8"), overwrite=True)

        logging.info(f'Arquivo gravado em bronze/{file_path}')

    except Exception as e:
        logging.error(f"Erro ao ler itsm.fila: {str(e)}")
        raise

@app.timer_trigger(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def extract_sla(myTimer: func.TimerRequest) -> None:
    logging.info('tabela sla')
    
    sql_server = os.getenv("HOST")
    sql_database = os.getenv("DATABASE")
    sql_user = os.getenv("USER")
    sql_pass = os.getenv("PASSWORD")

    logging.info(f'servidor={sql_server}, banco de dados={sql_database}, usuario={sql_user}, senha={sql_pass} ')

    # Configura a string de conexão para o banco de dados SQL Server
    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={sql_server};"
        f"DATABASE={sql_database};"
        f"UID={sql_user};"
        f"PWD={sql_pass};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )


    try:
        # Estabelece a conexão com o banco de dados usando pyodbc
        with pyodbc.connect(conn_str) as conn:
            # Cria um cursor para executar a consulta
            cursor = conn.cursor()
            
            query = "select * from itsm.sla"

            # Executa a consulta SQL
            cursor.execute(query)

            # Busca todos os resultados da consulta
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]

            logging.info(f'{len(rows)} linhas lidas de itsm.sla')

        # Cria um buffer de memória para armazenar os dados CSV
        buffer = io.StringIO()
        # Cria um objeto CSV writer e escreve os dados no buffer
        writer = csv.writer(buffer)
        # Escreve o cabeçalho e as linhas no buffer CSV
        writer.writerow(columns)
        # Escreve todas as linhas no buffer CSV
        writer.writerows(rows)

        # Grava o arquivo no contêiner bronze do Data Lake, particionado por data
        now = datetime.now(timezone.utc)
        file_path = f"sla/{now:%Y/%m/%d}/sla_{now:%Y%m%d_%H%M%S}.csv"

        #itsm/sla/year=2024/month=06/day=05/sla_20240605_123456.csv
        #file_path = f"itsm/sla/year={now:%Y}/month={now:%m}/day={now:%d}/sla_{now:%Y%m%d_%H%M%S}.csv"

        # Cria o cliente do Data Lake e grava o arquivo no contêiner bronze
        datalake = DataLakeServiceClient.from_connection_string(os.getenv("DATALAKE_CONNECTION_STRING"))
        # Cria o cliente do sistema de arquivos e grava o arquivo no contêiner bronze
        file_client = datalake.get_file_system_client("bronze").get_file_client(file_path)
        # Grava os dados do buffer no arquivo do Data Lake, sobrescrevendo se já existir
        file_client.upload_data(buffer.getvalue().encode("utf-8"), overwrite=True)

        logging.info(f'Arquivo gravado em bronze/{file_path}')

    except Exception as e:
        logging.error(f"Erro ao ler itsm.sla: {str(e)}")
        raise

@app.timer_trigger(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def extract_solicitante(myTimer: func.TimerRequest) -> None:
    logging.info('tabela solicitante')
    
    sql_server = os.getenv("HOST")
    sql_database = os.getenv("DATABASE")
    sql_user = os.getenv("USER")
    sql_pass = os.getenv("PASSWORD")

    logging.info(f'servidor={sql_server}, banco de dados={sql_database}, usuario={sql_user}, senha={sql_pass} ')

    # Configura a string de conexão para o banco de dados SQL Server
    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={sql_server};"
        f"DATABASE={sql_database};"
        f"UID={sql_user};"
        f"PWD={sql_pass};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )


    try:
        # Estabelece a conexão com o banco de dados usando pyodbc
        with pyodbc.connect(conn_str) as conn:
            # Cria um cursor para executar a consulta
            cursor = conn.cursor()
            
            query = "select * from itsm.solicitante"

            # Executa a consulta SQL
            cursor.execute(query)

            # Busca todos os resultados da consulta
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]

            logging.info(f'{len(rows)} linhas lidas de itsm.solicitante')

        # Cria um buffer de memória para armazenar os dados CSV
        buffer = io.StringIO()
        # Cria um objeto CSV writer e escreve os dados no buffer
        writer = csv.writer(buffer)
        # Escreve o cabeçalho e as linhas no buffer CSV
        writer.writerow(columns)
        # Escreve todas as linhas no buffer CSV
        writer.writerows(rows)

        # Grava o arquivo no contêiner bronze do Data Lake, particionado por data
        now = datetime.now(timezone.utc)
        file_path = f"solicitante/{now:%Y/%m/%d}/solicitante_{now:%Y%m%d_%H%M%S}.csv"

        #itsm/solicitante/year=2024/month=06/day=05/solicitante_20240605_123456.csv
        #file_path = f"itsm/solicitante/year={now:%Y}/month={now:%m}/day={now:%d}/solicitante_{now:%Y%m%d_%H%M%S}.csv"

        # Cria o cliente do Data Lake e grava o arquivo no contêiner bronze
        datalake = DataLakeServiceClient.from_connection_string(os.getenv("DATALAKE_CONNECTION_STRING"))
        # Cria o cliente do sistema de arquivos e grava o arquivo no contêiner bronze
        file_client = datalake.get_file_system_client("bronze").get_file_client(file_path)
        # Grava os dados do buffer no arquivo do Data Lake, sobrescrevendo se já existir
        file_client.upload_data(buffer.getvalue().encode("utf-8"), overwrite=True)

        logging.info(f'Arquivo gravado em bronze/{file_path}')

    except Exception as e:
        logging.error(f"Erro ao ler itsm.solicitante: {str(e)}")
        raise