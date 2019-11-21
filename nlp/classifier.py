import json
from fasttext.FastText import load_model, tokenize
import numpy as np

model = load_model('/opt/installed/var/models/cc.ne.300.bin')

def main():
    with open("../combined.json", 'r') as f:
        for line in f:
            tokens = tokenize(json.loads(line)["title"])
            print(np.sum([model.get_word_vector(x) for x in tokens], axis = 0 ))

if __name__ == "__main__":
    main()