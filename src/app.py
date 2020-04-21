import json
from datetime import datetime
from time import sleep
from typing import Tuple
from selenium.webdriver import Firefox

import requests
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options

from utils import get_environment_variable
from dotenv import load_dotenv

load_dotenv()
HEADERS = {"User-Agent": "github.com/anubhavcodes/socialkarma"}


def get_twitter_followers(twitter_handle: str) -> str:
    url: str = f"https://mobile.twitter.com/{twitter_handle}"
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")
    followers: str = soup.find("a", {"href": f"/{twitter_handle}/followers"}).text.strip(" Followers \n")
    return followers


def get_stackoverflow_followers(stack_overflow_handle: str) -> Tuple[str, str]:
    url = f"https://stackoverflow.com/users/{stack_overflow_handle}"
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")
    stack_overflow_reputation = soup.find("div", {"title": "reputation"}).text.strip("\n").split("\n")[0]
    stack_overflow_profile_views = soup.findAll("li", {"class": "ow-break-word"})[5].text.strip("\n").split(" ")[0]
    return stack_overflow_reputation, stack_overflow_profile_views


def get_keybase_followers(keybase_handle: str) -> str:
    url: str = f"https://keybase.io/{keybase_handle}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    followers: str = soup.findAll("h4")[1].text.strip("Followers ").strip("(").strip(")")
    return followers


def get_linkedin_views(username: str, password: str, profile_handle: str) -> Tuple[str, str, str, str, str]:
    opts = Options()
    opts.headless = False
    browser = Firefox(options=opts)
    browser.get("https://linkedin.com/login")
    browser.find_element_by_name("session_key").send_keys(username)
    browser.find_element_by_name("session_password").send_keys(password)
    browser.find_element_by_tag_name("button").click()
    browser.get(f"https://www.linkedin.com/{profile_handle}")
    sleep(2)
    post_views = browser.find_element_by_class_name("update-views").text.split("\n")[0]
    profile_views = browser.find_element_by_class_name("profile-views").text.split("\n")[0]
    search_appearances = browser.find_element_by_class_name("search-appearances").text.split("\n")[0]
    followers = browser.find_element_by_class_name("pv-recent-activity-section__follower-count").text.split(" ")[0]
    sleep(2)
    browser.get("https://www.linkedin.com/mynetwork/")
    connections = browser.find_element_by_css_selector("#ember1193 > div:nth-child(1) > div:nth-child(2)").text
    return profile_views, post_views, search_appearances, followers, connections


def get_github_stats(github_username: str) -> Tuple[str, str]:
    r = requests.get(f"https://github.com/{github_username}", headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")
    followers = soup.find("a", {"href": f"/{github_username}?tab=followers"}).text.strip("followers\n").strip()
    following = soup.find("a", {"href": f"/{github_username}?tab=following"}).text.strip("following\n").strip()
    return followers, following


def run():
    print("running socialkarma")
    twitter_handle = get_environment_variable("TWITTER_HANDLE")
    keybase_handle = get_environment_variable("KEYBASE_HANDLE")
    linkedin_username = get_environment_variable("LINKEDIN_USERNAME")
    linkedin_password = get_environment_variable("LINKEDIN_PASSWORD")
    linkedin_profile_handle = get_environment_variable("LINKEDIN_PROFILE_HANDLE")
    github_username = get_environment_variable("GITHUB_USERNAME")
    stackoverflow_handle = get_environment_variable("STACKOVERFLOW_HANDLE")
    sentry_dns = get_environment_variable("SENTRY_DSN")

    if sentry_dns:
        import sentry_sdk

        sentry_sdk.init(sentry_dns)

    result = []
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    try:
        print("getting twitter followers")
        twitter_followers = get_twitter_followers(twitter_handle)
        result.append({"type": "twitter", "timestamp": timestamp, "twitter_followers": twitter_followers})
        keybase_followers = get_keybase_followers(keybase_handle)
        result.append({"type": "keybase", "timestamp": timestamp, "keybase_followers": keybase_followers})
        github_followers, github_following = get_github_stats(github_username)
        result.append(
            {
                "type": "github",
                "timestamp": timestamp,
                "github_followers": github_followers,
                "github_following": github_following,
            }
        )
        stackoverflow_reputation, stackoverflow_profile_views = get_stackoverflow_followers(stackoverflow_handle)
        result.append(
            {
                "type": "stackoverflow",
                "timestamp": timestamp,
                "stackoverflow_reputation": stackoverflow_reputation,
                "stackoverflow_profile_views": stackoverflow_profile_views,
            }
        )
        linkedin_profile_views, linkedin_post_views, linkedin_search_appearances, linkedin_followers, linkedin_connections = get_linkedin_views(
            linkedin_username, linkedin_password, linkedin_profile_handle
        )
        result.append(
            {
                "type": "linkedin",
                "timestamp": timestamp,
                "linkedin_profile_views": linkedin_profile_views,
                "linkedin_post_views": linkedin_post_views,
                "linkedin_search_appearances": linkedin_search_appearances,
                "linkedin_followers": linkedin_followers,
                "linkedin_connections": linkedin_connections,
            }
        )
    except KeyError as e:
        result.append({"timestamp": timestamp, "error": str(e)})
    print(json.dumps(result))


if __name__ == "__main__":
    run()
