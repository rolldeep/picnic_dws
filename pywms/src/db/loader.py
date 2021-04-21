import os
import sqlite3
import sys

import pandas as pd

PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))

PATHTOFILE_AS = PATH + "/data/input/articles.tsv"
PATHFILE_CU = PATH + "/data/input/consumer_units.tsv"
PATHFILE_TZ = PATH + "/data/input/temperature_zone.tsv"
PATHFILE_TU = PATH + "/data/input/trade_units.tsv"
PATHFILE_WMS = PATH + "/data/output/wms_load.tsv"
PATH_DB = PATH + "/data/output/base.db"

db = sqlite3.connect(PATH_DB)

__all__ = ["db", "PATHFILE_WMS"]
def fill_db():
    db.execute("TRUNCATE TABLE articles")
    db.execute("TRUNCATE TABLE consumer_units(sku)")
    db.execute("TRUNCATE TABLE temperature_zone(\"group\")")

    for c in pd.read_csv(PATHTOFILE_AS, chunksize=1000, sep="\t+", engine="python"):
        c.to_sql("articles", db, if_exists="append")

    for c in pd.read_csv(PATHFILE_CU, chunksize=1000, sep="\t+", engine="python"):
        c.to_sql("consumer_units", db, if_exists="append")

    for c in pd.read_csv(PATHFILE_TZ, chunksize=1000, sep="\t+", engine="python"):
        c.to_sql("temperature_zone", db, if_exists="append")

    """ Creat indexes

    Index is allowing us to quickly search and join tables in the database faster. 
    """

    db.execute("CREATE INDEX street ON articles(id)")
    db.execute("CREATE INDEX street ON articles(product_type)")
    db.execute("CREATE INDEX street ON consumer_units(sku)")
    db.execute("CREATE INDEX street ON temperature_zone(\"group\")")
    db.close()


if __name__ == "__main__":
    fill_db()
