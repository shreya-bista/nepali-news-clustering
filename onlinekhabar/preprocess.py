import json, sys
from nepali_date import NepaliDate
from unicodedata import digit

files = ["onlinekhabar_05112019_1.json", "onlinekhabar_05112019_2.json", "onlinekhabar_05112019_3.json"]
outfile = open("onlinekhabar.json", "w")
ids = set()
cats = set()
cnt = 0
month_map = {u"जेठ": 2, u"असार": 3, u"साउन": 4, u"भदौ": 5, u"वैशाख": 1, u"असोज": 6, u'कात्तिक': 7, u'कार्तिक': 7 }

cat_map = {'bank-main': 'business', 'rojgar': 'business', 'corporate': 'business', 'prabhas-news': 'world', 'generalsports': 'sports', 'football': 'sports', 'technology': 'technology', 'sports-news': 'sports', 'cricket': 'sports', 'ent-news': 'entertainment', 'bolly-hollywood': 'entertainment', 'news': 'news', 'tourism': 'business', 'eco-policy': 'business', 'sports-feature': 'sports'}

for f in files:
    print("reading from ", f)
    with open(f, 'r') as fp:
        for line in fp:
            data = json.loads(line)
            try:
                month = int(data["url"].split("/")[-2])
                id_ = data["id"]
                if month not in {8, 9, 10}:
                    print("filtered out article ", data["url"])
                    continue
                if id_ in ids:
                    print("duplicate ")
                    continue
                date_nep = data["date_nepali"].split()[:3]
                yy = "".join([ str(digit( c )) for c in date_nep[0] ])
                if int(yy) < 2076:
                    print("filtered out article from year ", yy)
                    continue
                dd = "".join([ str(digit( c )) for c in date_nep[2] ])
                mm = month_map[date_nep[1] ]
                nd = NepaliDate(yy, mm, dd, lang='nep')

                # print(date_nep, nd)
                # sys.exit(-1)
                data["date_english"] = nd.to_english_date().strftime("%Y/%-m/%d")
                data["title"] = data["title"].replace(u'\xa0', u' ')
                data["subtitle"] = data["subtitle"].replace(u'\xa0', u' ')
                data["description"] = data["description"].replace(u'\xa0', u' ')
                data["source"] = "onlinekhabar"
                data["category"] = data["category"].split("/")[-1]
                # data['category'] = cat_map[data["category"].split("/")[-1]]
                cats.add(data["category"])
                outfile.write(json.dumps(data) + "\n" )
                ids.add(id_)
                cnt += 1
                if cnt % 100 == 0:
                    print("processed ", cnt, " articles")
            except Exception as ex:
                print(ex, date_nep, nd)

# 

print("processed ", cnt, " articles of categories: ", cats)