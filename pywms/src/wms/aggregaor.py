""" Aggregating the data from output files. """
from os import sep
import aiofiles
import pandas
PATHTOFILE = r"C:\Users\alexander.urumtsev\OneDrive - JSC Arcadia Inc\Desktop" \
    "\data-engineer-assignment-python\data\input\articles.tsv"

async with aiofiles.open(PATHTOFILE, mode='r', sep="\t") as f:
    contents = await f.read()

print(contents)
