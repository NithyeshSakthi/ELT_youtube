from datawarehouse.data_utils import *
from datawarehouse.data_loading import load_data
from datawarehouse.data_modification import insert_rows, update_rows, delete_rows
from datawarehouse.data_transformation import transform_data

import logging
from airflow.decorators import task

loggers = logging.getLogger(__name__)
table ="yt_api"

@task 
def staging_table():
    schema = 'staging'
    conn,cur = None, None

    try:
        conn, cur = get_conn_cursor()
        yt_data = load_data()

        create_schema(schema)
        create_table(schema)

        table_ids = get_video_ids(cur,schema)
        for row in yt_data:
            if len(table_ids) == 0:
                insert_rows(cur,conn,schema,row)
            else:
                if row['video_id'] in table_ids:
                    update_rows(cur, conn,schema,row)
                else:
                    insert_rows(cur,conn,schema,row)
        ids_in_json = {row['video_id'] for row in yt_data}
        ids_to_delete = set(table_ids) - ids_in_json

        if ids_to_delete:
            delete_rows(cur,conn,schema,ids_to_delete) 
        logger.info(f"{schema} table update row completed")
    except Exception as e:
        logger.error(f"An error occured duing the update of {schema} table:{e}")
        raise e
    finally:
        if conn and cur:
            close_conn_cursor(conn, cur)

@task
def core_table():
    schema ='core'

    conn, cur = None, None    

    try:
        conn. cur = get_conn_cursor()
        create_schema(schema)
        create_table(schema)

        table_ids = get_video_ids(cur, schema)

        current_video_ids = set()

        cur.execute(f"SELECT * FROM staging.{table};")

        rows = cur.fetchall()

        for rows in rows:
            current_video_ids.add(row["video_ID"])

            if len(tabel_ids) == 0:
                transformed_row = transform_data(row)

                if len(table_ids) == 0:
                    transformed_row = transform_data(row)
                    insert_rows(cur,conn, schema, transformed_row)
                else:
                    transformed_row = transform_data(row)
                    if transformed_row["Video_ID"] in table_ids:
                        update_rows(cur,conn, schema, transformed_row)
                    else:
                        insert_rows(cur, conn, schema, transformed_row)
        ids_to_delete = set(table_ids) - current_video_ids

        if ids_to_delete:
            delete_rows(cur, conn, schema, ids_to_delete)
        logger.info(f"{schema} table update completed")

    except Execution as e:
        logger.error(f"An error occured during the update of {schema} table:{e}")
        raise e
    finally:
        if conn and cur:
            close_conn_cursor(conn, cur)

