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

def getNowDtStr():
    """
    現時刻の文字列(%Y%m%d%H%M%S)を返す
    """
    dt_now = datetime.datetime.now()
    dt_str = dt_now.strftime('%Y%m%d%H%M%S')
    return dt_str

def getCrypto(path):
    """
    仮想通貨の最新レートを取得する
    第1引数:GMOコインのエンドポイント
    戻値:辞書型の仮想通貨情報
    """
    res = requests.get(path)
    dic = res.json()
    return dic

def getFilepath(dir_path):
    """
    出力するtsvのファイルパスを作成する
    ファイル名は cryptocurrency_[datetime].tsv とする
    第1引数:ディレクトリパス
    戻値:ファイルパス
    """
    dt_str = getNowDtStr()
    filepath = dir_path + '/cryptocurrency_{0:s}.tsv'.format(dt_str)
    print("時刻:" + dt_str + " 保存先のパス:" + filepath)
    return filepath

def createTsv(dic):
    for rows in dic['data']:
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

if __name__ == '__main__':
    endpoint = 'https://api.coin.z.com/public'
    path = '/v1/ticker'
    dir_path = os.getcwd()
    
    crypto_dic = getCrypto(endpoint + path)
    filepath = getFilepath(dir_path)

    # ステータスが0(正常)かを確認する
    if crypto_dic['status'] == 0:
        createTsv(crypto_dic)
    else:
        # ログなどにエラーを出す際はこちらに書く
        print("status error.")

    print("終了時刻:"+getNowDtStr())