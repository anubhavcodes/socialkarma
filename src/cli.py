import click

from service import process_source, SOURCES


@click.command()
@click.option("--id", required=True, help="id of the source")
@click.option("--username", required=False, default=None, help="username of the source")
@click.option("--password", required=False, default=None, help="password of the source")
@click.option("--mongo-url", required=False, default="mongo://localhost:27107")
@click.option("--db", required=False, default="socialkarma")
@click.option("--quite/--no-quite", default=False)
@click.argument("source", type=click.Choice(SOURCES.keys()))
def run(id, username, password, mongo_url, db, quite, source):
    process_source(source, id, mongo_url, db, username, password, quite)


if __name__ == "__main__":
    run()
