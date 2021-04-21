# Picnic Data Integration Assignment (Python)

Please read the following instructions carefully and make sure that you fulfill all
requirements.

## Background

One of the key systems in our operations is the Warehouse Management System (WMS). The Tech team
is integrating against a third-party service for the warehouse management and needs to
quickly load a reasonably realistic test dataset in the system. This will not only speed
up the development and testing but will also help identify any input data issues which
could be fixed at the source. The input data contains all articles offered by the
supplier, not all of which are in our assortment.

## Task

1. Write a small Python application for generating the WMS data.

2. Generate an input file for the WMS with the columns specified in
   [`data/output/wms_load.tsv`][wms_load], selecting precisely the articles in our
   assortment. All fields should have a value, as the system cannot handle nulls.

   In case requirements are not clear please proceed with the implementation based on
   your sound judgment of the underlying data. We are looking for a complete solution
   even if it means that you must make an educated guess to what we are hoping for.

3. During the generation process create column `own_sku` as a derivative of the
   supplier's article id. Make sure that the mapping is a non-trivially reversible
   function (we would like to obscure the supplier's article IDs for our customers). The
   `own_sku` will be used internally in all systems and thus the ID generation process
   should accommodate identifiers from multiple suppliers.

4. There are volume limitations on a single consumer unit imposed by the WMS. In case
   the actual volume exceeds the limit per temperature zone, exclude the record.

   Maximum allowed volumes:

   - `ambient`: 36366 cm<sup>3</sup>
   - `chilled`: 29092 cm<sup>3</sup>
   - `frozen` : 6732 cm<sup>3</sup>

5. Provide a list of:
   - Missing/ambiguous requirements and assumptions made during the solution.
   - Identified data quality issues and corresponding handling strategies.
   - Technical details of the generated file so that the Data team can properly parse it
     (e.g. encoding, column separator, aggregated values separator).

## Considerations

- How will the solution have to be adapted to efficiently process production data
  volumes?
  >We can apply 3 optimization methods like indexing, data compression and chunking.  
- Which design patterns will be applicable in order to deploy the solution in
  production?
  >Because of chuncking we can utilize multiple CPUs. Dask is a great way to do this in production.
- Which software engineering best-practices and design principles can you apply?
   >indexing, data compression, chunking and parallelism.
## Input data

1. Three files provided by the wholesale supplier:

   - [`data/input/articles.tsv`][articles] - articles data, where assortment code
     (`assortm_code`) maps: `1` to `ja`; `2` to `nee`; `3` to `misschien`.
   - [`data/input/consumer_units.tsv`][consumer_units] - consumer EAN units data.
   - [`data/input/trade_units.tsv`][trade_units] - trade EAN units data.

2. One mapping file for the temperature zone
   ([`data/input/temperature_zone.tsv`][temperature_zone])

[articles]: data/input/articles.tsv
[consumer_units]: data/input/consumer_units.tsv
[trade_units]: data/input/trade_units.tsv
[temperature_zone]: data/input/temperature_zone.tsv
[wms_load]: data/output/wms_load.tsv


## Installation

Poetry provides a custom installer that will install `poetry` isolated
from the rest of your system.

### osx / linux / bashonwindows install instructions
```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
```
### windows powershell install instructions
```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py -UseBasicParsing).Content | python -
```

### Run poetry
1. In `bash` or `powershell` navigate to `pywms` folder
``` 
cd ./picnic_dws/pywms
```

2. Install env and run the application
```
poetry install
poetry run app
```