client:
	@python ./src/application.py client

server:
	@python ./src/application.py server

setup:
	@pip install -r requirements.txt

clean:
	@rm -rf ./src/__pycache__