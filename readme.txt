# Pycharmプロジェクトを作成する。venvでDjangoを導入しておく。

# Django全体設定の作成
$ cd <project_directory>
$ django-admin startproject <project_name> .

# アプリケーションの作成（複数可）
$ python manage.py startapp <application name>
...
$ python manage.py startapp <application name>

# settings.py の INSTALLED_APPS に apps.py の AppConfigクラスを登録する。

# models.pyにモデルクラスを作成して、
# 以下のコマンドを実行すると、テーブル作成用のクラスファイルが、 migrations配下に作成される。
$ python manage.py makemigrations <application name>

# 以下のコマンドでテーブル作成用のSQLの内容が表示される。
$ python manage.py sqlmigrate <application name> 0001

# 以下のコマンドでアプリ登録されているアプリのモデルに対応するテーブルをDBに作成する。
$ python manage.py migrate

# 以下のコマンドでsetting.pyのSTATIC_ROOTに指定したディレクトリに静的ファイルを配置する。
$ python manage.py collectstatic

# 以下のコマンドで管理サイト(admin)のユーザを作成できる。
$ python manage.py createsuperuser

# 開発サーバ起動
$ python manage.py runserver

# ユーザ名の変更
python manage.py changepassword <user_name>

#
# デプロイ方法
#
    ./packer.py <stackname> <region>

スクリプトを実行すると、Djangoアプリの実行に必要な資材を./source 配下にコピーし、./deploy ./appspec.yml とともに "mysite.tar.gz" にアーカイブして、
s3://<stackname>-xxxxxxxx-com/release/<region>/mysite.tar.gz にアップロードします。

CodeDeployアプリケーションの”リビジョンの場所”に、s3://<stackname>-xxxxxxxx-com/release/<region>/mysite.tar.gz を指定してデプロイを実行してください。

▪デプロイ設定
    appspec.yml

このファイルのfilesセクションでsourceに指定したリビジョン内のファイル/ディレクトリがdestinationのパスにコピーされます。
permissionsセクションでファイル/ディレクトリの権限設定をします。
hooksセクションで、ライフサイクルイベントごとにlocationに指定したプログラムをrunasに指定したユーザで実行します。
