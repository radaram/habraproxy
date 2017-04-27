import re
from urllib.parse import urlparse

from lxml import html

from settings import HABRAHABR_URL


class TMSetter(object):
    SKIP_TAGS = ('style', 'link', 'script', 'noscript')
    TM_CODE = "\u2122"
    WORD_LENGTH = 6

    def modify(self, content, base_url=None):
        self.base_url = base_url
        if not content:
            return content
        root = html.fromstring(content)
        for chield in root.xpath('.//body//*'):
            self._modify_element(chield)
        return '<!DOCTYPE html>' + html.tostring(root, encoding='unicode')

    def _modify_element(self, element):
        if not element.tag in TMSetter.SKIP_TAGS:
            if element.tail:
                element.tail = self._modify_text(element.tail)
            if element.text:
                element.text = self._modify_text(element.text)
            if element.tag == 'a' and 'href' in element.attrib:
                self._replace_link(element, HABRAHABR_URL, self.base_url)

    def _replace_link(self, element, old_url, new_url):
        source_url_obj = urlparse(element.attrib['href'])
        old_url_obj, new_url_obj = urlparse(old_url), urlparse(new_url)

        if old_url_obj.netloc == source_url_obj.netloc:
            element.attrib['href'] = element.attrib['href'].replace(
                old_url_obj.netloc, new_url_obj.netloc
            )

            if new_url_obj.scheme == 'http' and source_url_obj.scheme == 'https':
                element.attrib['href'] = element.attrib['href'].replace(
                    'https://', 'http://'
                )

    def _modify_text(self, text):
        words = set(re.split('\W+', str(text), flags=re.UNICODE))
        for word in words:
            if len(word) != TMSetter.WORD_LENGTH:
                continue
            text = re.sub(r'\b{}\b'.format(word),
                          '{}{}'.format(word, TMSetter.TM_CODE),
                          text,
                          flags=re.UNICODE)
        return text
