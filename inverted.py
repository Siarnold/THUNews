# coding: utf-8

import sqlite3
import jieba

TABLE_NAME = 'inverted'
FILE_NAME = 'data.db'
STOPWORDS_FILE = 'stopwords.txt'

COLUMNS = ('word', 'in_title', 'in_content')

jieba.enable_parallel(8)
with open(STOPWORDS_FILE) as f:
    stopwords = [line.strip('\n').decode('utf-8') for line in f]

def check_valid(word):
    word = word.lower()
    return word.strip() and word not in stopwords and word not in COLUMNS

def update_or_insert(src, target, news_id):
    for word in set(filter(check_valid, jieba.cut_for_search(src))):
        sql = 'select count(*) from inverted where word="%s"' % word
        count = conn.execute(sql).next()[0]
        if count:
            if count > 1:
                print("WARNING: %d rows selected for %s" % (count, word))
            sql = 'select %s from inverted where word="%s"' % (target, word)
            id_list = eval(conn.execute(sql).next()[0])
            if news_id not in id_list:
                id_list.append(news_id)
                sql = 'update inverted set %s="%s" where word="%s"' % (
                    target, repr(id_list), word
                )
                conn.execute(sql)
        else:
            if target == 'in_title':
                sql = 'insert into inverted values ("%s", "[%d]", "[]")' % (
                    word, news_id)
            elif target == 'in_content':
                sql = 'insert into inverted values ("%s", "[]", "[%d]")' % (
                    word, news_id)
            conn.execute(sql)

conn = sqlite3.connect(FILE_NAME)

sql = 'drop table if exists [%s]' % TABLE_NAME
conn.execute(sql)
conn.commit()

sql = 'create table if not exists [%s]' % TABLE_NAME
column_define = ['[%s] text' % c for c in COLUMNS]
primary_key = 'primary key (%s)' % 'word'
column_define.append(primary_key)
sql += '(%s)' % ', '.join(column_define)
conn.execute(sql)
conn.commit()

rows = conn.execute('select * from ThuSpiderItem')
column_names = list(map(lambda x: x[0], rows.description))
idx_id = column_names.index('news_id')
idx_title = column_names.index('title')
idx_content = column_names.index('content')
total = conn.execute('select count(*) from ThuSpiderItem').next()[0]
for i, row in enumerate(rows):
    news_id = int(row[idx_id])
    title = row[idx_title]
    content = row[idx_content]

    update_or_insert(title, 'in_title', news_id)
    update_or_insert(content, 'in_content', news_id)

    conn.commit()
    print("%d/%d" % (i + 1, total))

conn.close()
