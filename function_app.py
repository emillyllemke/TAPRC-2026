import logging
import os
import io
import csv
from datetime import datetime, timezone

import azure.functions as func
import pyodbc
from azure.storage.filedatalake import DataLakeServiceClient

app = func.FunctionApp()

logger = logging.getLogger(__name__)

# chamado
@app.timer_trigger(
    schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False
)
def extract_chamado(myTimer: func.TimerRequest) -> None:
    user_sql = os.getenv("USER")
    database_sql = os.getenv("DATABASE")
    host_sql = os.getenv("HOST")
    password_sql = os.getenv("PASSWORD")

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
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM itsm.chamado"
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            logging.info(f'{len(rows)} linhas lidas de itsm.chamado')

        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(columns)
        writer.writerows(rows)

        now = datetime.now(timezone.utc)
        file_path = f"chamado/{now:%Y/%m/%d}/chamado_{now:%Y%m%d_%H%M%S}.csv"

        datalake = DataLakeServiceClient.from_connection_string(os.getenv("DATALAKE_CONNECTION_STRING"))
        file_client = datalake.get_file_system_client("bronze").get_file_client(file_path)
        file_client.upload_data(buffer.getvalue().encode("utf-8"), overwrite=True)

        logging.info(f'Arquivo gravado em bronze/{file_path}')

    except Exception as e:
        logging.error(f"Erro ao ler itsm.chamado: {str(e)}")
        raise


# Chamado_sla
@app.timer_trigger(
    schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False
)
def extract_chamado_sla(myTimer: func.TimerRequest) -> None:
    user_sql = os.getenv("USER")
    database_sql = os.getenv("DATABASE")
    host_sql = os.getenv("HOST")
    password_sql = os.getenv("PASSWORD")

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
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM itsm.chamado_sla"
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            logging.info(f'{len(rows)} linhas lidas de itsm.chamado_sla')

        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(columns)
        writer.writerows(rows)

        now = datetime.now(timezone.utc)
        file_path = f"chamado_sla/{now:%Y/%m/%d}/chamado_sla_{now:%Y%m%d_%H%M%S}.csv"

        datalake = DataLakeServiceClient.from_connection_string(os.getenv("DATALAKE_CONNECTION_STRING"))
        file_client = datalake.get_file_system_client("bronze").get_file_client(file_path)
        file_client.upload_data(buffer.getvalue().encode("utf-8"), overwrite=True)

        logging.info(f'Arquivo gravado em bronze/{file_path}')

    except Exception as e:
        logging.error(f"Erro ao ler itsm.chamado_sla: {str(e)}")
        raise


# Chamado_status_historico
@app.timer_trigger(
    schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False
)
def extract_chamado_status_historico(myTimer: func.TimerRequest) -> None:
    user_sql = os.getenv("USER")
    database_sql = os.getenv("DATABASE")
    host_sql = os.getenv("HOST")
    password_sql = os.getenv("PASSWORD")

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
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM itsm.chamado_status_historico"
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            logging.info(f'{len(rows)} linhas lidas de itsm.chamado_status_historico')

        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(columns)
        writer.writerows(rows)

        now = datetime.now(timezone.utc)
        file_path = f"chamado_status_historico/{now:%Y/%m/%d}/chamado_status_historico_{now:%Y%m%d_%H%M%S}.csv"

        datalake = DataLakeServiceClient.from_connection_string(os.getenv("DATALAKE_CONNECTION_STRING"))
        file_client = datalake.get_file_system_client("bronze").get_file_client(file_path)
        file_client.upload_data(buffer.getvalue().encode("utf-8"), overwrite=True)

        logging.info(f'Arquivo gravado em bronze/{file_path}')

    except Exception as e:
        logging.error(f"Erro ao ler itsm.chamado_status_historico: {str(e)}")
        raise


# cliente_organizacao
@app.timer_trigger(
    schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False
)
def extract_cliente_organizacao(myTimer: func.TimerRequest) -> None:
    user_sql = os.getenv("USER")
    database_sql = os.getenv("DATABASE")
    host_sql = os.getenv("HOST")
    password_sql = os.getenv("PASSWORD")

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
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM itsm.cliente_organizacao"
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            logging.info(f'{len(rows)} linhas lidas de itsm.cliente_organizacao')

        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(columns)
        writer.writerows(rows)

        now = datetime.now(timezone.utc)
        file_path = f"cliente_organizacao/{now:%Y/%m/%d}/cliente_organizacao_{now:%Y%m%d_%H%M%S}.csv"

        datalake = DataLakeServiceClient.from_connection_string(os.getenv("DATALAKE_CONNECTION_STRING"))
        file_client = datalake.get_file_system_client("bronze").get_file_client(file_path)
        file_client.upload_data(buffer.getvalue().encode("utf-8"), overwrite=True)

        logging.info(f'Arquivo gravado em bronze/{file_path}')

    except Exception as e:
        logging.error(f"Erro ao ler itsm.cliente_organizacao: {str(e)}")
        raise


# analista
@app.timer_trigger(
    schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False
)
def extract_analista(myTimer: func.TimerRequest) -> None:
    user_sql = os.getenv("USER")
    database_sql = os.getenv("DATABASE")
    host_sql = os.getenv("HOST")
    password_sql = os.getenv("PASSWORD")

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
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM itsm.analista"
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            logging.info(f'{len(rows)} linhas lidas de itsm.analista')

        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(columns)
        writer.writerows(rows)

        now = datetime.now(timezone.utc)
        file_path = f"analista/{now:%Y/%m/%d}/analista_{now:%Y%m%d_%H%M%S}.csv"

        datalake = DataLakeServiceClient.from_connection_string(os.getenv("DATALAKE_CONNECTION_STRING"))
        file_client = datalake.get_file_system_client("bronze").get_file_client(file_path)
        file_client.upload_data(buffer.getvalue().encode("utf-8"), overwrite=True)

        logging.info(f'Arquivo gravado em bronze/{file_path}')

    except Exception as e:
        logging.error(f"Erro ao ler itsm.analista: {str(e)}")
        raise


# categoria
@app.timer_trigger(
    schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False
)
def extract_categoria(myTimer: func.TimerRequest) -> None:
    user_sql = os.getenv("USER")
    database_sql = os.getenv("DATABASE")
    host_sql = os.getenv("HOST")
    password_sql = os.getenv("PASSWORD")

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
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM itsm.categoria"
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            logging.info(f'{len(rows)} linhas lidas de itsm.categoria')

        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(columns)
        writer.writerows(rows)

        now = datetime.now(timezone.utc)
        file_path = f"categoria/{now:%Y/%m/%d}/categoria_{now:%Y%m%d_%H%M%S}.csv"

        datalake = DataLakeServiceClient.from_connection_string(os.getenv("DATALAKE_CONNECTION_STRING"))
        file_client = datalake.get_file_system_client("bronze").get_file_client(file_path)
        file_client.upload_data(buffer.getvalue().encode("utf-8"), overwrite=True)

        logging.info(f'Arquivo gravado em bronze/{file_path}')

    except Exception as e:
        logging.error(f"Erro ao ler itsm.categoria: {str(e)}")
        raise


# csat_avaliacao e fila
# Primeira função - duda
@app.timer_trigger(
    schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False
)
def extract_csat_avaliacao(myTimer: func.TimerRequest) -> None:
    user_sql = os.getenv("USER")
    database_sql = os.getenv("DATABASE")
    host_sql = os.getenv("HOST")
    password_sql = os.getenv("PASSWORD")

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
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM itsm.csat_avaliacao"
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            logging.info(f'{len(rows)} linhas lidas de itsm.csat_avaliacao')

        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(columns)
        writer.writerows(rows)

        now = datetime.now(timezone.utc)
        file_path = f"csat_avaliacao/{now:%Y/%m/%d}/csat_avaliacao_{now:%Y%m%d_%H%M%S}.csv"

        datalake = DataLakeServiceClient.from_connection_string(os.getenv("DATALAKE_CONNECTION_STRING"))
        file_client = datalake.get_file_system_client("bronze").get_file_client(file_path)
        file_client.upload_data(buffer.getvalue().encode("utf-8"), overwrite=True)

        logging.info(f'Arquivo gravado em bronze/{file_path}')

    except Exception as e:
        logging.error(f"Erro ao ler itsm.csat_avaliacao: {str(e)}")
        raise


# Segunda função - duda
@app.timer_trigger(
    schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False
)
def extract_fila(myTimer: func.TimerRequest) -> None:
    user_sql = os.getenv("USER")
    database_sql = os.getenv("DATABASE")
    host_sql = os.getenv("HOST")
    password_sql = os.getenv("PASSWORD")

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
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM itsm.fila"
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            logging.info(f'{len(rows)} linhas lidas de itsm.fila')

        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(columns)
        writer.writerows(rows)

        now = datetime.now(timezone.utc)
        file_path = f"fila/{now:%Y/%m/%d}/fila_{now:%Y%m%d_%H%M%S}.csv"

        datalake = DataLakeServiceClient.from_connection_string(os.getenv("DATALAKE_CONNECTION_STRING"))
        file_client = datalake.get_file_system_client("bronze").get_file_client(file_path)
        file_client.upload_data(buffer.getvalue().encode("utf-8"), overwrite=True)

        logging.info(f'Arquivo gravado em bronze/{file_path}')

    except Exception as e:
        logging.error(f"Erro ao ler itsm.fila: {str(e)}")
        raise


# sla
@app.timer_trigger(
    schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False
)
def extract_sla(myTimer: func.TimerRequest) -> None:
    user_sql = os.getenv("USER")
    database_sql = os.getenv("DATABASE")
    host_sql = os.getenv("HOST")
    password_sql = os.getenv("PASSWORD")

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
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM itsm.sla"
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            logging.info(f'{len(rows)} linhas lidas de itsm.sla')

        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(columns)
        writer.writerows(rows)

        now = datetime.now(timezone.utc)
        file_path = f"sla/{now:%Y/%m/%d}/sla_{now:%Y%m%d_%H%M%S}.csv"

        datalake = DataLakeServiceClient.from_connection_string(os.getenv("DATALAKE_CONNECTION_STRING"))
        file_client = datalake.get_file_system_client("bronze").get_file_client(file_path)
        file_client.upload_data(buffer.getvalue().encode("utf-8"), overwrite=True)

        logging.info(f'Arquivo gravado em bronze/{file_path}')

    except Exception as e:
        logging.error(f"Erro ao ler itsm.sla: {str(e)}")
        raise


# solicitante
@app.timer_trigger(
    schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False
)
def extract_solicitante(myTimer: func.TimerRequest) -> None:
    user_sql = os.getenv("USER")
    database_sql = os.getenv("DATABASE")
    host_sql = os.getenv("HOST")
    password_sql = os.getenv("PASSWORD")

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
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM itsm.solicitante"
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            logging.info(f'{len(rows)} linhas lidas de itsm.solicitante')

        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(columns)
        writer.writerows(rows)

        now = datetime.now(timezone.utc)
        file_path = f"solicitante/{now:%Y/%m/%d}/solicitante_{now:%Y%m%d_%H%M%S}.csv"

        datalake = DataLakeServiceClient.from_connection_string(os.getenv("DATALAKE_CONNECTION_STRING"))
        file_client = datalake.get_file_system_client("bronze").get_file_client(file_path)
        file_client.upload_data(buffer.getvalue().encode("utf-8"), overwrite=True)

        logging.info(f'Arquivo gravado em bronze/{file_path}')

    except Exception as e:
        logging.error(f"Erro ao ler itsm.solicitante: {str(e)}")
        raise