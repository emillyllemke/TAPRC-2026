# TAPRC-2026
Repositório destinado ao trabalho de Tópicos Avançados em Programação.

## Timer Trigger

Esta aplicacao usa Python com o modelo v2 do Azure Functions. A funcao `timer_trigger` e executada a cada 5 minutos por padrao.

### Executar localmente

1. Crie e ative um ambiente virtual:

	```powershell
	py -m venv .venv
	.\.venv\Scripts\Activate.ps1
	```

2. Instale as dependencias:

	```powershell
	python -m pip install -r requirements.txt
	```

3. Inicie o host local:

	```powershell
	func start
	```

O intervalo pode ser alterado pela configuracao `TIMER_SCHEDULE` em `local.settings.json`, usando o formato CRON de seis campos do Azure Functions.
