import scrapy


class RugbypassSpider(scrapy.Spider):
    name = 'rugbypass'

    def start_requests(self):
        url = 'https://www.rugbypass.com/results/'

        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        base_selectors = response.xpath('//a[contains(@class, "link-box")]')
        for selector in base_selectors:
            link = selector.xpath('@href').extract()[0]
            yield scrapy.Request(link, self.parse_match)
        # for link in
        # yield from response.follow_all(tag_page_links, self.parse_tag) ## change the callback type

        # pagination_links = response.css('li.next a')
        # yield from response.follow_all(pagination_links, self.parse)

    def parse_match(self, response):
        # title_selector = response.xpath('//h1[contains(@class, "Headline-headline")]')
        # title = title_selector.xpath('text()').extract()[0]
        # text_selectors = response.xpath('//p[contains(@class, "Paragraph-paragraph")]')
        # text = text_selectors.xpath('text()').extract()
        # text = ' '.join(text)
        # date_selector = response.xpath('//time')
        # page = response.url.split("/")[-2]

        title_selector = response.xpath('//h1[contains(@class, "clearfix")]')
        title = title_selector.xpath('span()').extract()[0]
        
        yield {
            'title': title,
        }

    # #     def extract_with_css(query):
    # #         return response.css(query).get(default='').strip()

    #     yield {
    #         'title': extract_with_css('h1').re(r'.*Headline-headline.*'),
    # #         #'birthdate': extract_with_css('.author-born-date::text'),
    # #         #'bio': extract_with_css('.author-description::text'),
    #     }