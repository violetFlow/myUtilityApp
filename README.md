# My Utility App

## 概要
システムの業務上、便利なツールをまとめたウェブアプリケーション

## 使用技術
 - Os
   - Debian GNU/Linux 11 (bullseye)
 - Programing language
   - python 3.7
 - Frameworks
   - Flask 2.2.2
 - Template engine
   - jinjar2
 - PaaS products
   - docker 20.10.21
   - docker-compose 2.13.0
 - Database
   - postgreSQL 13.5
 - ORM
   - flask-sqlalchemy
 - Library
   - Pandas  

## 起動方法
```bash
# my-network作成
docker network create my_network --subnet=10.11.0.0/16

# my-utility-app ビルド
docker build -t my-utility-app:latest .

# my-utility-app 実行
docker run --net=my_network --ip 10.11.0.10 -p 5001:80 -v ${PWD}:/app -d my-utility-app

# docker-composeを利用したpostgreSQL構築
cd docker-postgre
docker-compose up -d

# uploadファイルはgitで管理しないため、フォルダを作成する。
mkdir upload
```


## 機能一覧
 - icsファイルを読み込み、macカレンダーで登録した日程を集計する
    - 期間中、作業別合計時間抽出
    - 期間中、日別別合計時間抽出
    - 使用法
       - mac純正カレンダーから「改善」カレンダーを選択後、「ファイル」→「書き出す」→「書き出す…」して「改善.ics」が吐き出されたら、そのファイルをアップロードする。
- アカウント管理機能
   - アカウント情報登録、更新、削除、一覧取得。

