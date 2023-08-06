
# json_stock [json_stock]

import sys
from sout import sout
from ezpip import load_develop
# json_stock [json_stock]
jst = load_develop("json_stock", "../", develop_flag = True)

# open DB
test_db = jst.JsonStock("./test_db/")
print(test_db)
# create table
test_db["test_table"] = {}
# get table
test_table = test_db["test_table"]
print(test_table)
# create new value
test_table["test"] = {"hello": "world!!"}
# read value
print(test_table["test"])
# iterate (listup all keys in the table)
print([key for key in test_table])
# delete value
del test_table["test"]
# delete table
del test_db["test_table"]
