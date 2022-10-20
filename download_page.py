import requests
import datetime
from datetime import datetime
import csv
from bs4 import BeautifulSoup as bs


def get_page(urls):
    categories = []
    category = ""
    with open("subcats.txt") as cats_file:
        for cat in cats_file:
            cat = cat.strip()
            categories.append(cat)

    with open(urls) as links_file:
        for count, link in enumerate(links_file):
            link = link.strip()
            for cat in categories:
                if cat.lower() in link:
                    category = cat.lower()
            HEADERS = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537/6",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "origin": link,
                "referer": link,
            }
            page = requests.get(link, headers=HEADERS)

            parse_url = link.split(".")

            for i in parse_url[1:]:
                if i == "www":
                    continue
                else:

                    # file_name = f"{i}-{category}.html"
                    file_name = f"{i}{datetime.today().strftime('%Y-%m-%d-%H-%M-%S')}-{count}.html"
                    file_name = f"{i}-{category}-{datetime.today().strftime('%Y-%m-%d')}-{count}.html"

                    break

            with open(file_name, "wb") as outfile:
                outfile.write(page.content)


get_page("groupon_links.txt")
