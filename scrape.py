import requests
from bs4 import BeautifulSoup as bs
import csv

url = "https://realpython.github.io/fake-jobs/"

page = requests.get(url)

# print(page)

# print(page.text)

# print(page.content)

soup = bs(page.content, "html.parser")

card_content_tags = soup.find_all("div", class_="card-content")
jobs = []

for job in card_content_tags:
    job_info = {}
    job_title = job.find("h2")
    company = job.find("h3", class_="company")
    location = job.find("p", class_="location")
    date_posted = job.find("time")

    footer = job.find("footer")
    links = footer.find_all("a")

    link_href = ""

    for link in links:
        if link.text == "Apply":
            link_href = link["href"]

    detail_page = requests.get(link_href)

    dp_soup = bs(detail_page.content, "html.parser")

    content = dp_soup.find("div", class_="content")

    description = content.find("p")

    if description:
        description = description.text.strip()

    if job_title:
        job_title = job_title.text.strip()
    if company:
        company = company.text.strip()
    if location:
        location = location.text.strip()
    if date_posted:
        date_posted = date_posted.text.strip()

    job_info["job_title"] = job_title
    job_info["company"] = company
    job_info["location"] = location
    job_info["date_posted"] = date_posted
    job_info["link_href"] = link_href
    job_info["description"] = description

    jobs.append(job_info)

print(jobs)

with open("jobs.csv", "w") as jobs_file:

    header = jobs[0].keys()
    wrt = csv.DictWriter(jobs_file, fieldnames=header)
    wrt.writeheader()
    wrt.writerows(jobs)


# print(soup)

# job_titles = soup.find_all("h2")

# print(job_titles)

# for job in job_titles:
#     print(job.text)
