import requests
from bs4 import BeautifulSoup
from . import DataSource

class HackerNewsDataSource(DataSource):
    """Data source implementation for Hacker News"""

    def fetch_data(self):
        """Fetch and parse data from Hacker News, return in RSS format"""
        url = "https://news.ycombinator.com"
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        items = []

        for item in soup.select(".athing"):
            title = item.select_one(".titleline a").text
            link = item.select_one(".titleline a")["href"]
            items.append({
                "title": title,
                "link": link,
                "description": title,
                "pubDate": "",
            })



        return items
