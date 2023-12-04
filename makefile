PYTHON = python
PIP = pip

client:
	@$(PYTHON) ./src/application.py client --path client-test-data

server:
	@$(PYTHON) ./src/application.py server --path server-test-data

setup:
	@$(PIP) install -r requirements.txt

clean:
	@rm -rf ./src/__pycache__

build:
	@pyinstaller --distpath ./bin/ --name storage --onefile ./src/application.py
	@rm -rf ./build
	@rm storage.spec

install:
	@sudo install ./bin/storage /usr/bin/