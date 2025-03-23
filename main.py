import argparse
from rss_generator import RSSGenerator
from data_sources.github_trending import GitHubTrending
from data_sources.infoq_trending import InfoQTrending

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
    parser.add_argument("-s", "--source", choices=["github", "infoq", "all"], 
                       default="github", help="Data source to use")
    args = parser.parse_args()
    
    # Process each data source separately
    for data_source, rss_config in get_data_sources(args.source):
        output_file = f"{rss_config['title'].lower().replace(' ', '_')}_rss_feed.xml"
        rss_gen = RSSGenerator(**rss_config)
        try:
            # Fetch data and generate RSS
            items = data_source.fetch_data()
            rss_feed = rss_gen.generate(items)
            
            # Save RSS to file
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(rss_feed)
            
            print(f"Successfully generated {output_file}")
            
        except Exception as e:
            print(f"Error processing {rss_config['title']}: {str(e)}")

if __name__ == "__main__":
    main()
