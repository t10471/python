# -*- coding: utf-8 -*-

from pysqlite2 import dbapi2 as sqlite

# データベースに接続(作成)
con = sqlite.connect('test1.db')
# テーブルの列要素: 名前、性別(male or female)、年齢
con.execute('CREATE TABLE people (name TEXT, sex TEXT, age INTEGER)')
# テストデータの挿入(1行はタプルで)
con.execute('INSERT INTO people VALUES ("Taro", "male", 22)')
con.execute('INSERT INTO people VALUES ("Hanako", "female", 38)')
con.execute('INSERT INTO people VALUES ("Ranka", "female", 17)')
con.execute('INSERT INTO people VALUES ("Ozuma", "male", 40)')
con.commit() # DBに反映

# データの検索
cur = con.execute('SELECT * FROM people')
# データの出力
print 'NAMEt  SEXt  AGE'
for row in cur:
    print '%-8s  %-6s  %2d' % row # 1行のデータ構造はタプル
con.close()