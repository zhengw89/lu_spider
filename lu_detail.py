from urllib import request
from bs4 import BeautifulSoup
import pprint


class LuFundDetail:

    def __init__(self, url):
        self.url = url

        page = request.urlopen(url)
        soup = BeautifulSoup(page, 'html5lib')

        self.product_id = url[-7:]
        self.__base_info__(soup)
        self.__grade__(soup)
        self.__stage_performance__(soup)
        self.__quarter_performance__(soup)
        self.__year_performance__(soup)

    def __base_info__(self, soup):
        self.net_value = soup.find('div', {'class': 'product-info'}) \
            .find('div', {'class': 'is-second clearfix'}) \
            .contents[1].contents[1].contents[1].string
        self.net_value = float(self.net_value)

        info_ul = soup.find('ul', {'class': 'fund-info'})
        self.code = info_ul.contents[1].contents[1].string
        self.name = info_ul.contents[3].contents[1].string
        self.company = info_ul.contents[5].contents[1].string
        self.type = info_ul.contents[7].contents[1].string
        self.custodian = info_ul.contents[13].contents[1].string
        self.setup_date = info_ul.contents[15].contents[1].string.replace('年', '-').replace('月', '-').replace('日', '')
        self.scale = info_ul.contents[19].contents[1].string

        if self.scale.endswith('亿元'):
            self.scale = int(float(self.scale.replace('亿元', '')) * 100000000)

    def __grade__(self, soup):
        self.grade = []
        grade_items = soup.find('div', {'class': 'fund-grade'}) \
            .find('table', {'class': 'product-table'}) \
            .tbody.find_all('tr')

        for tr in grade_items:
            if len(tr) > 3:
                self.grade.append(LuFundGrade(tr))

    def __stage_performance__(self, soup):
        performance_trs = soup.find('table', {'class': 'product-table productRateTable'}).tbody.contents[1] \
            .find_all('span')

        if performance_trs[1].string.strip() != '--':
            self.week_rate = performance_trs[1].string.strip()
        if performance_trs[2].string.strip() != '--':
            self.month_rate = performance_trs[2].string.strip()
        if performance_trs[3].string.strip() != '--':
            self.quarter_rate = performance_trs[3].string.strip()
        if performance_trs[4].string.strip() != '--':
            self.half_year_rate = performance_trs[4].string.strip()
        if performance_trs[5].string.strip() != '--':
            self.year_rate = performance_trs[5].string.strip()

    def __quarter_performance__(self, soup):
        quarter_performance_table = soup.find_all('table', {'class': 'productRateTable'})[1]
        self.quarter_performance = self.__parse_performance_table__(quarter_performance_table)

    def __year_performance__(self, soup):
        year_performance_table = soup.find_all('table', {'class': 'productRateTable'})[2]
        self.year_performance = self.__parse_performance_table__(year_performance_table)

    def __parse_performance_table__(self, table):
        performance = []
        title_items = table.thead.tr.find_all('th')
        title_items.pop(0)

        stage_items = table.tbody.find_all('tr')[0].find_all('span')
        stage_items.pop(0)

        rank_items = table.tbody.find_all('tr')[4].find_all('td')
        rank_items.pop(0)

        for index in range(len(stage_items)):
            if stage_items[index].string.strip() != '--':
                performance.append(
                    LuFundPerformance(title_items[index].string.strip(),
                                      stage_items[index].string.strip(),
                                      rank_items[index].string.strip()))

        return performance

    def __repr__(self):
        return str(self.__dict__.copy())

    def pprint(self):
        pprint.pprint(self.__dict__, width=1)


class LuFundGrade:

    def __init__(self, html):
        self.organization = html.contents[1].contents[0].string
        self.date = html.contents[3].contents[0].string
        self.level = html.contents[5].contents[0]['class'][-1] \
            .replace('one', '1').replace('two', '2') \
            .replace('three', '3').replace('four', '4').replace('five', '5')

    def __repr__(self):
        return str(self.__dict__.copy())


class LuFundPerformance:

    def __init__(self, title, performance, rank):
        self.title = title
        self.performance = performance
        self.rank = rank

    def __repr__(self):
        return str(self.__dict__.copy())


if __name__ == '__main__':
    luDetail = LuFundDetail("https://e.lufunds.com/jijin/detail?productId=2279195")
    luDetail.pprint()
