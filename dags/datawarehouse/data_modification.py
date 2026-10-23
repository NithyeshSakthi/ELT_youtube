import logging

logger = logging.getLogger(__name__)
table="yt_api"

def insert_rows(cur, conn, schema, row):

    try:

        if schema == 'staging':
            video_id = "video_id"
            cur.execute(
                f""" 
                INSERT INTO {schema}.{table}("Video_ID", "Video_Title","Upload_Date", "Duration", "Video_Views", "Likes_Count","Comments_Count")
                VALUES(%(video_id)s, %(title)s,%(publishedAt)s,%(duration)s,%(viewCount)s,%(likeCount)s,%(commentCount)s);
                """, row
            )
        else:
            video_id = 'video_Id'
            cur.execute(
                f""" 
                INSERT INTO {schema}.{table}("Video_ID", "Video_Title","Upload_Date", "Duration", "Video_Views", "Likes_Count","Comments_Count")
                VALUES(%(video_id)s, %(title)s,%(publishedAt)s,%(duration)s,%(viewCount)s,%(likeCount)s,%(commentCount)s);
                """, row
            )
        conn.commit()

        logger.info(f"Inserted row with Video_ID: {row[video_id]}")

    except Exception as e:
        logger.error(f"Error inserting row with Video_ID: {row[video_id]}")
        raise e

def update_rows(cur, conn, schema, row):
    try:
        if schema == 'staging':
            video_id = 'video_id'
            upload_date = 'publishedAT'
            video_title = 'title'
            video_view = "viewCount"
            likes_count = 'likeCount'
            comments_count = 'commnetCount'

        else:
            video_id = 'video_id'
            upload_date = 'Upload_Date'
            video_title = 'Video_Title'
            video_views = "Video_Views"
            likes_count = 'likes_Count'
            comments_count = 'comments_Count'            
        cur.execute(
            f"""
            UPDATE {schema}.{table}
            SET "Video_Title" = %({video_title})s,
                "Video_Views" = %({video_views})s,
                "Likes_Count" = %({likes_count})s,
                "Comments_Count" = %({comments_count})s
            WHERE "video_ID" = %({video_id})s AND "Upload_Date" = %({upload_date})s;

            """,
            row,
        )

        conn.commit()
        logger.info(f"Updated row with Video_ID: {row[video_id]}")

    except Exception as e:
        logger.error(f"Error updating row with Video_ID: {row[video_id]} - {e}")
        raise e
def delete_rows(cur, conn, schema, ids_to_delete):
    try :
        ids_to_delete = f"""({', '.join(f"'{id}'" for id in ids_to_delete)})"""
        cur.execute(
            f"""
            DELETE FROM {schema}.{table}
            WHERE "Video_ID" IN {ids_to_delte};

            """
        )

        conn.commit()
        logger.info(f"Delete rows with Video_IDs: {ids_to_delete}")
    except Exception as e:
        logger.error(f"Error deleting rows with Video_IDs: {ids_to_delte} -{e}")
        raise e