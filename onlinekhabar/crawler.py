from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import json, time, sys
import requests
import hashlib
import traceback
import multiprocessing as mp
from urllib.request import Request, urlopen

home_site = "https://www.onlinekhabar.com"

def listner(q, path):
    fp = open(path, "w")
    while True:
        m = q.get()
        if m == "kill":
            break
        fp.write(json.dumps(m) + "\n")
        fp.flush()
    fp.close()

def parse_onlinekhabar(link):
    r = requests.get(link)
    soup = bs(r.text, 'lxml')
    for script in soup(["script", "style"]):
        script.decompose()
    ls = soup.find(
        "div", class_ = "col colspan3 main__read--content ok18-single-post-content-wrap"
    )

    res = ls.text
    # hdr = soup.find("div", {"class": "article-header"}).text
    hdr = soup.find( "h2", class_ = "mb-0" ).text
    
    date = soup.find("div", class_ =  "post__time").text
    return res, hdr, date

def get_onlinekhabar_category(category_name, page, callback = lambda x: print(x)):

    try:
        url = "{}/{}/page/{:d}".format(home_site, category_name, page)    # Defining url based on category_name parameter
        # Requesting and parsing the HTML
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        sauce = urlopen(req).read()
        soup = bs(sauce, 'lxml')

        # Indexing the main div that contains a single article
        items = soup.find_all("a", class_ =  "title__regular")
        # print(category_name, items)
        for item in items:
                    
            title_ = item.text
            link = item["href"]
            print(title_, link)
            _id = int(hashlib.sha256(title_.encode('utf-8')).hexdigest(), 16) % 10**8
            try:
                description, hdr, date = parse_onlinekhabar(link)
                assert hdr == title_, (hdr, title_)
                # Creating a dictionary
                news = { "id" : "onlinekhabar_{}".format(_id),
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
        print(url + " doesn't exist")
    return

manager = mp.Manager()
q = manager.Queue()
pool = mp.Pool(int(sys.argv[1]))
watcher = pool.apply_async(listner, (q, "onlinekhabar_05112019_99.json"))
jobs = []
categories = ['content/news', 'content/business/technology', 'content/prabhas-news', 
'content/eco-policy', 'content/tourism', 'content/bank-main', 'content/biz-talk', 
'content/corporate', 'content/rojgar', 'content/ent-news', 'content/bolly-hollywood', 
'content/sports-news', 'content/cricket', 'content/football', 'content/sports-feature', 'content/generalsports']
for category_name in categories:
    for page in range(1, 50):
        job = pool.apply_async(get_onlinekhabar_category, (category_name, page, q.put))
        jobs.append(job)

for job in jobs:
    job.get()

q.put("kill")
pool.close()
