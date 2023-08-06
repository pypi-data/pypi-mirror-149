
import os
import sys
import fies
import json
import hashlib
from sout import sout

# DBディレクトリが存在しないときに作成
def make_db_dir(db_dir):
	# ディレクトリが存在しない場合に作成
	if os.path.exists(db_dir) is False: os.mkdir(db_dir)
	# 索引が存在しない場合に作成
	index_filename = os.path.join(db_dir, "index.json")
	if os.path.exists(index_filename) is False:
		fies[index_filename] = {}
	# dataディレクトリが存在しない場合に作成
	data_dir = os.path.join(db_dir, "data")
	if os.path.exists(data_dir) is False: os.mkdir(data_dir)

# key文字列をhashに変換
def gen_hash(table_name, key):
	# 2値をつなげた文字列を作成
	dkey_obj = [table_name, key]
	dkey = json.dumps(dkey_obj, ensure_ascii = False)
	# ハッシュ化
	bin_dkey = dkey.encode()
	hash_key = hashlib.sha256(bin_dkey).hexdigest()
	return hash_key

# テーブルクラス
class Table:
	# 初期化処理
	def __init__(self, table_name, db):
		self.table_name = table_name
		self.db = db	# 属しているDB
	# valueの読み出し (Read)
	def __getitem__(self, key):
		# 存在するかどうかを確認
		if key not in self:
			raise Exception("[json_stock error] The key '%s' does not exist."%key)
		# 値のファイルの読み出し
		hash_key = gen_hash(self.table_name, key)	# key文字列をhashに変換
		filename = "%s.json"%hash_key
		return fies[self.db.db_dir]["data"][filename]
	# valueの新規作成/上書き (Create / Update)
	def __setitem__(self, key, value):
		# 値のファイルの作成 or 上書き
		hash_key = gen_hash(self.table_name, key)	# key文字列をhashに変換
		filename = "%s.json"%hash_key
		fies[self.db.db_dir]["data"][filename] = value
		# 新規作成の場合のみ索引登録
		if key not in self:
			index = fies[self.db.db_dir]["index.json"]
			index[self.table_name][key] = True
			fies[self.db.db_dir]["index.json"] = index
	# keyの存在確認
	def __contains__(self, key):
		# 索引を調べる
		index = fies[self.db.db_dir]["index.json"]
		# 存在するかどうかを返す
		return (key in index[self.table_name])
	# valueの削除 (Delete)
	def __delitem__(self, key):
		# 存在するかどうかを確認
		if key not in self:
			raise Exception("[json_stock error] The key '%s' does not exist."%key)
		# 索引から削除
		index = fies[self.db.db_dir]["index.json"]
		del index[self.table_name][key]
		fies[self.db.db_dir]["index.json"] = index
		# 値のファイルの削除
		hash_key = gen_hash(self.table_name, key)	# key文字列をhashに変換
		filename = os.path.join(self.db.db_dir, "data",
			"%s.json"%hash_key)
		os.remove(filename)
	# keyのイテレート (for 文脈への対応)
	def __iter__(self):
		# 索引を利用
		index = fies[self.db.db_dir]["index.json"]
		for key in index[self.table_name]:
			yield key
	# 文字列化
	def __str__(self):
		return "<json_stock Table '%s' (%d records)>"%(
			self.table_name, len(self))
	# 文字列化_その2
	def __repr__(self):
		return str(self)
	# レコード数
	def __len__(self):
		# 索引から調べる
		index = fies[self.db.db_dir]["index.json"]
		return len(index[self.table_name])

# データベースクラス
class JsonStock:
	# 初期化処理
	def __init__(self, db_dir):
		# DBディレクトリが存在しないときに作成
		make_db_dir(db_dir)
		self.db_dir = db_dir
	# 新規テーブル作成
	def __setitem__(self, table_name, value):
		# すでにテーブルが存在する場合
		if table_name in self:
			raise Exception("[json_stock error] Creation of new table failed. (The table '%s' already exists.)"%table_name)
		# value が空辞書出ない場合
		if value != {}:
			raise Exception("[json_stock error] Creation of new table failed. (Value must be an empty dictionary like '{{}}'.)")
		# 新規テーブル登録
		index = fies[self.db_dir]["index.json"]
		index[table_name] = {}
		fies[self.db_dir]["index.json"] = index
	# テーブルの取得
	def __getitem__(self, table_name):
		# テーブルの存在確認
		if table_name not in self:
			raise Exception("[json_stock error] The table '%s' does not exist."%table_name)
		# テーブルオブジェクトを返す
		return Table(table_name, db = self)
	# テーブルの存在確認
	def __contains__(self, table_name):
		# 索引を取得
		index = fies[self.db_dir]["index.json"]
		return (table_name in index)
	# tableの削除 (Delete)
	def __delitem__(self, table_name):
		# 存在するかどうかを確認
		if table_name not in self:
			raise Exception("[json_stock error] The table '%s' does not exist."%table_name)
		# テーブルに残存するレコードをすべて削除
		table = self[table_name]
		for key in table: del table[key]
		# 索引から削除
		index = fies[self.db_dir]["index.json"]
		del index[table_name]
		fies[self.db_dir]["index.json"] = index
	# tableのイテレート (for 文脈への対応)
	def __iter__(self):
		# 索引を利用
		index = fies[self.db_dir]["index.json"]
		for table_name in index:
			yield table_name
	# 文字列化
	def __str__(self):
		return "<json_stock DB (%d tables)>"%len(self)
	# 文字列化_その2
	def __repr__(self):
		return str(self)
	# テーブル数
	def __len__(self):
		# 索引の規模
		index = fies[self.db_dir]["index.json"]
		return len(index)
