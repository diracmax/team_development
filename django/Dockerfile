# ベースとするDockerイメージを指定
FROM python:3.8-buster

# リアルタイムでログを見れるように環境変数を指定
ENV PYTHONUNBUFFERD 1

# ローカルのrequirements.txtをコンテナにコピー
COPY ./requirements.txt /requirements.txt

# Djangoプロジェクトを置くディレクトリをコンテナ上に作成
RUN mkdir /django

# コンテナ上の作業するディレクトリを変更
WORKDIR /django

# ローカルのdjangoディレクトリをコンテナにコピー
COPY . /django

# アプリケーションを実行するためのユーザを作成する
RUN adduser --disabled-password --gecos "" user

# ユーザをrootから変更
USER user

ENV PATH $PATH:/home/user/.local/bin

# requirements.txtに従ってパッケージを一括でインストール
RUN pip install -r /requirements.txt
