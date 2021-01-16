# -*- coding:utf-8 -*-

"""
GMOコインのAPIを利用して仮想通貨の値を取得して、
Google Storageにtsvファイルとして保存する(GCF版)
"""

__author__ = "@detian_itatbs"
__status__ = "development"
__version__ = "0.0.1"
__date__    = "16 January 2021"

import getCryptocurrency as gc
import os

from google.cloud import storage

def uploadGcs(filepath, dt_str):
    """
    ファイルをGCSにアップロードする
    第1引数:tsvファイルを作成したファイルパスとファイル名
    第2引数:%Y%m%d%H%M%S形式の文字列
    """
    # envよりバケット名を取得する
    bucket_name = os.environ.get('BUCKET')

    # GCSのファイル名を作成する
    filename = filepath.split('/')[-1]
    filename = "/".join([dt_str[:4], dt_str[4:6], dt_str[6:8], filename])

    # GCSにアップロードする
    print("GCSにUpload開始")
    print("BUCKET:{} BLOB:{}".format(bucket_name, filename))
    try:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(filename)
        blob.upload_from_filename(filepath)
        print("GCSにUpload完了")
    except:
        print("GCSにUpload失敗")

def getCryptocurrencyToGCS(event, context): # for background functions
    endpoint = 'https://api.coin.z.com/public'
    path = '/v1/ticker'

    # Cloud FunctionsではCurrent DirectoryはRead Onlyなので
    # /tmp以下に保存するようにする
    dir_path = '/tmp'
    dt_str = gc.getNowDtStr()
    
    crypto_dic = gc.getCrypto(endpoint + path)
    filepath = gc.getFilepath(dir_path)

    # ステータスが0(正常)かを確認する
    if crypto_dic['status'] == 0:
        gc.createTsv(crypto_dic, filepath)
        uploadGcs(filepath, dt_str)

    else:
        # ログなどにエラーを出す際はこちらに書く
        print("status error.")

    print("終了時刻:"+gc.getNowDtStr())

    