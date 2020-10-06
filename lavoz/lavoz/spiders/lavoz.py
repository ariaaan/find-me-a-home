"""LaVoz spider."""
import scrapy
from lavoz.items import LaVozItem


class LaVozSpider(scrapy.Spider):
    name = "lavoz"

    def start_requests(self):
        urls_dict = {
            'cofico': (
                'https://clasificados.lavoz.com.ar/'
                'inmuebles/departamentos/alquileres/'
                '1-dormitorio?ciudad=cordoba'
                '&provincia=cordoba&barrio[0]=cofico'
            ),
            'alta-cordoba': (
                'https://clasificados.lavoz.com.ar/'
                'inmuebles/departamentos/alquileres/'
                '1-dormitorio?ciudad=cordoba'
                '&provincia=cordoba&barrio[0]=alta-cordoba'
            ),
            'general-paz': (
                'https://clasificados.lavoz.com.ar/'
                'inmuebles/departamentos/alquileres/'
                '1-dormitorio?ciudad=cordoba'
                '&provincia=cordoba&barrio[0]=general-paz'
            ),
        }

        for barrio, url in urls_dict.items():
            request = scrapy.Request(
                url=url,
                callback=self.parse_pages
            )

            request.meta['barrio'] = barrio

            yield request

    def parse_pages(self, response):
        page_number = response.request.meta.get('page_number', 1)

        listing_urls = response.xpath(
            '//div[contains(@class, "safari-card")]'
            '/a[@class="text-decoration-none"]/@href'
        ).extract()

        self.log(f'Parsing results of page {page_number}')

        barrio = response.request.meta['barrio']

        for listing_url in listing_urls:
            item = LaVozItem()
            item['barrio'] = barrio
            item['url'] = listing_url

            request = scrapy.Request(
                url=listing_url,
                callback=self.parse_item
            )

            request.meta['item'] = item

            yield request

        next_page_url = response.xpath(
            '//a[@class="right button-narrow"]/@href'
        ).extract_first()

        if next_page_url:
            request = scrapy.Request(
                url=next_page_url,
                callback=self.parse_pages
            )

            request.meta['barrio'] = barrio
            request.meta['page_number'] = page_number + 1

            yield request

    def parse_item(self, response):
        item = response.request.meta['item']

        alquiler = response.xpath(
            '//div[@class="h2 mt0 main bolder"]/text()'
        ).extract_first()

        item['alquiler'] = alquiler.strip() if alquiler else None

        direccion = response.xpath(
            '//p[@class="h4 bolder m0"]/text()'
        ).extract_first()

        item['direccion'] = (
            direccion.strip().title() if direccion else None
        )

        expensas = response.xpath(
            '//h3[@class=" h4 mt0 main bolder"]/text()'
        ).extract_first()

        item['expensas'] = expensas.strip().split()[-1] if expensas else None

        item['descripcion'] = (
            '\n'.join(
                [
                    p.strip() for p in response.xpath(
                        '//div[@class="container px1 md-px0 h4 "]//text()'
                    ).extract()
                ]
            )
        )

        item['imagenes'] = response.xpath(
            '//div[@id="camera"]//amp-carousel[@type="slides"]//amp-img/@src'
        ).extract()

        attribute_sections = response.xpath('//div[@class="clearfix px2"]')
        atributos = {}

        for section in attribute_sections:
            title = section.xpath('./p/text()').extract_first()

            items = [
                item.strip() for item in section.xpath(
                    './/ul/li/text()'
                ).extract()
            ]

            atributos[title] = items

        item['atributos'] = atributos

        return item
