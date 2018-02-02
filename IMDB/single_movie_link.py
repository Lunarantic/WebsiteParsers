import requests
import bs4


class Parser:
    def __init__(self, link_to_scrape=""):
        self.link_to_scrape = link_to_scrape
        self.page_being_scrape = None
        pass

    def link_to_scrape(self, link_to_scrape):
        if link_to_scrape:
            self.link_to_scrape = link_to_scrape
        pass

    def check_link(self):
        try:
            page_being_scrape = requests.get(self.link_to_scrape)
            print(str(page_being_scrape.headers))
            self.page_being_scrape = page_being_scrape
            return True
        except requests.exceptions.MissingSchema as e:
            print(e.args)
        except BaseException as e:
            print(e.args)
        return False

    def parse(self):
        print("Parsing link :: %s" % self.link_to_scrape)
        if not self.check_link():
            return

        page_soup = bs4.BeautifulSoup(self.page_being_scrape.content, "html5lib")

        divs = page_soup.find('body')

        title_details_div = divs.find('div', id='titleDetails')
        h3s = title_details_div.find('h3', string='Box Office')
        details = h3s.find_next_siblings('div')
        if len(details) > 4:
            details = details[:4]

        details = [det.get_text() for det in details]
        print("\n\n\n\n\n")
        print(details)

        print("Still parsing")

        pass


if __name__ == "__main__":
    p = Parser("http://www.imdb.com/title/tt1469304")
    p.parse()
