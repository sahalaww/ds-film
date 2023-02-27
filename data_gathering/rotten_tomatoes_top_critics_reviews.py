import requests
import json
import base64
import time
import urllib.parse as urlparser
import random
import csv

headers = {
    'authority': 'www.rottentomatoes.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'referer': 'https://www.rottentomatoes.com/m/iron_man/reviews?type=top_critics',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

all_data = []
i = 0

while True:
    p1 = str(base64.b64encode(str(i).encode('utf-8')))[1::].replace("'", "")
    p1_uri_encode = urlparser.quote(p1)
    response = requests.get(
        "https://www.rottentomatoes.com/napi/movie/41ca006b-8820-379c-84fc-aaae870b37f6/criticsReviews/top_critics/:sort?&f=null&direction=prev&endCursor=&startCursor=" + p1_uri_encode,
        headers=headers,
    )

    r = json.loads(response.text)
    reviews = r['reviews']
    has_next_page = r['pageInfo']['hasNextPage']
    print(i, has_next_page)
    all_data.extend(reviews)
    if not has_next_page:
        break

    i = i + 1
    time.sleep(random.randint(3, 7))

save_reviews_file = open('reviews_top_critics_iron-man-2008_all.json', 'w')
json.dump(all_data, save_reviews_file, indent=4)
save_reviews_file.close()

reviews_file = open('reviews_top_critics_iron-man-2008_all.json', 'r')
reviews_json = json.load(reviews_file)

with open('reviews_top_critics_iron-man-2008_all.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    csv_header = ['creation_date', 'critic_name', 'critic_picture', 'critic_vanity', 'is_fresh', 'is_rotten',
                  'is_rt_url', 'is_rt_url', 'is_top', 'publication_id', 'publication_name', 'review_url', 'quote',
                  'review_id', 'score_ori', 'score_sentiment']

    writer.writerow(csv_header)
    for i in range(len(reviews_json)):
        creation_date = reviews_json[i]['creationDate']
        critic_name = reviews_json[i]['critic']['name']
        critic_picture = reviews_json[i]['critic']['criticPictureUrl']
        critic_vanity = reviews_json[i]['critic']['vanity']
        is_fresh = reviews_json[i]['isFresh']
        is_rotten = reviews_json[i]['isRotten']
        is_rt_url = reviews_json[i]['isRtUrl']
        is_top = reviews_json[i]['isTop']
        publication_id = reviews_json[i]['publication']['id']
        publication_name = reviews_json[i]['publication']['name']
        review_url = reviews_json[i]['reviewUrl']
        quote = reviews_json[i]['quote']
        review_id = reviews_json[i]['reviewId']
        score_ori = reviews_json[i]['scoreOri']
        score_sentiment = reviews_json[i]['scoreSentiment']

        writer.writerow([creation_date, critic_name, critic_picture, critic_vanity, is_fresh, is_rotten,
                         is_rt_url, is_rt_url, is_top, publication_id, publication_name, review_url, quote,
                         review_id, score_ori, score_sentiment])
