#!/bin/sh

APP_PACKAGE_DIR=/home/john/huzhu
APP_DEPLOY_DIR=/var/www/
NGINX_CONFIG_DIR=$APP_PACKAGE_DIR/deploy/config/nginx
SUPERVISOR_CONFIG_DIR=$APP_PACKAGE_DIR/deploy/config/supervisor

install_nginx()
{
        echo "start to install nginx"
        yum -y install nginx>>/dev/null
        nginx_installcation_ok=$(rpm -qa "nginx")
        if [ "$nginx_installation_ok" ];then
                echo "success to install nginx"
        else
                echo "failed to install nginx"
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
        echo "start to install supervisor"
        yum -y install supervisor>>/dev/null
        supervisor_installation_ok=$(rpm -qa "supervisor")
        if [ "$supervisor_installation_ok" ];then
                echo "success to install supervisor"
        else
                echo "failed to install supervisor"
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
        echo "make log file directory failed!"
        exit -1
    fi
}
copy_app_package(){
    mkdir -p "$APP_DEPLOY_DIR"
    cp_app_pack_err=$(cp -af "$APP_PACKAGE_DIR" "$APP_DEPLOY_DIR/" )
    if [  "$cp_app_pack_err" ];then
        echo "copy app package failed!"
        exit -1
    fi 
}
config(){
    OK=$(cp -af $NGINX_CONFIG_DIR/* /etc/nginx/)
    if [  "$OK" ];then
        echo "failed to copy nginx config file"
        exit -1
    fi
    OK=$(cp -af $SUPERVISOR_CONFIG_DIR/* /etc/supervisord.d/)
    if [  "$OK" ];then
       echo "failed to copy supervisor config file"
       exit -1
    fi
}
start_app(){
    supervisorctl stop all
    supervisor_pid=$(ps -aux |grep supervisord|awk '{print $2,$7}'|grep '?'|awk '{print $1}')
    kill -9  ${supervisor_pid}
    nginx -s quit >/dev/null 2>&1
    supervisord -c /etc/supervisord.conf > /dev/null 2>&1
    supervisor_pid=$(ps -aux |grep supervisord|awk '{print $2,$7}'|grep '?'|awk '{print $1}')
    if [ ! "$supervisor_pid" ];then
            echo "failed to start supervisor"
            exit -1
    fi
    nginx_is_on=$(nginx)
    if [  "$nginx_is_on" ];then
            echo "failed to start nginx"
            exit -1
    fi 
}
compress_js(){
    for js_file in `ls $APP_DEPLOY_DIR/huzhu/static/javascripts`
    do
          uglifyjs ${APP_DEPLOY_DIR}/huzhu/static/javascripts/${js_file} -m -o ${APP_DEPLOY_DIR}/huzhu/static/javascripts/${js_file}
    done 

}
main()
{
    rm -rf /var/www/huzhu/
    check_nginx
    check_supervisor
    create_log_dir
    copy_app_package
    config
    compress_js
    start_app
    echo "success to deploy app"
}

main
