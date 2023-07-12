from bs4 import BeautifulSoup
import re


class StringCleaner():
    def raw_text(dirty_string):
        soup = BeautifulSoup(dirty_string, 'lxml')
        return soup.get_text('', strip=True)

    def remove_tags(self, dirty_string):
        return BeautifulSoup(dirty_string, 'lxml').text.strip()

    def convert_entities(self, dirty_string):
        return BeautifulSoup(dirty_string).text

    def remove_whitespaces(self, dirty_string):
        return re.sub("\s+", " ", dirty_string, flags=re.UNICODE)