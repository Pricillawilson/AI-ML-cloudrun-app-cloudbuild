from google.cloud import bigquery
from flask import Flask
from flask import request
import os 

app = Flask(__name__)
def get_bigquery_client():
    return bigquery.Client()
# client = bigquery.Client()

@app.route('/')
# client = get_bigquery_client()
def main():
    big_query_client = get_bigquery_client()
    table_id = "ml-project-161098.test_schema.us_states"
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
    )
    uri = "gs://ml-ops-dataset/us-states.csv"
    load_job = big_query_client.load_table_from_uri(
        uri, table_id, job_config=job_config
    )

    load_job.result()  

    destination_table = big_query_client.get_table(table_id)
    return {"data": destination_table.num_rows}

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5052)))