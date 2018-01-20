from urllib import request
from bs4 import BeautifulSoup
import pprint


class LuFundDetail:

    def __init__(self, url):
        self.url = url
        self._grade = []

        page = request.urlopen(url)
        soup = BeautifulSoup(page, 'html5lib')

        self.__base_info__(soup)
        self.__grade__(soup)

    def __base_info__(self, soup):
        self._net_value = soup.find('div', {'class': 'product-info'})\
            .find('div', {'class': 'is-second clearfix'})\
            .contents[1].contents[1].contents[1].string
        self._net_value = float(self._net_value)

        info_ul = soup.find('ul', {'class': 'fund-info'})
        self._code = info_ul.contents[1].contents[1].string
        self._name = info_ul.contents[3].contents[1].string
        self._company = info_ul.contents[5].contents[1].string
        self._type = info_ul.contents[7].contents[1].string
        self._custodian = info_ul.contents[13].contents[1].string
        self._setup_date = info_ul.contents[15].contents[1].string.replace('年', '-').replace('月', '-').replace('日', '')
        self._scale = info_ul.contents[19].contents[1].string

        if self._scale.endswith('亿元'):
            self._scale = int(float(self._scale.replace('亿元', '')) * 100000000)

    def __grade__(self, soup):
        grade_items = soup.find('div', {'class': 'fund-grade'}) \
            .find('table', {'class': 'product-table'}) \
            .tbody.find_all('tr')

        for tr in grade_items:
            if len(tr) > 3:
                self._grade.append(LuFundGrade(tr))

    def __repr__(self):
        return str(self.__dict__.copy())

    def pprint(self):
        pprint.pprint(self.__dict__, width=1)


class LuFundGrade:

    def __init__(self, html):
        self._organization = html.contents[1].contents[0].string
        self._date = html.contents[3].contents[0].string
        self._level = html.contents[5].contents[0]['class'][-1] \
            .replace('one', '1').replace('two', '2') \
            .replace('three', '3').replace('four', '4').replace('five', '5')

    def __repr__(self):
        return str(self.__dict__.copy())


if __name__ == '__main__':
    luDetail = LuFundDetail("https://e.lufunds.com/jijin/detail?productId=2708445")
    luDetail.pprint()
