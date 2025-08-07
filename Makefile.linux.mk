
venv:
	@if [ ! -d .venv ]; then \
		echo "Creating virtual environment..."; \
		python3 -m venv .venv; \
	else \
		echo "Virtual environment already exists."; \
	fi

req: requirements.txt
	@.venv/bin/pip install -r requirements.txt

setup:	setup.py
	@.venv/bin/pip install .

kick:
	@.venv/bin/ahustle --help

init:
	@make venv
	@make setup
	@echo "====================="
	@echo "=========USAGE======="
	@echo "====================="
	@make kick
