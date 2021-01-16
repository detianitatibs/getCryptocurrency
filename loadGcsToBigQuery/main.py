# -*- coding:utf-8 -*-

"""
StorageにたまったTSVファイルを日次でBigQueryにロードする(GCF版)
"""

__author__ = "@detian_itatbs"
__status__ = "development"
__version__ = "0.0.1"
__date__    = "16 January 2021"

import datetime
import os

from google.cloud import bigquery

def getNowDtStrAgo(isConvertJST=False):
    """
    現時刻から1日前の文字列(%Y%m%d%H%M%S)を返す
    第1引数:実施環境の時刻がUTCの場合はTrueにすることでJSTに変換する
    """
    dt_now = datetime.datetime.now() - datetime.timedelta(days=1)
    if isConvertJST :
        dt_now = dt_now + datetime.timedelta(hours=9)
    dt_str = dt_now.strftime('%Y%m%d%H%M%S')
    return dt_str

def loadCryptocurrecyGcsToBigQuery(event, context):
    bq = bigquery.Client()
    dt_str = getNowDtStrAgo(True)

    bucket = os.environ.get('BUCKET')
    filename = os.environ.get('FILENAME')
    project_id = os.environ.get('PROJECT_ID')
    dataset = os.environ.get('DATASET')
    table_name = os.environ.get('TABLE_NAME')

    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("timestamp", "DATETIME"),
            bigquery.SchemaField("symbol", "STRING"),
            bigquery.SchemaField("last", "FLOAT"),
            bigquery.SchemaField("high", "FLOAT"),
            bigquery.SchemaField("low", "FLOAT"),
            bigquery.SchemaField("ask", "FLOAT"),
            bigquery.SchemaField("bid", "FLOAT"),
            bigquery.SchemaField("volume", "FLOAT"),
        ],
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        source_format=bigquery.SourceFormat.CSV,
        field_delimiter='\t'
    )

    uri = 'gs://{0}/{1}/{2}/{3}/{4}_*'.format(bucket, dt_str[:4], dt_str[4:6], dt_str[6:8], filename)
    table_id = '{0}.{1}.{2}${3}'.format(project_id, dataset, table_name, dt_str[:8])

    load_job = bq.load_table_from_uri(
        uri, table_id, job_config=job_config
    )  # Make an API request.

    print("end")