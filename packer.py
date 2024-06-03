#!/usr/bin/env python

import boto3
import os
import sys
# import re

# 引数チェック
try:
    me = sys.argv.pop(0)
    stackname = sys.argv.pop(0)
    region = sys.argv.pop(0)
except Exception as e:
    print("Usage: packer.py <stackname> <region>")
    print(e)
    sys.exit(1)

instname = "db1-" + stackname
cache = "memca1-" + stackname
BUCKET = stackname + '.' + region + '.xxxxxxxx.com'
PACKAGE = 'mysite.tar.gz'

try:
    # RDSとECAのエンドポイントをAWS-CLI経由で取得する。
    session = boto3.Session(profile_name='default', region_name=region)
    instances = session.client('rds').describe_db_instances(
        DBInstanceIdentifier='DB-kbn'
    )
    EP1 = instances['DBInstances'][0]['Endpoint']['Address']
#    EP1 = 'a'

    session = boto3.Session(profile_name='default', region_name=region)
    clusters = session.client('elasticache').describe_cache_clusters(
        CacheClusterId='memcached-kbn'
    )
    EP2 = clusters['CacheClusters'][0]['ConfigurationEndpoint']['Address']
#    EP2 = 'b'

except Exception as e:
    print("ERROR: エンドポイントの取得に失敗しました。")
    print(e)
    exit(1)

# 追加パラメタを設定ファイルに
settings = '''
DB2['default']['HOST'] = '{_EP1}'
CC1['default']['LOCATION'] = '{_EP2}:11211'
DATABASES = DB2
CACHES = CC1
SESSION_ENGINE='django.contrib.sessions.backends.cache'
STATIC_ROOT='/var/www/html/static/'
DEBUG = False
'''.format(_EP1=EP1, _EP2=EP2)

fw = open("deploy/conf/db.conf", "w")
fw.write(settings)
fw.close()

rc = os.system("mkdir source/")
if rc != 0:
    print("ERROR: sourceディレクトリの作成に失敗しました。")
    exit(rc)

for obj in ('config', 'polls', 'health', 'manage.py'):  # Djangoアプリに必要な資材をsource配下にコピーして、
    rc = os.system("cp -Rp " + obj + " source/")
    if rc != 0:
        print("ERROR: 資材のコピーに失敗しました。")
        exit(rc)

rc = os.system("tar cfvz " + PACKAGE + " deploy source appspec.yml")  # 環境依存の資材と一緒に固める
if rc != 0:
    print("ERROR: 資材のアーカイビングに失敗しました。")
    exit(rc)

rc = os.system("rm -rf source")
if rc != 0:
    print("ERROR: soruceフォルダの削除に失敗しました。")
    exit(rc)

# パッケージをS3バケットへアップロードする。
try:
    bucket = boto3.resource('s3').Bucket(BUCKET)
    print('release/' + PACKAGE)
    bucket.upload_file(PACKAGE, 'release/' + PACKAGE)
except Exception as e:
    print(BUCKET)
    print('ERROR: パッケージのアップロードに失敗しました。')
    print(e)
else:
    print('upload ' + PACKAGE + ' successfully.')
    print('revision is s3://' + BUCKET + '/release/' + PACKAGE)

if os.path.isfile(PACKAGE):
    os.remove(PACKAGE)
