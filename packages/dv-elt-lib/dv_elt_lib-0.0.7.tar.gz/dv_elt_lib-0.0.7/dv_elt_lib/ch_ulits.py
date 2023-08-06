import logging


def insert_df(df, ch_client, dst_path, batch_size=1_000_000, log=logging.getLogger(__name__)):
    size = df.shape[0]
    for ind in range(0, size, batch_size):
        ch_client.insert_dataframe(f"insert into {dst_path} values", df.iloc[ind: ind+batch_size])
        log.info(f"batch of size {min(batch_size, size-ind)} was inserted")



def select_df(ch_client, query, log=logging.getLogger(__name__)):
    return ch_client.query_dataframe(query)