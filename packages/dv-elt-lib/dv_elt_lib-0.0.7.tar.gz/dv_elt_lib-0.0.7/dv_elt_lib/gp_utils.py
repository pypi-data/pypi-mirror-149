import logging
import pandas as pd
import numpy as np

from datetime import datetime


def _insert_batch_df(df, conn, table, log=logging.getLogger(__name__)):
    """
    Insert pandas dataframe to table
    :param df: dataframe to insert
    :param conn: pg/gp connection
    :param table: target table name
    :return:
    """
    cursor = conn.cursor()
    cols = df.columns.tolist()
    values = [cursor.mogrify("(%s)" % ','.join('%s' for _ in cols), tup).decode('utf8') for tup in
              df.itertuples(index=False)]
    query = "INSERT INTO %s(%s) VALUES " % (table, ','.join(cols)) + ",".join(values)
    cursor.execute(query)
    conn.commit()
    cursor.close()


def insert_df(df, conn, table, batch_size=1_000_000, log=logging.getLogger(__name__)):
    """
    Insert data from pandas dataframe into table in batch mode'
    :param df: dataframe to insert
    :param conn: pg/gp connection
    :param table: target table name
    :param batch_size: batch size
    :return:
    """
    size = df.shape[0]
    for ind in range(0, size, batch_size):
        _insert_batch_df(df.iloc[ind:ind + batch_size], conn, table, log=log)
        log.info(f"batch of size {min(batch_size, size-ind)} was inserted")


_type_map = {
    'int8': (np.int64,),
    'int4': (np.int64,),
    'text': (np.unicode_, 1024),
    '_text': (list,),
    'bpchar': (np.unicode_, 1024),
    'varchar': (np.unicode_, 1024),
    'timestamp': (datetime,),
    'float4': (np.float64,),
    'float8': (np.float64,),
    '_varchar': (list,)
}
def __get_types(oids, cur):
    cur.execute(f"select oid, typname from pg_type where oid in ({','.join(map(str, oids))});")
    rows = cur.fetchall()
    data = {oid: _type_map[type_name] for oid, type_name in rows}
    return data


def select_df(conn, query, batch_size=1_000_000, log=logging.getLogger(__name__), use_dtypes=True):
    cur = conn.cursor()
    cur.execute(f"DECLARE cursor CURSOR FOR ({query});")

    def fetch_df(cur, use_dtypes):
        cur.execute(f"""FETCH FORWARD {batch_size} FROM cursor;""")
        rows = cur.fetchall()
        log.info(f"batch of size {len(rows)} was selected")
        columns = [desc[0] for desc in cur.description]
        if use_dtypes:
            oids = [desc[1] for desc in cur.description]
            types = __get_types(oids, cur)
            data = np.array(rows, dtype=[(col, *types[oid]) for col, oid in zip(columns, oids)])
        else:
            data = rows
        return pd.DataFrame(data, columns=columns)
    dfs = []
    _df = fetch_df(cur, use_dtypes=use_dtypes)
    while _df.shape[0] != 0:
        dfs.append(_df)
        _df = fetch_df(cur, use_dtypes=use_dtypes)
    if len(dfs) == 0:
        return pd.DataFrame()
    return pd.concat(dfs, axis=0)


def select_df_generator(conn, query, batch_size=1_000_000, log=logging.getLogger(__name__), use_dtypes=True):
    cur = conn.cursor()
    cur.execute(f"DECLARE cursor CURSOR FOR ({query});")

    def fetch_df(cur, use_dtypes):
        cur.execute(f"""FETCH FORWARD {batch_size} FROM cursor;""")
        rows = cur.fetchall()
        log.info(f"batch of size {len(rows)} was selected")
        columns = [desc[0] for desc in cur.description]
        if use_dtypes:
            oids = [desc[1] for desc in cur.description]
            types = __get_types(oids, cur)
            data = np.array(rows, dtype=[(col, *types[oid]) for col, oid in zip(columns, oids)])
        else:
            data = rows
        return pd.DataFrame(data, columns=columns)
    _df = fetch_df(cur, use_dtypes=use_dtypes)
    while _df.shape[0] != 0:
        yield _df
        _df = fetch_df(cur, use_dtypes=use_dtypes)
