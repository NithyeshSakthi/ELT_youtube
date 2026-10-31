from airflow import DAG
import pendulum
from datetime import datetime, timedelta 
from api.video_stats import get_playlist_id, get_video_ids, extract_video_data, save_to_json

from datawarehouse.dwh import staging_table, core_table
local_tz = pendulum.timezone("Europe/Berlin")
#defining the local time zone
default_args = {
    "owner": "dataengineer",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "dataengineer.com",
    "max_active_runs": 1,
    "dagrun_timeout": timedelta(hours=1),
    "start_date": datetime(2026, 1, 1, tzinfo=local_tz)
}

with DAG(
    dag_id = "json_file",
    default_args = default_args,
    description = "Dag to produe the Json file from the raw",
    schedule = '0 14 * * *',
    catchup = False
)as dag:

    #define dags
    playlist_id = get_playlist_id()
    video_ids = get_video_ids(playlist_id)
    extract_data = extract_video_data(video_ids)
    save_to_json_task = save_to_json(extract_data)

    # define dependencies
    playlist_id >> video_ids >> extract_data >> save_to_json_task


with DAG(
    dag_id = "update_db",
    default_args = default_args,
    description = "Dag to process JSON file & insert data into staging& core schema",
    schedule = '0 14 * * *',
    catchup = False
)as dag:

    #define dags
    update_staging = staging_table()
    update_core = core_table()


    # define dependencies
    update_staging >> update_core