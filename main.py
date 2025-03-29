import argparse
import os
import traceback
from rss_generator import RSSGenerator
from datasource.github import GitHubTrending
from datasource.infoq import InfoQTrending
from datasource.hackernews import HackerNewsDataSource

def get_data_sources(source):
    """Get data sources based on input"""
    sources = {
        "github": (GitHubTrending(), {
            "title": "GitHub Trending",
            "description": "Daily trending repositories on GitHub",
            "link": "https://github.com/trending"
        }),
        "infoq": (InfoQTrending(), {
            "title": "InfoQ Trending",
            "description": "Trending news from InfoQ",
            "link": "https://www.infoq.cn/hotlist"
        }),
        "hacknews": (HackerNewsDataSource(), {
            "title": "Hacker News",
            "description": "Top stories from Hacker News",
            "link": "https://news.ycombinator.com/"
        })
    }
    
    if source == "all":
        return sources.values()
    elif source in sources:
        return [sources[source]]
    else:
        raise ValueError(f"Unknown data source: {source}")

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Generate RSS feed from various sources")
    parser.add_argument("-s", "--source", choices=["github", "infoq", "hacknews", "all"], 
                       default="all", help="Data source to use")
    parser.add_argument("-o", "--output", default="outputs", 
                       help="Output directory for RSS files")
    args = parser.parse_args()
    
    # Process each data source separately
    for data_source, rss_config in get_data_sources(args.source):
        output_file = f"{rss_config['title'].lower().replace(' ', '_')}_rss_feed.xml"
        rss_gen = RSSGenerator(**rss_config)
         # Fetch data and generate RSS
        items = data_source.fetch_data()
        try:
            rss_feed = rss_gen.generate(items)
            
            # Save RSS to file
            output_path = os.path.join(args.output, output_file)
            os.makedirs(args.output, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(rss_feed)
            
            print(f"Successfully generated {output_file}")
            
        except Exception as e:
            print(f"Error processing {rss_config['title']}: {str(e)}")
            traceback.print_exc()

if __name__ == "__main__":
    main()
