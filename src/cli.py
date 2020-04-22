import click

from service import process_source, SOURCES


@click.command()
@click.option("--id", required=True, help="id of the source")
@click.option("--username", required=False, default=None, help="username of the source")
@click.option("--password", required=False, default=None, help="password of the source")
@click.option("--host", required=True, default="localhost", help="host of mongo instance")
@click.option("--port", required=True, default=27017, help="port number of the mongo instance")
@click.option("--db", required=True, default="stats", help="db to use for mongo instance")
@click.argument("source", type=click.Choice(SOURCES.keys()))
def run(id, username, password, host, port, db, source):
    print(f"Mongo called with {host}:{port}")
    process_source(source, id, host, port, db, username, password)


if __name__ == "__main__":
    run()
