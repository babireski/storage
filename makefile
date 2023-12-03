client:
	@python ./src/application.py client

server:
	@python ./src/application.py server

setup:
	@pip install -r requirements.txt

clean:
	@rm -rf ./src/__pycache__

build:
	@pyinstaller --distpath ./bin/ --name storage --onefile ./src/application.py
	@rm -rf ./build
	@rm storage.spec