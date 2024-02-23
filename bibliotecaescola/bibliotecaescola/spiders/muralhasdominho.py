import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import os
import json

class MuralhasDomInhoSpider(CrawlSpider):
    name = 'muralhasdominho'
    allowed_domains = ['biblioteca.muralhasdominho.com']
    start_urls = ['http://biblioteca.muralhasdominho.com']

    rules = (
        Rule(LinkExtractor(allow=('/')), callback='parse_page', follow=True),
    )

    def __init__(self, *args, **kwargs):
        super(MuralhasDomInhoSpider, self).__init__(*args, **kwargs)
        json_filename = os.path.join('muralhasdominho_content', 'muralhasdominho_text.json')
        
        # Clear the content of the JSON file and add an opening square bracket at the beginning
        with open(json_filename, 'w', encoding='utf-8') as json_file:
            json_file.write('[\n')

        self.log(f'Arquivo JSON {json_filename} inicializado.')

    def parse_page(self, response):
        all_text = ' '.join(response.css('body ::text').extract())
        title = response.css('title::text').get()
        link = response.url
        current_page = response.url.split('/')[-1]

        data = {'title': title, 'text': all_text, 'link': link}

        json_filename = os.path.join('muralhasdominho_content', 'muralhasdominho_text.json')
        with open(json_filename, 'a', encoding='utf-8') as json_file:
            json_file.write(',\n' if os.path.getsize(json_filename) > 8 else '')  # Add a comma if not the first entry
            json.dump(data, json_file, ensure_ascii=False, indent=4)

        self.log(f'Título, texto e link da página {current_page} adicionados ao arquivo JSON: {json_filename}')

    def closed(self, reason):
        json_filename = os.path.join('muralhasdominho_content', 'muralhasdominho_text.json')

        # Add a closing square bracket at the end of the JSON file
        with open(json_filename, 'a', encoding='utf-8') as json_file:
            json_file.write('\n]')

        self.log(f'Arquivo JSON {json_filename} finalizado.')

# Rest of your Scrapy settings and configurations
