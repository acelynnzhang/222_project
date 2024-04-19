import os
import sqlite3

os.remove("database.db")
con = sqlite3.connect("database.db")
cur = con.cursor()
cur.execute("CREATE TABLE comments(class,comment, dateposted)")