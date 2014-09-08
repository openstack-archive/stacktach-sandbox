#!/bin/bash

echo "StackTach dev env build script"

SOURCE_DIR=git
VENV_DIR=.venv
PIPELINE_ENGINE=oahu

if [[ -f local.sh ]]; then
    source local.sh
fi

if [[ ! -d "$SOURCE_DIR" ]]; then
  mkdir $SOURCE_DIR
fi

if [[ ! -d "$VENV_DIR" ]]; then
  virtualenv $VENV_DIR
fi

cd $SOURCE_DIR
for file in StackTach/shoebox StackTach/simport StackTach/notigen \
            StackTach/notabene StackTach/notification_utils rackerlabs/yagi \
            StackTach/stackdistiller StackTach/quincy StackTach/quince \
            StackTach/klugman StackTach/oahu StackTach/winchester
do
    git clone https://github.com/$file
done
cd ..

source ./$VENV_DIR/bin/activate

# Some extra required libs ...
pip install gunicorn
pip install httpie
pip install librabbitmq

# Needed by pyrax:
pip install pbr

for file in $SOURCE_DIR/*
do
    echo "----------------------- $file ------------------------------"
    cd $file
    rm -rf build dist
    python setup.py install
    cd ../..
done

(cat yagi.conf.$PIPELINE_ENGINE ; cat yagi.conf.common ) > yagi.conf

if [ $PIPELINE_ENGINE == "winchester" ]
then
    winchester_db -c winchester.yaml upgrade head
fi

screen -c screenrc.$PIPELINE_ENGINE

