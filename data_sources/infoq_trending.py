from bs4 import BeautifulSoup
from datetime import datetime, timezone
from playwright.sync_api import sync_playwright
from . import DataSource

class InfoQTrending(DataSource):
    def fetch_data(self):
        """Fetch trending news from InfoQ homepage using Playwright"""
        url = "https://www.infoq.cn/hotlist"
        
        with sync_playwright() as p:
            # Configure browser with additional options
            browser = p.chromium.launch(
                headless=True,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                    '--no-sandbox'
                ]
            )
            
            # Create new context with custom user agent
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                viewport={'width': 1280, 'height': 800}
            )
            page = context.new_page()
            
            # Intercept JavaScript requests
            page.route('**/*.js', lambda route: route.continue_())
            
            try:
                # Configure page to mimic real user
                page.set_viewport_size({"width": 1280, "height": 800})
                
                # Navigate with retry logic
                max_retries = 3
                retry_count = 0
                
                while retry_count < max_retries:
                    try:
                        page.goto(url, timeout=30000)
                        
                        # Scroll page to trigger lazy loading
                        page.mouse.wheel(0, 500)
                        page.wait_for_timeout(1000)
                        page.mouse.wheel(0, 500)
                        
                        # Wait for content with longer timeout
                        page.wait_for_selector('.item-main', timeout=30000)
                        break
                    except Exception as e:
                        retry_count += 1
                        if retry_count == max_retries:
                            raise Exception(f"Failed to load page after {max_retries} attempts: {str(e)}")
                        page.wait_for_timeout(5000)  # Wait before retry
                
                # Take screenshot for debugging
                # page.screenshot(path='infoq_screenshot.png', full_page=True)
                
                content = page.content()
                return self._parse_response(content)
            except Exception as e:
                # Capture screenshot on error
                raise Exception(f"Failed to fetch InfoQ data: {str(e)}")
            finally:
                browser.close()

    def _parse_response(self, html):
        """Parse the HTML response"""
        soup = BeautifulSoup(html, 'html.parser')
        items = []
        
        # Find all article containers
        articles = soup.select('.item-main')
        
        for article in articles:
            # Extract title
            title = article.select_one('.com-article-title span')
            if not title:
                continue
                
            # Extract link
            link = article.select_one('.com-article-title')
            if not link or not link.get('href'):
                continue
                
            # Extract description
            description = article.select_one('.summary')
            
            # Extract date
            date_element = article.select_one('.date')
            pub_date = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
            if date_element:
                try:
                    pub_date = datetime.strptime(date_element.text.strip(), "%Y-%m-%d").strftime("%a, %d %b %Y %H:%M:%S GMT")
                except ValueError:
                    pass
            
            items.append({
                'title': title.text.strip(),
                'link': "https://www.infoq.cn" + link['href'],
                'description': description.text.strip() if description else '',
                'pub_date': pub_date
            })
            
        return items
