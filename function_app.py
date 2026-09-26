import logging
import azure.functions as func
import os
import urllib.request
import urllib.parse

app = func.FunctionApp()

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