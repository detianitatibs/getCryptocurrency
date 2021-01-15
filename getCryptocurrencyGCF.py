# -*- coding:utf-8 -*-

"""
GMOコインのAPIを利用して仮想通貨の値を取得して、
Google Storageにtsvファイルとして保存する(GCF版)
"""

__author__ = "@detian_itatbs"
__status__ = "development"
__version__ = "0.0.1"
__date__    = "16 January 2021"

# ISSUE:functions-frameworkで別ファイルをimportする手段が分からない
import getCryptocurrency

def main(event, context): # for background functions
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
    