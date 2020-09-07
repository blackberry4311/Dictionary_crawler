import datetime
import re

from scrapy import Spider

from crawler.dictionary_crawler.model.CambridgeItem import CambridgeItem


# words="goat,angry,clean,cool,ask,street,swim,skate,roof,worse,field,change,choose,different,stadium,competition,foggy,journalist,invent,important,design,region,curious,peaceful,meaning,direct,study,involve,approximate,considerable,alternative,interfere,measure,navigate,opponent,Profound,conceptual,Emission,segment,excavate,eradicate,impartial"


#  scrapy crawl cambridge -a words="test,remember"
class CambridgeCrawler(Spider):
    name = "cambridge"
    current_domain = "https://dictionary.cambridge.org"
    allowed_domains = [current_domain]

    def __init__(self, *args, **kwargs):
        super(CambridgeCrawler, self).__init__(*args, **kwargs)

        words = kwargs.get('words').split(',')
        self.start_urls = ["https://dictionary.cambridge.org/dictionary/english/" + word for word in words]

    def parse(self, response):
        word = response.request.url.split("/")[-1]
        definition_dict = []
        dictionary = response.xpath("//*[@id='page-content']/div[@class='page']//div[@class='entry']")[0]
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

                    if meaning:
                        definition_output.append(
                            {'level': level, 'meaning': meaning, 'example': example})
            if definition_output:
                definition_dict.append({'form': form, 'tense': tense, 'us_pronounce': us_pronounce,
                                        'us_sound': us_sound, 'uk_pronounce': uk_pronounce,
                                        'uk_sound': uk_sound, 'definition': definition_output})

        if definition_dict:
            output_word['word'] = word
            output_word['definitions'] = definition_dict
            output_word['crawled_at'] = datetime.datetime.utcnow()
            yield output_word
