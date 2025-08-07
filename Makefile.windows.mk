venv:
	@if not exist .venv ( \
		echo Creating virtual environment... && \
		python -m venv .venv \
	) else ( \
		echo Virtual environment already exists. \
	)

req: requirements.txt
	@.venv\Scripts\pip install -r requirements.txt

setup: setup.py
	@.venv\Scripts\pip install .

kick:
	@.venv\Scripts\ahustle --help

init:
	@make venv
	@make setup
	@echo =====================
	@echo ======= USAGE =======
	@echo =====================
	@make kick
