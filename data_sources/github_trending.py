import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from . import DataSource

class GitHubTrending(DataSource):
    def __init__(self, language="", since="daily"):
        self.language = language
        self.since = since
        
    def fetch_data(self):
        """Fetch trending repositories from GitHub"""
        url = self._build_url()
        headers = self._get_headers()
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch trending data: {str(e)}")
            
        return self._parse_response(response.text)
        
    def _build_url(self):
        """Build the GitHub Trending URL"""
        url = "https://github.com/trending"
        if self.language:
            url += f"/{self.language}"
        url += f"?since={self.since}"
        return url
        
    def _get_headers(self):
        """Get request headers"""
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        
    def _parse_response(self, html):
        """Parse the HTML response"""
        soup = BeautifulSoup(html, 'html.parser')
        items = []
        
        for article in soup.find_all('article', class_='Box-row'):
            item = {
                'title': self._extract_title(article),
                'link': self._extract_link(article),
                'description': self._extract_description(article),
                'pub_date': self._extract_pub_date(article)
            }
            items.append(item)
        return items
        
    def _extract_title(self, article):
        """Extract repository title"""
        title = article.find('h2', class_='h3')
        return title.text.strip().replace('\n', '').replace(' ', '') if title else ''
        
    def _extract_link(self, article):
        """Extract repository link"""
        title = article.find('h2', class_='h3')
        return "https://github.com" + title.find('a')['href'] if title and title.find('a') else ''
        
    def _extract_description(self, article):
        """Extract repository description"""
        description = article.find('p', class_='col-9')
        return description.text.strip() if description else ''
        
    def _extract_pub_date(self, article):
        """Extract repository publish date"""
        time_element = article.find('relative-time')
        if time_element and 'datetime' in time_element.attrs:
            return datetime.fromisoformat(time_element['datetime']).strftime("%a, %d %b %Y %H:%M:%S GMT")
        return datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
