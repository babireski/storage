PYTHON = python
PIP = pip

client:
	@$(PYTHON) ./src/application.py client --path client-test-data --host 192.168.15.20

server:
	@$(PYTHON) ./src/application.py server --path stg

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

test:
	@$(PYTHON) ./src/tester.py