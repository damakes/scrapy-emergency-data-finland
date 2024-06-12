# scrapy-emergency-data-finland 
**Scrapy spider project for emergency & incident data collection of Finland.**

Visit the interactive map: [Scrapy Emergency Data Finland](https://damakes.github.io/scrapy-emergency-data-finland/) 🖱️  

Project Features

1. Scraping: crawl and scrape emergency and incident data from website.
    1. Tracking & blocking prevention: Integrated with [ScrapeOps](https://scrapeops.io/docs/intro/) API for user-agent & headers creation.
1. Cleaning: Scrapy Items and Item Pipelines to clean and structure the data.
1. Storage: Save the cleaned data into CSV files for further analysis.
1. Visualization: Geographical distribution of incidents using [Folium maps](https://python-visualization.github.io/folium/latest/user_guide.html).
