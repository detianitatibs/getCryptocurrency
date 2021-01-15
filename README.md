# 仮想通貨情報取得バッチ
GMOコインのAPIを活用して、仮想通貨の情報を取得し、TSVファイル形式で保存するバッチをpythonで作成する。  
学習を兼ねて、ローカル版とGCF(Google Cloud Function)版を作成し、GCFについては、SchedulerとPub/Subを組み合わせて定期的に実行するようにする。  

## GCP上でのイメージ
Cloud Scheduler --(数分感覚でkick)--> Pub/Sub --> Cloud Functions  

## `getCryptocurrency.py`
ローカル版。  
実行したディレクトリで`cryptocurrency_[datetime].tsv `が作成される。

```bash
python getCryptocurrency.py
```

| column | desc |
| --- | --- |
|timestamp | 約定時の時間(日本時間に変換) |
|symbol | 銘柄(JPYは日本円) |
|last | 最終取引金額 |
|high | 最高気配値 |
|low | 最低気配値 |
|ask | 現在の売注文の最良気配値 |
|bid | 現在の買注文の最良気配値 |
|volume | 24時間の取引量 |

## `getCryptocurrencyTest.py`
ローカル版のテストコード。  
学習兼用なので、カバレッジは考慮していない。気が向いたらケースを増やす。  

実施には、`pytest`が必要
```bash
pip install pytest
pytest getCryptocurrencyTest.py
```