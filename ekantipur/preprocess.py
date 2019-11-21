import json

files = ["ekantipur_082019.json", "ekantipur_092019.json", "ekantipur_102019.json"]
outfile = open("ekantipur.json", "w")
ids = set()
cnt = 0
cats = set()

for f in files:
    print("reading from ", f)
    with open(f, 'r') as fp:
        for line in fp:
            data = json.loads(line)
            try:
                month = int(data["date_english"].split("/")[1])
                id_ = data["id"]
                if month not in {8, 9, 10}:
                    print("filtered out article from ", data["date_english"])
                    continue
                if id_ in ids:
                    print("duplicate ")
                    continue

                data["title"] = data["title"].replace(u'\xa0', u' ')
                data["subtitle"] = data["subtitle"].replace(u'\xa0', u' ')
                data["description"] = data["description"].replace(u'\xa0', u' ')
                data["source"] = "ekantipur"
                cats.add(data["category"])
                outfile.write(json.dumps(data) + "\n" )
                ids.add(id_)
                cnt += 1
                if cnt % 100 == 0:
                    print("processed ", cnt, " articles")
            except:
                pass

print(cats)