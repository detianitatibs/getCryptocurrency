# 仮想通貨情報取得バッチ
GMOコインのAPIを活用して、仮想通貨の情報を取得し、TSVファイル形式で保存するバッチをpythonで作成する。  
学習を兼ねて、ローカル版とGCF(Google Cloud Function)版を作成し、GCFについては、SchedulerとPub/Subを組み合わせて定期的に実行するようにする。  

機能追加として、日次でGCSからBigQueryにデータをロードするGCFも追加する。

## GCP上でのイメージ
- 毎分処理
    Cloud Scheduler --(1分間隔)--> Pub/Sub --> Cloud Functions(API->GCS)  
- 日次処理
    Cloud Scheduler --(0:10起動)--> Pub/Sub --> Cloud Functions(GCS->BigQuery)  

## getCryptocurrencyToGCS
GMOコインのAPIより取得した仮想通貨情報をGCSに保存する

### `getCryptocurrency.py`
ローカル動作確認版兼、関数作成。    
以下のコマンドで実行したディレクトリに`cryptocurrency_[datetime].tsv `が作成される。

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

### `getCryptocurrencyTest.py`
ローカル版のテストコード。  
学習兼用なので、カバレッジは考慮していない。気が向いたらケースを増やす。  

実施には、`pytest`が必要
```bash
pip install pytest
pytest getCryptocurrencyTest.py
```

### `main.py`
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

## loadGcsToBigQuery
StorageにたまったTSVファイルを日次でBigQueryにロードする。  
毎日0:10に実行し、前日1日分のファイルを一括でロードする。  
分割パーティションを採用し、前日分の日付を設定する。  

### main.py
GCF版。  
仮想通貨情報取得のときと同じく、ローカル環境では`functions-framework`を使用する。  

```
# 起動コマンド
functions-framework --target=loadGceToBigQuery --source=main.py --signature-type=event

# テストコマンド
curl -d '{"data": "test"}' -X POST -H "Content-Type: application/json" http://localhost:8080

# bigqueryのインストール
pip install google-cloud-bigquery

# gcloudデプロイコマンド
gcloud functions deploy loadCryptocurrecyGcsToBigQuery --runtime=python37 --trigger-topic=loadCryptocurrecyGcsToBigQuery --env-vars-file=.env.yaml --memory=128MB
```