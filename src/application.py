import typer

application = typer.Typer()

@application.command()
def hello(name):
    print('Hello, {}!'.format(name))

@application.command()
def goodbye(name):
    print('Goodbye, {}!'.format(name))

application()