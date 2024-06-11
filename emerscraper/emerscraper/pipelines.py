# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime

class EmerscraperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                adapter[field_name] = value[0].strip()


        date_string = adapter.get('date')
        adapter['date'] = datetime.strptime(date_string, '%d.%m.%Y').date()

        time_string = adapter.get('time')
        adapter['time'] = datetime.strptime(time_string, '%H:%M:%S').time()

        return item

import pandas as pd
from scrapy.exporters import CsvItemExporter
from generate_folium_map import generate_map

class CsvPipeline:
    def __init__(self):
        self.file = open('emersnow.csv', 'wb')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

        # Generate the Folium map after the CSV file is saved
        generate_map('emersnow.csv', 'index.html')

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
