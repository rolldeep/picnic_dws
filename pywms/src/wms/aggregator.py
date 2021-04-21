""" Aggregating the data to output file. """
import pandas
import pandas as pd
from hashids import Hashids

from db import PATHFILE_WMS, db

Q = """SELECT
	a.id,
	a.product_type content_unit,
	a.description,
	tz.temperature_zone,
	0 shelf_life,
	a."length" * a."depth" * a.height volume_cm3,
	a.brutto_weight,
	a.unit_of_measure brutto_weight_unit,
	cu.consumer_unit_ean,
    tu.trade_unit_ean content
FROM
	consumer_units cu
LEFT JOIN trade_units tu ON
	tu.sku = cu.sku
LEFT JOIN articles a on
	a.id = cu.sku
left join temperature_zone tz on
	tz."group" = a.product_type
WHERE
	temperature_zone is NOT NULL 
	AND a."length" * a."depth" * a.height is NOT NULL 
	AND a.brutto_weight is NOT NULL
	AND a.assortm_code = 1 ;
"""
__all__ = ["get_output"]

def get_output():
    df_base = pd.read_sql_query(Q, db)

    """colapsing ean_list
	"""
    df_collapsed = df_base.groupby(['id', 'content_unit', 'description', 'temperature_zone', 'shelf_life',
                                    'volume_cm3', 'brutto_weight', 'brutto_weight_unit',
                                    'content']).apply(lambda x: set(x['consumer_unit_ean'].values)).reset_index()
    df_collapsed.rename(columns={0: 'ean_list'}, inplace=True)

    """applying fit conditions
	"""
    df_ambient = df_collapsed[df_collapsed['temperature_zone'] == 'ambient']
    df_chilled = df_collapsed[df_collapsed['temperature_zone'] == 'chilled']
    df_frozen = df_collapsed[df_collapsed['temperature_zone'] == 'diepvries']
    df_ambient = df_ambient[df_ambient['volume_cm3'] <= 36366.0]
    df_chilled = df_chilled[df_chilled['volume_cm3'] <= 29092.0]
    df_frozen = df_frozen[df_frozen['volume_cm3'] <= 6732.0]
    df_union = pd.concat(
        [df_ambient, df_chilled, df_frozen], ignore_index=True)
    # Ask data owners about mesures
    df_union['volume_mm3'] = df_union['volume_cm3'] * 1000

    """creating own_sku
	"""
    hashids = Hashids()
    hashids = Hashids(salt='secret')
    df_union['own_sku'] = df_union['id'].apply(lambda x: hashids.encode(x))
    df_union.drop(columns=['id', 'volume_cm3'], inplace=True)

    """writing to the output file
    """
    df_wms = pd.read_csv(PATHFILE_WMS,
                         sep='\t+',
                         engine='python')
    df_wms = df_wms.iloc[0:0]
    df_wms = pd.concat([df_wms, df_union])
    df_wms.to_csv(PATHFILE_WMS, sep='\t')

if __name__ == "__main__":
	get_output()