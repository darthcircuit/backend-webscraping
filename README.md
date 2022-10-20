# backend-webscraping

I wanted to get more deals than the 6 or 7 that would load upon requesting the page. I couldn't figure out how to get page scrolling to work with python requests, so I just wrote a program (get_links.py) that will generate full url's for every category in groupon salt lake city.

Then, we can take that list of urls and download local copies, and then finally scrape the data pulled and save to a usable csv.

I also included some filtering to get rid of groupon's ad listings that didn't contain any pricing data.

this should work for any area groupon supports by changing the base url to another city's base url in get_links.py and then running that file.

# Running

local copies of html pages can be obtained through running:
`python download_page.py`

one all pages are scraped and saved into local folder, running:
`python groupon.py`

will build a csv file with all the deals from pulled groupon categories.
