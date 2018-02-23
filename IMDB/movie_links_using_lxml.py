from lxml import html
import requests


def parse_single(link):
    try:
        page = requests.get(link)
        tree = html.fromstring(page.content)

        budget = ''.join(tree.xpath('//*[@id="titleDetails"]/div[7]/text()')).replace('\n','').replace(' ','')
        opening_weekend = ''.join(tree.xpath('//*[@id="titleDetails"]/div[8]/text()')).replace('\n','').replace(' ','').strip(',')
        gross_usa = ''.join(tree.xpath('//*[@id="titleDetails"]/div[9]/text()')).replace('\n','').replace(' ','')
        gross_world = ''.join(tree.xpath('//*[@id="titleDetails"]/div[10]/text()')).replace('\n','').replace(' ','')
        # print(budget, opening_weekend, gross_usa, gross_world)
        return (budget, opening_weekend, gross_usa, gross_world)
    except:
        return None

def parse_links(links):
    box_office_data = {}
    for link in links:
        box_office_data[link] = parse_single(link)
    return box_office_data
    

if __name__=="__main__":
    links = ['http://www.imdb.com/title/tt1469304/']
    box_office_data = parse_links(links)
    print(str(box_office_data))
