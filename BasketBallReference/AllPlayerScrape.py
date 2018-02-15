import requests
import bs4
import pandas
import urllib
import numpy
import time
import string


# Performance Calculations Constants
point_scored = 1
missed_field_goal = -.25
missed_field_throw = -.25
assist = 1.5
rebound = 1.25
turnover = -.5
steal = 2
block = 2
three_point_made = 1
double_double = 2
triple_double = 2


def get_html_table_in_dataframe(divs, html_attr_id):

    div = divs.find(id="all_"+html_attr_id)
    table = div.find(id=html_attr_id)
    if not table:
        html = str(bs4.BeautifulSoup(''.join([c.extract() for c in div.find_all(
            string=lambda text: isinstance(text, bs4.Comment))]), "html5lib").find(id=html_attr_id))
    else:
        html = str(table)

    df = pandas.read_html(html, header=0)
    df = df[0].iloc[:, :30]
    df = df.set_index('Season')
    df.index.names = ['Year']
    print "\n\n\n" + str(df.to_json())

    df['point_scored'] = (df.PTS * point_scored)

    df['missed_goals'] = (df.FGA - df.FG)
    df['calP'] = df.FG + df['3P'] + df['2P']
    df['calP2'] = df.FG + (2 * df['3P']) + df['2P']
    df['missed_field_goal'] = ((df.FGA - df.FG) * missed_field_goal)

    df['missed_field_throw'] = ((df.FTA - df.FT) * missed_field_throw)

    df['assist'] = df.AST * assist

    df['rebound'] = df.TRB * rebound

    df['turnovers'] = df.TOV * turnover

    df['steal'] = df.STL * steal

    df['block'] = df.BLK * block

    df['three_point_made'] = df['3P'] * three_point_made

    # df['double_double'] = numpy.where(df['2P']) * double_double

    # df['triple_double'] = df[''] * triple_double

    df['performance'] = df.point_scored + df.missed_field_goal + df.missed_field_throw + df.assist + df.rebound + \
                        df.turnovers + df.steal + df.block + df.three_point_made

    # print(df[['PTS', 'performance', 'FGA', 'FG', 'calP', 'calP2']])

    return df


def basket_ball_reference_scrape_player(link_to_scrape="https://www.basketball-reference.com/players/j/jamesle01.html"):

    print "Scrapping :: " + link_to_scrape

    page_being_scrape = requests.get(link_to_scrape)
    page_soup = bs4.BeautifulSoup(page_being_scrape.content, "html.parser")

    divs = page_soup.find('body')
    # print divs

    print "\n\n\n"

    # try:
    #     lebron_image_url = [img for img in divs.find_all('img') if 'photo of' in img['alt'].lower()][0]['src']
    #     urllib.urlretrieve(lebron_image_url, 'lebron_james.jpg')
    #     print 'Image of Lebron James downloaded'
    # except:
    #     print "Image of Lebron James not downloaded"

    # Getting data from per_game table
    per_game_df = get_html_table_in_dataframe(divs, "per_game")

    print "\n\n\n"

    # Getting data from per_game table
    playoffs_per_game_df = get_html_table_in_dataframe(divs, "playoffs_per_game")

    compared_df = per_game_df[['performance']].join(playoffs_per_game_df[['performance']],
                                                    lsuffix='_season', rsuffix='_playoffs').fillna(0)
    compared_df['better_performed_in'] = numpy.where(
        compared_df['performance_playoffs'] == 0.0, 'None', numpy.where(
            compared_df['performance_playoffs'] < compared_df['performance_season'], 'Season', 'Playoffs'))
    print(compared_df)


def scrape_player_links(link_to_scrape="https://www.basketball-reference.com/players/a/"):

    page_being_scrape = requests.get(link_to_scrape)
    page_soup = bs4.BeautifulSoup(page_being_scrape.content, "html.parser")

    divs = page_soup.find('body')

    div = divs.find(id="div_players")
    table = div.find("table")
    tbody = table.find("tbody")
    trs = tbody.find_all("tr")

    player_links = [tr.find("th").find("a").get("href") for tr in trs]

    for link in player_links:
        try:
            basket_ball_reference_scrape_player("https://www.basketball-reference.com" + link)
        except:
            pass
        time.sleep(1)
    return


if __name__ == '__main__':
    for alphabet in list(string.ascii_lowercase):
        try:
            scrape_player_links("https://www.basketball-reference.com/players/" + alphabet + "/")
        except:
            pass
