import scrapy
from ..items import CelebItem    #importing class from items.py
from monkeylearn import MonkeyLearn  #importing this for keyword extraction

import re

class QuoteSpider(scrapy.Spider):

    name = 'actor'   #name of spider

    #state the list of urls you want to scrape
    start_urls = [
        'https://www.imdb.com/list/ls068010962/'
    ]

    def parse(self, response):    #response contains the source code of the parsed site

        items = CelebItem()

        stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", \
                     "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', \
                     'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', \
                     'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these',
                     'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do',
                     'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while',
                     'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before',
                     'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
                     'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each',
                     'few', 'more', 'most', 'other', 'some', 'such', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o',
                     're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't",'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't",
                     'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'href','shouldn', "shouldn't", 'wasn', "wasn't", 'weren',"weren't", 'won', "won't", 'wouldn', "wouldn't"]

        all_celeb = response.css("div.lister-item.mode-detail")    #extracting per block per actor

        for celeb in all_celeb: #extracting info one actor at a time

            name = celeb.css(".lister-item-header a::text").extract()
            image = celeb.css("div.lister-item-image img").xpath("@src").extract()
            info = celeb.css(".text-small+ p").extract()

            #cleaning text
            phrase = re.sub(r"won't", "will not", info[0])
            phrase = re.sub(r"can\'t", "can not", phrase)

            phrase = re.sub(r"n\'t", " not", phrase)
            phrase = re.sub(r"\'re", " are", phrase)
            phrase = re.sub(r"\'s", " is", phrase)
            phrase = re.sub(r"\'d", " would", phrase)
            phrase = re.sub(r"\'ll", " will", phrase)
            phrase = re.sub(r"\'t", " not", phrase)
            phrase = re.sub(r"\'ve", " have", phrase)
            text = re.sub(r"\'m", " am", phrase)

            text = text.replace('\\r', ' ')
            text = text.replace('\\"', ' ')
            text = text.replace('\\n', ' ')
            text = re.sub('[^A-Za-z0-9]+', ' ', text)

            text = ' '.join(e for e in text.split() if e.lower() not in stopwords)

            #keyword extraction
            ml = MonkeyLearn('6b40ae68e34cbc91e37aebdd56a87c82694becb8')
            data = [text]
            model_id = 'ex_YCya9nrn'
            result = ml.extractors.extract(model_id, data)

            feature_list = []
            for i in range(10):
                a = result.body[0]['extractions'][i]['parsed_value']
                feature_list.append(a)   #preparing the feature list

            items['name'] = name
            items['image'] = image
            items['info'] = feature_list

            yield items


            #handling continuous web pages
            next_page = response.css("a.flat-button.lister-page-next.next-page::attr(href)").extract()

            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)