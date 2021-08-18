import scrapy
from scrapy_splash import SplashRequest

script = """
function main(splash)
    local num_scrolls = 10
    local scroll_delay = 1.0

    local scroll_to = splash:jsfunc("window.scrollTo")
    local get_body_height = splash:jsfunc(
        "function() {return document.body.scrollHeight;}"
    )
    assert(splash:go(splash.args.url))
    splash:wait(splash.args.wait)

    for _ = 1, num_scrolls do
        scroll_to(0, get_body_height())
        splash:wait(scroll_delay)
    end        
    return splash:html()
end
"""

class ReutersSpider(scrapy.Spider):
    name = 'reuters'

    def start_requests(self):
        url = 'https://www.reuters.com/'
        ticker = getattr(self, 'ticker', None) 
        exchange = getattr(self, 'exchange', None) 
        tag = getattr(self, 'tag', None) 
        
        if ticker is not None:
            if exchange  is not None:
                if tag  is not None:
                    exchange_dict = {'NASDAQ' : 'O'}
                    url = url + 'companies/' + ticker + '.' + exchange_dict[exchange] + '/' + tag

        yield SplashRequest(url,
                            self.parse,
                            endpoint='execute', 
                            args={'wait':2, 'lua_source': script}
                            )

    def parse(self, response):
        base_selectors = response.xpath('//a[contains(@class, "MarketStoryItem")]')
        for selector in base_selectors:
            link = selector.xpath('@href').extract()[0]
            yield scrapy.Request(link, self.parse_tag)

    def parse_tag(self, response):
        title_selector = response.xpath('//h1[contains(@class, "Text__text")]')
        title = title_selector.xpath('text()').extract()[0]
        text_selectors = response.xpath('//p[contains(@class, "Text__text")]')
        text = text_selectors.xpath('text()').extract()
        text = ' '.join(text)
        date_selector = response.xpath('//time/span')
        date = date_selector.xpath('text()').extract()[0]
        time = date_selector.xpath('text()').extract()[1]

        yield {
            'title': title,
            'text': text,
            'date': date,
            'time': time,
        }
