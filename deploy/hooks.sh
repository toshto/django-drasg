#!/bin/bash

APPBASE="/var/www/mysite"

case $LIFECYCLE_EVENT in

  "BeforeBlockTraffic" )
    #  ** 旧インスタンスで実行される。
  ;;
  "BlockTraffic" )
  # この間に疎通停止する。
  ;;
  "AfterBlockTraffic" )
    #  ** 旧インスタンスで実行される。
  ;;
  "ApplicationStop" )
    #  ** 旧インスタンスで実行される。
  ;;
  "DownloadBundle" ):
    # デプロイ物件のダウンロードをする。
  ;;
  "BeforeInstall" )
    # Stop application server.
    if [ -f /var/run/httpd/uwsgi.pid ]; then
      # shellcheck disable=SC2046
      kill -9 $(cat /var/run/httpd/uwsgi.pid)
    fi

    # Set maintenace screen.
    if [ -f /etc/httpd/conf/app_maint.conf ]; then
      cp /etc/httpd/conf/app_maint.conf /etc/httpd/conf/app.conf
      systemctl restart httpd
    fi
  ;;
  "Install" )
    # デプロイ物件展開
  ;;
  "AfterInstall" )
    cat $APPBASE/db.conf >> $APPBASE/config/settings.py

    # Preconfiguration for Application
    chown -R apache:apache $APPBASE
    source ${APPBASE}/venv/bin/activate
    python ${APPBASE}/manage.py migrate
    python ${APPBASE}/manage.py collectstatic --noinput
  ;;

  "ApplicationStart" )
    # Start application server
    ${APPBASE}/venv/bin/uwsgi --ini ${APPBASE}/uwsgi.ini
  ;;

  "ValidateService" )
    # Start Online
    if [ -f /etc/httpd/conf/app_on.conf ]; then
      # Set online screen
      cp /etc/httpd/conf/app_on.conf /etc/httpd/conf/app.conf
      # Restart httpd
      /usr/bin/systemctl restart httpd
    fi
  ;;

  "BeforAllowTraffic" )
  # ** 旧インスタンスで実行される。
  ;;
  "AllowTraffic" )
  # この間に疎通開始する。
  ;;
  "AfterAllowTraffic" )
  ;;

esac
