import copy
import os
import time

import emoji
import requests
from bs4 import BeautifulSoup

from .utils import load_json, save_json, setup_logger, discord_push

# NXBrew variables
LATEST_ADDED_ID = "tab-recent-6"
LATEST_UPDATED_ID = "custom_html-6"

# Pull in environment variables
NXBREW_URL = os.getenv("NXBREW_URL", None)

CONFIG_DIR = os.getenv("CONFIG_DIR", os.getcwd())

DISCORD_URL = os.getenv("NXBREW_DISCORD_URL", None)

CADENCE = os.getenv("NXBREW_CADENCE", "1")
CADENCE = int(CADENCE) * 60

LOG_LEVEL = os.getenv("NXBREW_LOG_LEVEL", "INFO")


def get_soup(url):
    """Scrape URL, soupify

    Args:
        url: URL to scrape
    """

    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    return soup


def get_emoji_free_text(text):
    """Remove emoji from a string

    Args:
        text: String to remove emoji from
    """

    allchars = [s for s in text]
    emoji_list = [c for c in allchars if c in emoji.EMOJI_DATA]
    clean_text = ' '.join([s for s in text.split() if s not in emoji_list])

    return clean_text


class NXBrewWatcher:

    def __init__(
            self,
    ):
        """Scrape NXBrew for latest additions and updates"""

        if NXBREW_URL is None:
            raise ValueError("NXBREW_URL environment variable must be set")

        self.cache_file = os.path.join(CONFIG_DIR, "nxbrew_cache.json")
        if os.path.exists(self.cache_file):
            self.cache = load_json(self.cache_file)
        else:
            self.cache = {"added": {}, "updated": {}}

        log_dir = os.path.join(CONFIG_DIR, "logs")
        logger = setup_logger(
            log_level=LOG_LEVEL,
            script_name="nxbrew_watcher",
            log_dir=log_dir,
        )
        self.logger = logger

    def run(self):
        """Run the watcher"""

        while True:
            # Scrape the website
            soup = get_soup(NXBREW_URL)

            # First, scrape and cache latest added
            self.scrape_latest_added(soup)

            # Then, scrape latest updates
            self.scrape_latest_updated(soup)

            # Save out the cache
            save_json(self.cache, self.cache_file)

            # Wait until the next run
            self.logger.info(f"Run complete, next run in {CADENCE}s")
            time.sleep(CADENCE)

    def scrape_latest_added(self,
                            soup,
                            ):
        """Look at latest added, and print out any not in the cache

        Args:
            soup: BeautifulSoup object
        """

        self.logger.info("Scraping latest added:")

        results = soup.find(id=LATEST_ADDED_ID)

        # Step backwards so the newest is last
        for item in results.find_all('li',
                                     )[::-1]:

            # Get title out of the tab-item-title
            item_title = item.find("p",
                                   attrs={'class': 'tab-item-title'},
                                   )

            # Get thumbnail from tab-item-thumbnail
            item_thumb = item.find("div",
                                   attrs={'class': 'tab-item-thumbnail'},
                                   )

            # Get title from text
            title = copy.deepcopy(item_title.text)

            # # Get href from the "a" tag
            url = item_title.find("a").get("href")

            # Get a thumbnail from img
            thumb = item_thumb.find("img").get("src")

            if title not in self.cache["added"]:

                self.logger.info(f"-> Found {title}, adding to cache")
                self.cache["added"][title] = url

                # Push to discord, if we're doing that
                if DISCORD_URL is not None:
                    embeds = [
                        {
                            "author": {
                                "name": "Added",
                                "url": "https://github.com/bbtufty/nxbrew-watcher",
                            },
                            "title": title,
                            "description": url,
                            "thumbnail": {"url": thumb},
                        }
                    ]

                    discord_push(
                        url=DISCORD_URL,
                        embeds=embeds,
                    )

        return True

    def scrape_latest_updated(self,
                            soup,
                            ):
        """Look at latest updated, and print out any not in the cache

        Args:
            soup: BeautifulSoup object
        """

        self.logger.info("Scraping latest updated:")

        results = soup.find(id=LATEST_UPDATED_ID)

        # Step backwards so the newest is last
        for item in results.find_all('a',
                                     )[::-1]:

            # Clean out the tick emoji and any extraneous whitespace
            title = get_emoji_free_text(item.text).strip()
            url = item.get("href")

            if title not in self.cache["updated"]:

                self.logger.info(f"-> Found {title}, adding to cache")
                self.cache["updated"][title] = url

                # Push to discord, if we're doing that
                if DISCORD_URL is not None:
                    embeds = [
                        {
                            "author": {
                                "name": "Updated",
                                "url": "https://github.com/bbtufty/nxbrew-watcher",
                            },
                            "title": title,
                            "description": url,
                        }
                    ]

                    discord_push(
                        url=DISCORD_URL,
                        embeds=embeds,
                    )

        return True
