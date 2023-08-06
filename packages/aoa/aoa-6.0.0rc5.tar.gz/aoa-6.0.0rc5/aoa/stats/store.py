import json
import pandas as pd
from typing import Dict

from teradataml import get_connection, DataFrame

ct_query = """
CT {} (
    column_name VARCHAR(128), 
    stats JSON, 
    update_ts TIMESTAMP)
UNIQUE PRIMARY INDEX ( column_name );
"""

merge_query = """
MERGE {} target
     USING {} source
       ON target.column_name = source.column_name
     WHEN MATCHED THEN
       UPD SET stats = source.stats, update_ts = source.update_ts
     WHEN NOT MATCHED THEN
       INS (source.column_name, source.stats, source.update_ts);
"""
temp_table = "aoa_stats_temp"


def save_feature_stats(features_table, stats: Dict, **kwargs):
    conn = get_connection()
    conn.execute(
        f"CREATE VOLATILE TABLE {temp_table} AS {features_table} WITH NO DATA ON COMMIT PRESERVE ROWS;")
    conn.execute(f"INS {temp_table} (?,?,CURRENT_TIMESTAMP);", [
                 [f, json.dumps(stats[f])] for f in stats])
    conn.execute(merge_query.format(features_table, temp_table))
    conn.execute(f"DROP TABLE {temp_table};")


def get_feature_stats(features_table):
    fs = DataFrame.from_query(f"SEL * FROM {features_table}")
    fs = fs.to_pandas().reset_index()
    fs = fs.drop(fs.columns.difference(["column_name", "stats"]), axis=1)
    fs = fs.set_index("column_name")
    fs = pd.Series(fs.stats).to_dict()
    return {k: json.loads(fs[k]) for k in fs}


def create_features_stats_table(features_table):
    conn = get_connection()
    conn.execute(ct_query.format(features_table))