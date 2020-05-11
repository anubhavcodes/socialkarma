from pprint import pprint
from typing import Dict

from pymongo import MongoClient

from core import TwitterSource, StackOverflowSource, KeybaseSource, LinkedInSource, GithubSource, SourceWithID

SOURCES = {
    "twitter": TwitterSource,
    "stackoverflow": StackOverflowSource,
    "keybase": KeybaseSource,
    "linkedin": LinkedInSource,
    "github": GithubSource,
}


def write_to_db(host: str, port: int, db: str, collection: str, document: Dict):
    print(f"Writing to mongo on {host}:{port}\n{document}")
    client = MongoClient(host=host, port=port)
    db = client[db]
    collection = db[collection]
    collection.insert_one(document=document)


def get_stats(source: str, id: str, username: str = None, password: str = None) -> Dict:
    if source == "linkedin":  # @TODO think of a better solution
        s: LinkedInSource = SOURCES["source"](id=id, username=username, password=password)  # noqa
    else:
        s: SourceWithID = SOURCES[source](id=id)  # noqa
    return s.get_stats()


def process_source(
    source: str, id: str, host: str, port: int, db: str, username: str = None, password: str = None, quite=False
):
    print(f"Processing {source}")
    stats = get_stats(source, id, username, password)
    if not quite:
        write_to_db(host=host, port=port, db=db, collection=source, document=stats)
    else:
        pprint(stats)
