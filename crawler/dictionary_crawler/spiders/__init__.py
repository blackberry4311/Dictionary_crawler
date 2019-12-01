import re
import scrapy
from crawler.dictionary_crawler.model.CambridgeItem import CambridgeItem

# by Peyman (mohsenikiasari@ce.sharif.edu) in 2019.
words = ['remember', 'us', 'this', 'way']


#  scrapy crawl oxford -o oxford.jl
class OxfordCrawler(scrapy.Spider):
    name = "oxford"
    allowed_domains = ["www.lexico.com"]
    start_urls = ["https://www.lexico.com/en/definition/" + word for word in words]

    def parse(self, response):
        word = response.request.url.split("/")[-1]
        definition_dict = {}

        for sections in response.xpath("//section[@class='gramb']"):
            try:
                part_of_speech = sections.xpath(".//span[@class='pos']/text()").extract()[0]
            except:
                part_of_speech = False
            def_list = sections.xpath("./ul/li/div[@class='trg']//span[@class='ind']").extract()
            if not def_list:
                def_list = sections.xpath(".//div[@class='empty_sense']//div[@class='crossReference']").extract()

            def_list = [re.sub(r'<.*?>', "", i).strip() for i in def_list]
            def_list = [i for i in def_list if i]

            if def_list and part_of_speech:
                if part_of_speech in definition_dict:
                    definition_dict[part_of_speech] += def_list
                else:
                    definition_dict[part_of_speech] = def_list

        if definition_dict:
            yield {word: definition_dict}


#  scrapy crawl longman -o longman.jl
class LongmanCrawler(scrapy.Spider):
    name = "longman"
    allowed_domains = ["https://www.ldoceonline.com"]
    start_urls = ["https://www.ldoceonline.com/dictionary/" + word for word in words]

    def parse(self, response):
        word = response.request.url.split("/")[-1]
        definition_dict = {}

        for sections in response.xpath("//span[@class='dictentry']"):
            try:
                part_of_speech = (sections.xpath(".//span[@class='POS']/text()").extract()[0]).strip()
            except:
                part_of_speech = False
            def_list = sections.xpath(".//span[@class='Sense']/span[@class='DEF']").extract()
            def_list = [re.sub(r'<.*?>', "", i[18:-7]).strip() for i in def_list]
            def_list = [i for i in def_list if i]

            if def_list and part_of_speech:
                if part_of_speech in definition_dict:
                    definition_dict[part_of_speech] += def_list
                else:
                    definition_dict[part_of_speech] = def_list

        if definition_dict:
            yield {word: definition_dict}


#  scrapy crawl cambridge -o cambridge.jl
class CambridgeCrawler(scrapy.Spider):
    name = "cambridge"
    current_domain = "https://dictionary.cambridge.org"
    allowed_domains = [current_domain]
    start_urls = ["https://dictionary.cambridge.org/dictionary/english/" + word for word in words]

    def parse(self, response):
        word = response.request.url.split("/")[-1]
        definition_dict = []
        dictionary = response.xpath("//*[@id='page-content']/div[@class='page']/div/div")[0]
        output_word = CambridgeItem()
        for form_list in dictionary.xpath(".//div[@class='entry-body']/div"):
            word_header = form_list.xpath(".//div[@class='pos-header dpos-h']")
            uk = word_header.xpath(".//span[contains(@class,'uk dpron-i')]")
            try:
                uk_sound = self.current_domain + uk.xpath(".//amp-audio//@src").extract_first()
            except:
                uk_sound = None

            uk_pronounce = uk.xpath(".//span[@class='pron dpron']").extract_first()
            uk_pronounce = re.sub(r'<.*?>|:', "", uk_pronounce).strip()

            us = word_header.xpath(".//span[contains(@class,'us dpron-i')]")
            try:
                us_sound = self.current_domain + us.xpath(".//amp-audio//@src").extract_first()
            except:
                us_sound = None
            us_pronounce = us.xpath(".//span[@class='pron dpron']").extract_first()
            us_pronounce = re.sub(r'<.*?>|:', "", us_pronounce).strip()

            try:
                tense = word_header.xpath(".//span[contains(@class,'irreg-infls dinfls')]").extract()[0]
                tense = re.sub(r'<.*?>|:', "", tense).strip()
            except:
                tense = None

            form = word_header.xpath(".//span[contains(@class,'pos dpos')]/text()").extract_first()

            definition_output = []
            for definition_list in form_list.xpath(".//div[contains(@class,'pr dsense')]"):
                for definition_block in definition_list.xpath(".//div[contains(@class,'def-block ddef_block')]"):
                    try:
                        level = definition_block.xpath(
                            ".//span[contains(@class,'epp-xref dxref')]/text()").extract_first()
                    except:
                        level = None
                    meaning = definition_block.xpath(".//div[contains(@class,'def ddef_d db')]").extract_first()
                    meaning = re.sub(r'<.*?>|:', "", meaning).strip()
                    example = definition_block.xpath(".//div[@class='def-body ddef_b']/div").extract()
                    example = [re.sub(r'<.*?>|:', "", i).strip() for i in example]

                    if meaning and level:
                        definition_output.append(
                            {'level': level, 'meaning': meaning, 'example': example})
            if definition_output:
                definition_dict.append({'form': form, 'tense': tense, 'us_pronounce': us_pronounce,
                                        'us_sound': us_sound, 'uk_pronounce': uk_pronounce,
                                        'uk_sound': uk_sound, 'definition': definition_output})

        if definition_dict:
            output_word['word'] = word
            output_word['definitions'] = definition_dict
            yield output_word


#  scrapy crawl webster -o webster.jl
class WebsterCrawler(scrapy.Spider):
    name = "webster"
    allowed_domains = ["https://www.merriam-webster.com"]
    start_urls = ["https://www.merriam-webster.com/dictionary/" + word for word in words]

    def parse(self, response):
        word = response.request.url.split("/")[-1]
        definition_dict = {}

        part_of_speeches = [re.sub(r'\(.*\)', "", i).strip() for i in
                            response.xpath("//span[@class='fl']/a/text()|//span[@class='fl']/text()").extract()]

        for sections in response.xpath("//div[contains(@id, 'dictionary-entry')]/div[@class='vg']"):
            part_of_speech = part_of_speeches.pop(0)
            def_list = sections.xpath(
                ".//span[@class='dtText' or @class='unText'][not(ancestor::span[@class='dtText'])]").extract()
            def_list = [re.sub(r'<span.*>.+</span>', "", i[21:-7]) for i in def_list]
            def_list = [re.sub(r'<.*?>|:', "", i).strip() for i in def_list]
            def_list = [i for i in def_list if i]

            if def_list and part_of_speech:
                if part_of_speech in definition_dict:
                    definition_dict[part_of_speech] += def_list
                else:
                    definition_dict[part_of_speech] = def_list

        if definition_dict:
            yield {word: definition_dict}


#  scrapy crawl collins -o collins.jl
class CollinsCrawler(scrapy.Spider):
    name = "collins"
    allowed_domains = ["https://www.collinsdictionary.com"]
    start_urls = ["https://www.collinsdictionary.com/dictionary/english/" + word for word in words]

    def parse(self, response):
        word = response.request.url.split("/")[-1]
        definition_dict = {}

        for sections in response.xpath("//div[@class='dictionary Cob_Adv_Brit']"
                                       "//div[@class='content definitions cobuild br']/div[@class='hom']"):
            try:
                part_of_speech = (sections.xpath(".//span[@class='pos']/text()").extract()[0]).strip()
            except:
                part_of_speech = False
            def_list = sections.xpath("./div[@class='sense']/div[@class='def']").extract()
            def_list = [re.sub(r'<.*?>', "", i[17:-6]).strip() for i in def_list]
            def_list = [i for i in def_list if i]

            if def_list and part_of_speech:
                if part_of_speech in definition_dict:
                    definition_dict[part_of_speech] += def_list
                else:
                    definition_dict[part_of_speech] = def_list

        if definition_dict:
            yield {word: definition_dict}
