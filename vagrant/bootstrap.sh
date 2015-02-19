#!/usr/bin/env bash

debconf-set-selections <<< 'mysql-server mysql-server/root_password password ROOTPASSWORD'
debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password ROOTPASSWORD'

sudo apt-get update
sudo apt-get install -y python-dev ipython mysql-server mysql-client libmysqlclient-dev git vim rabbitmq-server python-pip librabbitmq1

pip install virtualenv

if [ ! -f /var/log/dbinstalled ];
then
    echo "CREATE USER 'winchester'@'localhost' IDENTIFIED BY 'testpasswd'" | mysql -uroot -pROOTPASSWORD
    echo "CREATE DATABASE winchester" | mysql -uroot -pROOTPASSWORD
    echo "GRANT ALL ON winchester.* TO 'winchester'@'localhost'" | mysql -uroot -pROOTPASSWORD
    echo "flush privileges" | mysql -uroot -pROOTPASSWORD
    touch /var/log/dbinstalled
    if [ -f /vagrant/data/initial.sql ];
    then
        mysql -uroot -pROOTPASSWORD internal < /vagrant/data/initial.sql
    fi
fi

