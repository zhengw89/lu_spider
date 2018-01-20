from urllib import request
from bs4 import BeautifulSoup


class LuFundPage:

    def __init__(self, url):
        self.url = url
        self._lu_items = []

    def load(self):
        self._lu_items.clear()
        page = request.urlopen(self.url)
        soup = BeautifulSoup(page, "html5lib")

        trs = soup.find_all('tr', {'data-sk-area': 'FundList-a'})

        for tr in trs:
            self._lu_items.append(LuFundItem(tr))

        return self._lu_items


class LuFundItem:

    def __init__(self, html):
        self._bs = html

        self._code = self._bs.contents[1].string
        self._name = self._bs.contents[3].a.string
        self._detail_url = 'https:' + self._bs.contents[3].a['href']
        self._price = self._bs.contents[5].p.string
        self._day_rate = self._bs.contents[7].span.string
        self._month_rate = self._bs.contents[9].span.string
        self._quarter_rate = self._bs.contents[11].span.string
        self._year_rate = self._bs.contents[13].span.string
        self._current_year_rate = self._bs.contents[15].span.string
        self._after_setup_rate = self._bs.contents[17].span.string

    @property
    def code(self):
        return self._code

    @property
    def name(self):
        return self._name

    @property
    def detail_url(self):
        return self._detail_url

    @property
    def price(self):
        return self._price

    @property
    def day_rate(self):
        return self._day_rate

    @property
    def month_rate(self):
        return self._month_rate

    @property
    def quarter_rate(self):
        return self._quarter_rate

    @property
    def year_rate(self):
        return self._year_rate

    @property
    def current_year_rate(self):
        return self._current_year_rate

    @property
    def after_setup_rate(self):
        return self._after_setup_rate

    def __repr__(self):
        property_dic = self.__dict__.copy()
        property_dic.pop('_bs', None)
        return str(property_dic)

    def html(self):
        print(self._bs.prettify())

    def to_string(self):
        return "Code:{}  Name:{}".format(self._code, self._name)


if __name__ == '__main__':
    luPage = LuFundPage("https://e.lufunds.com/jijin/list?currentPage=1")
    luItems = luPage.load()
    for luItem in luItems:
        print(luItem.__repr__())
