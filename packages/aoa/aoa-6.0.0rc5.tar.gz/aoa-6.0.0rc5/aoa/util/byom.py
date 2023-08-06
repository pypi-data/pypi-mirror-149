from teradataml import DataFrame


def store_byom_tmp(context, table: str, model_version: str, model_bytes: bytes):
    """
    Store a byom model in a temporary table so we can use it

    :param context: get_context()
    :param table: temp table name to use
    :param model_version: model version
    :param model_bytes: model bytes
    :return: DataFrame of model
    """
    context.execute(f"""
        CREATE VOLATILE TABLE {table}(
            model_version VARCHAR(255),
            model_id VARCHAR(255),
            model BLOB(2097088000)
        ) ON COMMIT PRESERVE ROWS;
        """)

    context.execute(f"INSERT INTO {table}(model_version, model) values(?,?)",
                    (model_version, model_bytes))

    return DataFrame.from_query(f"""
        SELECT model_version as model_id, model FROM {table} 
            WHERE model_version='{model_version}'
        """)


def check_if_table_exists(context, database: str, name: str, table_kind: str):
    """
    Check if the table/view/etc exists in the database

    :param context: sqlalchemy context/engine
    :param database: the database
    :param name: the table/view/etc name
    :param table_kind: 'V' for view, 'T' for table etc
    :return: (bool) True if exists, False otherwise
    """
    rs = context.execute(f"""
    SELECT * FROM DBC.TABLES WHERE 
        TABLENAME ='{name}' AND 
        tablekind = '{table_kind}' AND 
        databasename='{database}'
    """)

    return rs.rowcount >= 1
