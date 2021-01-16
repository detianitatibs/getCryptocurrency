# -*- coding: utf-8 -*-

"""
getCryptocurrencyのテストコード
"""

from getCryptocurrency import getFilepath, getNowDtStr
    
def test1_getnowDtStr():
    """
    getnowDtStr() ケース1
    期待動作
    長さが一致していること
    """
    dt = '20210115003754'
    assert len(getNowDtStr()) == len(dt)

def test2_getNowDtStr():
    """
    getnowDtStr() ケース2
    期待動作
    型が一致していること
    """
    dt = '20210115003754'
    assert type(getNowDtStr()) == type(dt)
