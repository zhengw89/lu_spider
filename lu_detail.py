from urllib import request
from bs4 import BeautifulSoup


class LuFundDetail:

    def __init__(self, url):
        self.url = url

        page = request.urlopen(url)
        soup = BeautifulSoup(page, 'html5lib')

        self.__base_info__(soup)

    def __base_info__(self, soup):
        info_ul = soup.find('ul', {'class': 'fund-info'})
        self.code = info_ul.contents[1].contents[1].string
        self.name = info_ul.contents[3].contents[1].string
        self.company = info_ul.contents[5].contents[1].string
        self.type = info_ul.contents[7].contents[1].string
        self.custodian = info_ul.contents[13].contents[1].string
        self.setup_date = info_ul.contents[15].contents[1].string
        self.scale = info_ul.contents[19].contents[1].string

    def __repr__(self):
        return str(self.__dict__.copy())


if __name__ == '__main__':
    luDetail = LuFundDetail("https://e.lufunds.com/jijin/detail?productId=2279195")
    print(luDetail.__repr__())
