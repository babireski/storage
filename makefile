client:
	@python ./src/application.py client

server:
	@python ./src/application.py server --path ../files

setup:
	@pip install -r requirements.txt

clean:
	@rm -rf ./src/__pycache__