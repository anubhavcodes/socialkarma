from datetime import datetime
from random import randint
from time import sleep
from typing import Dict
import attr

import requests
from bs4 import BeautifulSoup


class Source:
    HEADERS = {f"User-Agent": "socialkarma"}
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def get_stats(self) -> Dict:
        raise NotImplementedError


@attr.s
class SourceWithID(Source):

    id: str = attr.ib()

    def get_stats(self) -> Dict:
        raise NotImplementedError


@attr.s
class SourceWithCredentials(Source):

    username: str = attr.ib()
    password: str = attr.ib()
    id: str = attr.ib(default=None)

    def get_stats(self) -> Dict:
        raise NotImplementedError


class TwitterSource(SourceWithID):
    def get_stats(self) -> Dict:
        url: str = f"https://mobile.twitter.com/{self.id}"
        r = requests.get(url, headers=self.HEADERS)
        soup = BeautifulSoup(r.text, "html.parser")
        followers: str = soup.find("a", {"href": f"/{self.id}/followers"}).text.strip(" Followers \n")
        following: str = soup.find("a", {"href": f"/{self.id}/following"}).text.strip(" Following \n")
        return {"timestamp": self.timestamp, "followers": followers, "following": following}


class StackOverflowSource(SourceWithID):
    def get_stats(self) -> Dict:
        url = f"https://stackoverflow.com/users/{self.id}"
        r = requests.get(url, headers=self.HEADERS)
        soup = BeautifulSoup(r.text, "html.parser")
        reputation = soup.find("div", {"title": "reputation"}).text.strip("\n").split("\n")[0]
        profile_views = soup.findAll("li", {"class": "ow-break-word"})[5].text.strip("\n").split(" ")[0]
        return {"timestamp": self.timestamp, "reputation": reputation, "profile_views": profile_views}


class KeybaseSource(SourceWithID):
    def get_stats(self):
        url: str = f"https://keybase.io/{self.id}"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        followers: str = soup.findAll("h4")[1].text.strip("Followers ").strip("(").strip(")")
        following: str = soup.findAll("h4")[0].text.strip("Following ").strip("(").strip(")")
        return {"timestamp": self.timestamp, "followers": followers, "following": following}


class LinkedInSource(SourceWithCredentials):
    def get_stats(self) -> Dict:
        from selenium.webdriver.firefox.options import Options
        from selenium.webdriver import Firefox

        opts = Options()
        opts.headless = False
        browser = Firefox(options=opts)
        browser.get("https://linkedin.com/login")
        browser.find_element_by_name("session_key").send_keys(self.username)
        browser.find_element_by_name("session_password").send_keys(self.password)
        browser.find_element_by_tag_name("button").click()
        browser.get(f"https://www.linkedin.com/{self.id}")
        sleep(randint(2, 5))
        post_views = browser.find_element_by_class_name("update-views").text.split("\n")[0]
        profile_views = browser.find_element_by_class_name("profile-views").text.split("\n")[0]
        search_appearances = browser.find_element_by_class_name("search-appearances").text.split("\n")[0]
        followers = browser.find_element_by_class_name("pv-recent-activity-section__follower-count").text.split(" ")[0]
        sleep(randint(2, 5))
        browser.get("https://www.linkedin.com/mynetwork/")
        connections = browser.find_element_by_css_selector("#ember1193 > div:nth-child(1) > div:nth-child(2)").text
        return {
            "timestamp": self.timestamp,
            "profile_views": profile_views,
            "post_views": post_views,
            "search_appearances": search_appearances,
            "followers": followers,
            "connections": connections,
        }


class GithubSource(SourceWithID):
    def get_stats(self) -> Dict:
        r = requests.get(f"https://github.com/{self.id}", headers=self.HEADERS)
        soup = BeautifulSoup(r.text, "html.parser")
        followers = soup.find("a", {"href": f"/{self.id}?tab=followers"}).text.strip("followers\n").strip()
        following = soup.find("a", {"href": f"/{self.id}?tab=following"}).text.strip("following\n").strip()
        return {"timestamp": self.timestamp, "followers": followers, "following": following}
