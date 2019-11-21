## 1. Crawling

Nepali news website crawling using python. Following python requirements can be installed as:
```
pip install beautifulsoup4 nepali-date lxml
```

or install using:

```
chmod +x install.sh
./install.sh
```
This install every required library(defined in `environment.yml`) in a new conda environment `project` ([requires miniconda](https://docs.conda.io/en/latest/miniconda.html)) for crawler and NLP stuffs. Once installation is complete, use command:
```
source activate project
```

The scripts to download and filter news articles are explained below. The files are compressed by `gzip` commnand. To uncompress use `gunzip`, e.g. `gunzip combined.json.gz`
 
### 1.1 Ekantipur

```
python ekantipur/crawler.py N_PROC MONTH_NUM
```

crawls from [**ekantipur.com**](ekantipur.com) by spawning N_PROC processes for year 2019 and month number specified by MONTH_NUM (e.g `python crawler.py 4 8` crawls with 4 processes for august). To change year, modify in `crawler.py` 

A file is created for each month.

### 1.2 Onlinekhabar

```
python onlinekhabar/crawler.py N_PROC
```

crawls from [**onlinekhabar.com**](onlinekhabar.com) by spawning N_PROC processes. By default, 50 page is crawled for each category of news, it can be changed in script. (e.g `python crawler.py 4` crawls with 4 processes). 

A single file is created for all data.

### 1.3 Setopati

```
python setopati/crawler.py N_PROC
```

crawls from [**setopati.com**](setopati.com) by spawning N_PROC processes. By default, 50 page is crawled for each category of news, it can be changed in script. (e.g `python crawler.py 4` crawls with 4 processes). 

A single file is created for all data.

## 2. Preprocessing
In this, I have implemented a `preprocess.py`. It filters out duplicates, failed downloads and articles other than from 2019 august to october. You can change `preprocess.py` inside `onlinekhabar\`, `ekantipur\`, `setopati\` to your requirements.

All these files are combined into single file `combined.json.gz`. This contains news articles from aug-oct 2019 from these three articles.

## News classifier and other NLP stuffs
TODO

## TODO
- add [nagariknews.com](nagariknews.com) - contributions welcome :) .