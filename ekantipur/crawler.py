from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import json, time, sys
import requests
import hashlib
import traceback
import multiprocessing as mp

home_site = "https://ekantipur.com"

def listner(q, path):
    fp = open(path, "w")
    while True:
        m = q.get()
        if m == "kill":
            break
        fp.write(json.dumps(m) + "\n")
        fp.flush()
    fp.close()

def clean_text_nepali(str):
    str = str.replace(u"\u202f", " ").replace(u"\xa0", "")
    return str

def parse_ekantipur(link):
    r = requests.get(link)
    soup = bs(r.text, 'lxml')
    for script in soup(["script", "style"]):
        script.decompose()
    ls = soup.find("main").find("article", {"class" : "normal"}).find(
        "div", {"class" : "row"}).find(
        "div", {"class" : "col-xs-10 col-sm-10 col-md-10"}).find(
        "div", {"class" : "description"}
    )
    res = ls.text.split("Share on Facebook")[0]
    hdr = soup.find("div", {"class": "article-header"}).text
    
    try:
        sub_desc = soup.find("div", {"class": "sub-headline"}).text
    except:
        sub_desc = ''
    date = soup.find("time").text
    return res, hdr, sub_desc, date

def get_ekantipur_category(category_name, yy, mm, dd, callback = lambda x: x):
    # outfile = open('ekantipur_{}_{}.json'.format(category_name, date), 'w')
    # outfile = open("ekantipur_{}{}{}.json".format(yy, mm, dd), "w")
    # for category_name in categories:
    try:
        url = "{}/{}/{}/{}/{:02d}".format(home_site, category_name, yy, mm, dd)    # Defining url based on category_name parameter
        
        print(url)

        # Requesting and parsing the HTML
        data = urlopen(url)
        sauce = data.read()
        soup = bs(sauce, 'lxml')

        # Indexing the main div that contains a single article
        items = soup.find_all("article")

        for item in items:
            if item:
                
                if item.h1:
                    item = item.h1
                elif item.h2:
                    item = item.h2
                else:
                    item = item.h3
                    
                title = item.find("a", {"data-type": "title"})
                title = title if title else item.find("a")
                link = home_site + title['href']
                try:
                    description, hdr, sub_desc, date = parse_ekantipur(link)
                    # Creating a dictionary
                    _id = int(hashlib.sha256(hdr.encode('utf-8')).hexdigest(), 16) % 10**8
                    news = { "id" : "ekantipur_{}".format(_id),
                         "category" : category_name,
                         "title" : hdr,
                         "date_nepali" : date,
                         "date_english": "{}/{}/{:02d}".format(yy, mm, dd),
                         "subtitle" : sub_desc,
                         "description": description,
                         "url" : link}
                    print("downloaded " + link + " : " + hdr)
                    callback(news)
                except Exception as ex:
                    # print(ex)
                    # traceback.print_exc()
                    callback({"status": "failed", "url": link})
                    print("can't download " + link)
        #outfile.close()
    except:
        print(url + " doesn't exist")
    
    return

manager = mp.Manager()
q = manager.Queue()
pool = mp.Pool(int(sys.argv[1]))
yy = 2019
mm = int(sys.argv[2])
watcher = pool.apply_async(listner, (q, "ekantipur_{:02d}{}.json".format(mm, yy)))
jobs = []
categories = ['world', 'news', 'business', 'sports', 'national', 'entertainment', 'technology', 'health']
for category_name in categories:
    for day in range(1, 32):
        job = pool.apply_async(get_ekantipur_category, (category_name, yy, mm, day, q.put))
        jobs.append(job)

for job in jobs:
    job.get()

q.put("kill")
pool.close()
