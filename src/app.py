import requests
from bs4 import BeautifulSoup
from sys import argv


def get_followers(twitter_handle: str) -> str:
    url: str = f"https://twitter.com/{twitter_handle}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    followers: str = soup.find("a", {"href": f"/{twitter_handle}/followers"}).findAll("span")[-1].attrs["data-count"]
    return followers


if __name__ == '__main__':
    print(get_followers(argv[-1]))
