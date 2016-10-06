#!/bin/bash
set -e
#set -x

APP_PACKAGE_DIR=/root/project/huzhu/
APP_DEPLOY_DIR=/var/www/
NGINX_CONFIG_DIR=$APP_PACKAGE_DIR/deploy/config/nginx
SUPERVISOR_CONFIG_DIR=$APP_PACKAGE_DIR/deploy/config/supervisor

install_nginx()
{
        echo -e "\e[0;33m start to install nginx \e[m"
        yum -y install nginx>>/dev/null
        nginx_installation_ok=$(rpm -qa "nginx")
        if [ "$nginx_installation_ok" ];then
                echo -e "\e[0;32m success to install nginx \e[m" 
        else
                echo -e "\e[0;31m failed to install nginx \e[m"
                exit -1
        fi
}

check_nginx()
{
        nginx_exists=$(rpm -qa "nginx")
        if [ ! "$nginx_exists" ];then
             install_nginx
        fi
}

install_supervisor(){
        echo -e "\e[0;33m start to install supervisor \e[m"
        yum -y install supervisor>>/dev/null
        supervisor_installation_ok=$(rpm -qa "supervisor")
        if [ "$supervisor_installation_ok" ];then
                echo -e "\e[0;32m success to install supervisor \e[m"
        else
                echo -e "\e[0;31m failed to install supervisor \e[m"
                exit -1
        fi
}

check_supervisor(){
        supervisor_exists=$(rpm -qa "supervisor")
        if [ ! "$supervisor_exists" ];then
             install_supervisor
        fi

}
create_log_dir(){
    mkdir_log_dir_err=$(mkdir -p /var/log/huzhu/{tornado,celery})
    if [ "$mkdir_log_dir_err" ];then
        echo -e "\e[0;31m make log file directory failed! \e[m"
        exit -1
    fi
}
copy_app_package(){
    mkdir -p "$APP_DEPLOY_DIR"
    cp_app_pack_err=$(cp -af "$APP_PACKAGE_DIR" "$APP_DEPLOY_DIR/" )
    if [  "$cp_app_pack_err" ];then
        echo -e "\e[0;31m copy app package failed! \e[m"
        exit -1
    fi 
}
config(){
    OK=$(cp -af $NGINX_CONFIG_DIR/* /etc/nginx/)
    if [  "$OK" ];then
        echo  -e "\e[0;31m failed to copy nginx config file \e[m"
        exit -1
    fi
    OK=$(cp -af $SUPERVISOR_CONFIG_DIR/* /etc/supervisord.d/)
    if [  "$OK" ];then
       echo -e "\e[0;31m failed to copy supervisor config file \e[m"
       exit -1
    fi
}
start_app(){
    supervisorctl stop all
    supervisor_pid=$(ps -aux |grep supervisord|awk '{print $2,$7}'|grep '?'|awk '{print $1}')
    if [ "$supervisor_pid" ];then
        kill -9  ${supervisor_pid}
    fi
    nginx -s quit >/dev/null 2>&1
    supervisord -c /etc/supervisord.conf > /dev/null 2>&1
    supervisor_pid=$(ps -aux |grep supervisord|awk '{print $2,$7}'|grep '?'|awk '{print $1}')
    if [ ! "$supervisor_pid" ];then
            echo -e "\e[0;31m failed to start supervisor \e[m"
            exit -1
    fi
    nginx_is_on=$(nginx)
    if [  "$nginx_is_on" ];then
            echo -e "\e[0;31m failed to start nginx \e[m"
            exit -1
    fi 
}

restart_app(){
    supervisorctl restart all
}

stop_app(){
    supervisorctl stop all
}

compress_js(){
    for js_file in `ls $APP_DEPLOY_DIR/huzhu/static/javascripts`
    do
          uglifyjs ${APP_DEPLOY_DIR}/huzhu/static/javascripts/${js_file} -m -o ${APP_DEPLOY_DIR}/huzhu/static/javascripts/${js_file}
    done 

}
deploy_app()
{
    echo -e "\e[0;33m start to deploy app \e[m"
    rm -rf /var/www/huzhu/
    check_nginx
    check_supervisor
    create_log_dir
    copy_app_package
    config
    compress_js
    start_app
    echo -e "\e[0;32m success to deploy app \e[m"
}


case $1 in 
    "deploy")
            deploy_app
     ;;
    "restart")
            restart_app
     ;;
    "stop")
            stop_app
     ;;
     *)
             echo -e "\e[0;31m please input one of them in the following commands:
                          'deploy',
                          'restart',
                          'stop' 
                       \e[m"
     ;;
esac


