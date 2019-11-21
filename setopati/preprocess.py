import json, traceback
from nepali_date import NepaliDate
from unicodedata import digit

files = ["setopati_05112019_1.json"]
outfile = open("setopati.json", "w")
ids = set()
cats = set()
cnt = 0
month_map = {u"जेठ": 2, u"असार": 3, u"साउन": 4, u"भदौ": 5, u"वैशाख": 1, u"असोज": 6, u'कात्तिक': 7 }

for f in files:
    print("reading from ", f)
    with open(f, 'r') as fp:
        for line in fp:
            data = json.loads(line)
            try:
                date_nep = data["date_nepali"].split(",")[1:3]
                # print(nd)
                yy = "".join([ str(digit( c )) for c in date_nep[1][1:]])
                if int(yy) < 2076:
                    print("filtered out article from year ", yy)
                    continue
                dd = "".join([ str(digit( c )) for c in date_nep[0].strip().split(' ')[1] ])
                mm = month_map[date_nep[0].strip().split(' ')[0] ]
                nd = NepaliDate(yy, mm, dd, lang='nep')
                # print(yy, mm, dd, nd, , )
                d_eng = nd.to_english_date()
                month = d_eng.month
                id_ = data["id"]
                if month not in {8, 9, 10}:
                    print("filtered out article ", data["url"])
                    continue
                if id_ in ids:
                    print("duplicate ")
                    continue
                data["date_english"] = d_eng.strftime("%Y/%-m/%d")
                data["title"] = data["title"].replace(u'\xa0', u' ')
                data["subtitle"] = data["subtitle"].replace(u'\xa0', u' ')
                data["description"] = data["description"].replace(u'\xa0', u' ')
                data["source"] = "setopati"
                data["category"] = data["category"]
                cats.add(data["category"])
                outfile.write(json.dumps(data) + "\n" )
                ids.add(id_)
                cnt += 1
                if cnt % 100 == 0:
                    print("processed ", cnt, " articles")
            except Exception as ex:
                print(ex, data.get("date_nepali", "NA"))
                # traceback.print_exc()
                pass
            # assert 1 == 2
print("processed ", cnt, " articles of categories: ", cats)