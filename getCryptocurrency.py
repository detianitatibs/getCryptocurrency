# -*- coding:utf-8 -*-

"""
GMOコインのAPIを利用して仮想通貨の値を取得して、
Google Storageにtsvファイルとして保存する
"""

__author__ = "@detian_itatbs"
__status__ = "development"
__version__ = "0.0.1"
__date__    = "14 January 2021"

import requests
import json
import os
import datetime
import csv

ENDPOINT = 'https://api.coin.z.com/public'
PATH     = '/v1/ticker'

DIR_PATH = os.getcwd()

# 仮想通貨の最新レートを取得する
crypto_res = requests.get(ENDPOINT + PATH)
crypto_dic = crypto_res.json()

# 出力tsvのパスを作成する
# ファイル名は cryptocurrency_[datetime].tsv とする
dt_now = datetime.datetime.now()
dt_str = dt_now.strftime('%Y%m%d%H%M%S')
filepath = DIR_PATH + '/cryptocurrency_{0:s}.tsv'.format(dt_str)

print("実行開始 時刻:" + dt_str + " 保存先のパス:" + filepath)

# ステータスが0(正常)かを確認する
if crypto_dic['status'] == 0:
    for rows in crypto_dic['data']:
        """
        timestamp: 約定時の時間(日本時間に変換)
        symbol: 銘柄(JPYは日本円)
        last: 最終取引金額
        high: 最高気配値
        low: 最低気配値
        ask: 現在の売注文の最良気配値
        bid: 現在の買注文の最良気配値
        volume: 24時間の取引量
        """
        # timestampを日本時間にして、datetime型の文字列に変形する
        ts = datetime.datetime.fromisoformat(rows['timestamp'].replace('Z', '+00:00'))
        j_ts = ts + datetime.timedelta(hours=9) 
        rows['timestamp'] = j_ts.strftime('%Y%m%d%H%M%S')

        # tsv形式で保存する
        with open(filepath, 'a', encoding="UTF-8") as file:
            writer = csv.writer(file, delimiter='\t', lineterminator='\n')
            writer.writerow([rows['timestamp'],
                            rows['symbol'],
                            rows['last'],
                            rows['high'],
                            rows['ask'],
                            rows['bid'],
                            rows['volume']])
else:
    # ログなどにエラーを出す際はこちらに書く
    print("status error.")

print("実行終了")