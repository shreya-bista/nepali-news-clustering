from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import json, time, sys
import requests
import hashlib
import traceback
import multiprocessing as mp
from urllib.request import Request, urlopen

# https://img.setopati.org/sports?page=3
home_site = "https://img.setopati.org"

def listner(q, path):
    fp = open(path, "w")
    while True:
        m = q.get()
        if m == "kill":
            break
        fp.write(json.dumps(m) + "\n")
        fp.flush()
    fp.close()

def parse_setopati(link):
    r = requests.get(link)
    soup = bs(r.text, 'lxml')
    for script in soup(["script", "style"]):
        script.decompose()
    ls = soup.find(
        "div", class_ = "editor-box"
    )

    res = ls.text
    # hdr = soup.find("div", {"class": "article-header"}).text
    hdr = soup.find( "span", class_ = "news-big-title" ).text
    date = soup.find("span", class_ =  "pub-date").text
    return res, hdr, date

def get_setopati_category(category_name, page, callback = lambda x: print(x)):

    try:
        url = "{}/{}?page={:d}".format(home_site, category_name, page)    # Defining url based on category_name parameter
        # Requesting and parsing the HTML
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        sauce = urlopen(req).read()
        soup = bs(sauce, 'lxml')

        # Indexing the main div that contains a single article
        items = soup.find_all("div", class_ =  "items col-md-6")
        # print(category_name, items)
        for item in items:
                    
            link = item.find("a")["href"]
            try:
                title_ = item.find("a")["title"]
                print(title_, link)
                _id = int(hashlib.sha256(title_.encode('utf-8')).hexdigest(), 16) % 10**8
                date_ = item.find("span", class_ =  "time-stamp").text
                description, hdr, date = parse_setopati(link)
                assert hdr == title_, (hdr, title_)
                # Creating a dictionary
                print(date, date_)
                news = { "id" : "setopati_{}".format(_id),
                        "category" : category_name,
                        "title" : hdr,
                        "date_nepali" : date,
                        "date_english": "",
                        "subtitle" : "",
                        "description": description,
                        "url" : link }
                print("downloaded " + link + " : " + hdr)
                callback(news)
            except Exception as ex:
                print(ex)
                traceback.print_exc()
                callback({"status": "failed", "url": link})
                print("can't download " + link)
    except Exception as ex:
        print(ex)
        traceback.print_exc()
        print(url + " doesn't exist")
    return

# get_setopati_category("sports", 2)
manager = mp.Manager()
q = manager.Queue()
pool = mp.Pool(int(sys.argv[1]))
watcher = pool.apply_async(listner, (q, "setopati_05112019_1.json"))
jobs = []
categories = ['sports', 'politics', 'social', 'art', 'sports', 'global', 'kinmel']
for category_name in categories:
    for page in range(1, 50):
        job = pool.apply_async(get_setopati_category, (category_name, page, q.put))
        jobs.append(job)

for job in jobs:
    job.get()

q.put("kill")
pool.close()