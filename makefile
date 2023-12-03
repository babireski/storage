client:
	@python3 ./src/application.py client

server:
	@python3 ./src/application.py server

setup:
	@pip3 install -r requirements.txt

clean:
	@rm -rf ./src/__pycache__
