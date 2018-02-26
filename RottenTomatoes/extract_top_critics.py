import requests
from bs4 import BeautifulSoup

def get_div_info(div, pattern):
    data = div.select(pattern)
    if data and len(data) > 0:
        return data[0].get_text()
    
def getReviews(movie_id):
    reviews = []
    page_url="https://www.rottentomatoes.com/m/%s/reviews/?type=top_critics" % movie_id
    page = requests.get(page_url)         
    
    if page.status_code==200:  
        soup = BeautifulSoup(page.content, 'html.parser') 
        select_data = soup.select("div#reviews div.row.review_table_row")

        for sd in enumerate(select_data):
            reviewer = get_div_info(sd, "div div.critic_name a")
            dt = get_div_info(sd, "div.review_date")
            desc = get_div_info(sd, "div.review_desc div.the_review")
            score = get_div_info(sd, "div.review_desc div.small.subtle")[31:]
           
           reviews.append((reviewer, dt, desc, score))
    return reviews


if _name== "main_":    
    movie_id = 'john_wick' # 'john_wick_chapter_2' # 'finding_dory'
    reviews = getReviews(movie_id) 
    print(reviews)
    
