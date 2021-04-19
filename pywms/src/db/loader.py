import os, sys
import sqlite3

import pandas as pd

PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))

PATHTOFILE_AS = PATH + "/data/input/articles.tsv" 
PATHFILE_CU = PATH + "/data/input/consumer_units.tsv"
PATHFILE_TZ = PATH + "/data/input/temperature_zone.tsv"
PATHFILE_TU = PATH + "/data/input/trade_units.tsv"
PATHFILE_WMS = PATH + "/data/output/wms_load.tsv"

db = sqlite3.connect("base.db")

for c in pd.read_csv(PATHTOFILE_AS, chunksize=1000, sep="\t+", engine="python"):
    c.to_sql("articles", db, if_exists="append")

for c in pd.read_csv(PATHFILE_CU, chunksize=1000, sep="\t+", engine="python"):
    c.to_sql("consumer_units", db, if_exists="append")

for c in pd.read_csv(PATHFILE_TZ, chunksize=1000, sep="\t+", engine="python"):
    c.to_sql("temperature_zone", db, if_exists="append")

for c in pd.read_csv(PATHFILE_TU, chunksize=1000, sep="\t+", engine="python"):
    c.to_sql("trade_units", db, if_exists="append")
