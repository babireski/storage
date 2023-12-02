client:
	@python3 ./src/application.py client --port 40000

server:
	@python3 ./src/application.py server --port 40000

setup:
	@pip install -r requirements.txt

clean:
	@rm -rf ./src/__pycache__
