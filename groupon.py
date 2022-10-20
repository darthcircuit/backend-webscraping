from urllib import request
from bs4 import BeautifulSoup as bs
import csv

# from download_page import get_page
import os

# url = "https://www.groupon.com/browse/salt-lake-city?lat=40.315&lng=-111.702&query=escape+room&address=Orem%2C+UT+84057&division=salt-lake-city&locale=en_US"
# url = "https://www.groupon.com/browse/salt-lake-city"
# file_name = get_page(url)


html_files = []
categories = []
category = ""
with open("subcats.txt") as cats_file:
    for cat in cats_file:
        cat = cat.strip()
        categories.append(cat)

for file in os.listdir():
    if ".html" in file:
        html_files.append(file)

deal_export = []
for file in html_files:
    category = file.split("-")[1]
    with open(file, "rb") as page:
        soup = bs(page, "html.parser")

    deals = soup.find_all("div", class_="cui-content")
    for deal in deals:
        deal_dict = {}

        deal_dict["category"] = category
        title = deal.find("div", class_="cui-udc-title")
        if title:
            title = title.text.strip()
            deal_dict["title"] = title
            location = deal.find("span", class_="cui-location-name")

        else:
            continue

        if "%" in title or "$" in title:
            continue

        if location:
            location = location.text.strip()
            deal_dict["location"] = location
        else:
            continue

        prices_block = deal.find("div", class_="cui-price")
        if prices_block:

            price = prices_block.find_all("div", class_="cui-sr-only")
            if price:

                reg_price = None
                dis_price = None
                dis_perc = None
                for i in price:
                    i = i.text
                    # print(i)

                    if "Regular" in i:
                        reg_price = str(i).replace("Regular price $", "")
                        reg_price = reg_price.replace(",", "")
                        reg_price = float(reg_price)
                        # print(reg_price)

                    elif "Discount" in i:
                        dis_price = str(i).replace("Discount price $", "")
                        dis_price = dis_price.replace(",", "")
                        dis_price = float(dis_price)

                    if dis_price and reg_price:
                        dis_perc = int((dis_price / reg_price) * 100)

                deal_dict["regular_price"] = reg_price if reg_price else None
                deal_dict["discount_price"] = dis_price if dis_price else None
                deal_dict["disc_amt"] = dis_perc

            if "regular_price" not in deal_dict or "discount_price" not in deal_dict:
                deal_dict = {}
                continue

        quick_summary = deal.find("div", class_="cui-udc-subtitle one-line-truncate")

        if quick_summary:
            deal_dict["summary"] = quick_summary.text.strip()

        deal_link = deal.find("a")
        if deal_link:
            link = deal_link["href"]

            deal_dict["link"] = link

        deal_export.append(deal_dict)

deal_export.sort(key=lambda x: x["title"])

dedup_deals = []

for deal in deal_export:
    if deal not in dedup_deals and "regular_price" in deal:
        if not deal["regular_price"]:
            continue
        dedup_deals.append(deal)

with open("deals.csv", "w") as export_file:
    writer = csv.DictWriter(export_file, dedup_deals[0].keys())

    writer.writeheader()
    writer.writerows(dedup_deals)
