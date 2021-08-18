# import scrapy


# class QuotesSpider(scrapy.Spider):
#     name = "quotes"

#     # def start_requests(self):
#     #     urls = [
#     #         'http://quotes.toscrape.com/page/1/',
#     #         'http://quotes.toscrape.com/page/2/',
#     #     ]
#     #     for url in urls:
#     #         yield scrapy.Request(url=url, callback=self.parse)

#     # replaces the above
#     start_urls = [
#         'http://quotes.toscrape.com/page/1/',
#         'http://quotes.toscrape.com/page/2/',
#     ]

#     def start_requests(self):
#         url = 'http://quotes.toscrape.com/'
#         tag = getattr(self, 'tag', None)
#         if tag is not None:
#             url = url + 'tag/' + tag
#         yield scrapy.Request(url, self.parse)

#     def parse(self, response):
#         for quote in response.css('div.quote'):
#             yield {
#                 'text': quote.css('span.text::text').get(),
#                 'author': quote.css('small.author::text').get(),
#                 'tags': quote.css('div.tags a.tag::text').getall(),
#             }

#             # in the Shell:

#             ## scrapy crawl quotes -O quotes.json
#                 ### -O overwrites
#                 ### -o does not overwrite 
#                 #### appending invalidates JSON but not JSON LINES - see BELOW:
#             ##scrapy crawl quotes -o quotes.jl

#         # Requests for shortcuts
#         # #Strings
#             # next_page = response.css('li.next a::attr(href)').get()
#             # if next_page is not None:
#             #     #next_page = response.urljoin(next_page)
#             #     #yield scrapy.Request(next_page, callback=self.parse)

#             #     #replaces above
#             #     ## .follow follows -'relative' requests unlike .Request
#             #     yield response.follow(next_page, callback=self.parse

#         # #Selectors
#             # for href in response.css('ul.pager a::attr(href)'):
#             #     yield response.follow(href, callback=self.parse)

#         # # <a> elements
#             # for a in response.css('ul.pager a'):
#             #     yield response.follow(a, callback=self.parse)
        
#         # # iterabbles
#             # anchors = response.css('ul.pager a')
#             # yield from response.follow_all(anchors, callback=self.parse)

#         # # iterabbles shortened
#             # yield from response.follow_all(css='ul.pager a', callback=self.parse)





# Arguments in the Shell: (passed to the Spider’s __init__ method)
    ## scrapy crawl quotes -O quotes-humor.json -a tag=humor
    ### tag (self.tag)

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        url = 'http://quotes.toscrape.com/'
        tag = getattr(self, 'tag', None) #get tag else none
        if tag is not None:
            url = url + 'tag/' + tag
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)