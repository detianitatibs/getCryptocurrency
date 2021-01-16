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

## `main.py`
GCF版。  
ローカル実行環境として、[functions-framework](https://github.com/GoogleCloudPlatform/functions-framework-python)を利用する。  


```bash
# functions-frameworkのインストール
pip install functions-framework

# 起動コマンド
functions-framework --target=main --source=main.py --signature-type=event

# テストコマンド
curl -d '{"data": "test"}' -X POST -H "Content-Type: application/json" http://localhost:8080

# cloud storageのインストール
google-cloud-storagey

# gcloudデプロイコマンド
gcloud functions deploy getCryptocurrencyToGCS --runtime=python37 --trigger-topic=getCryptocurrencyToGCS --env-vars-file=.env.yaml --memory=128MB
```
