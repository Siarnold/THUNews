# THUNews
Spider for crawling http://news.tsinghua.edu.cn/

## Setup

```
pip install -r requirements.txt
```

## Run spider

```
cd thuspider
scrapy crawl thuspider -o ../data.db -t sqlite
```
