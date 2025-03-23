from datetime import datetime, timezone
from xml.etree import ElementTree as ET
from xml.dom import minidom

class RSSGenerator:
    def __init__(self, title, description, link):
        self.title = title
        self.description = description
        self.link = link

    def generate(self, items):
        """Generate RSS feed from items"""
        rss = ET.Element("rss", version="2.0")
        channel = ET.SubElement(rss, "channel")
        
        ET.SubElement(channel, "title").text = self.title
        ET.SubElement(channel, "description").text = self.description
        ET.SubElement(channel, "link").text = self.link
        ET.SubElement(channel, "lastBuildDate").text = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
        
        for item in items:
            self._add_item(channel, item)
        
        xml_str = ET.tostring(rss, encoding="utf-8", method="xml")
        return minidom.parseString(xml_str).toprettyxml(indent="  ")

    def _add_item(self, channel, item):
        """Add individual item to RSS channel"""
        rss_item = ET.SubElement(channel, "item")
        ET.SubElement(rss_item, "title").text = item.get("title", "")
        ET.SubElement(rss_item, "link").text = item.get("link", "")
        ET.SubElement(rss_item, "description").text = item.get("description", "")
        ET.SubElement(rss_item, "pubDate").text = item.get("pub_date", "")
