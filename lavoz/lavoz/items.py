"""Items."""
import scrapy


class LaVozItem(scrapy.Item):
    """LaVoz Item."""
    url = scrapy.Field()
    barrio = scrapy.Field()
    direccion = scrapy.Field()
    descripcion = scrapy.Field()
    alquiler = scrapy.Field()
    expensas = scrapy.Field()
    imagenes = scrapy.Field()
    atributos = scrapy.Field()
