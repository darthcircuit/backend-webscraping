import csv

categories = []
cat_links = []
url = "https://www.groupon.com/browse/salt-lake-city"

with open("groupon-cats.csv", encoding="utf-8-sig") as cats:
    cat_dict_list = list(csv.DictReader(cats))

    for cat_dict in cat_dict_list:
        for key, val in cat_dict.items():
            if val:
                category = {}
                category[key.lower()] = val.lower()
                categories.append(category)

for i in categories:
    cat, subcat = list(i.items())[0]
    cat_link = f"{url}?category={cat}&subcategory={subcat}\n"
    cat_links.append(cat_link)

with open("groupon_links.txt", "w") as outfile:
    outfile.writelines(cat_links)
