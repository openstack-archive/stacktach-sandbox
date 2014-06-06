#!/bin/bash

echo "StackTach dev env build script"

SOURCE_DIR=git
VENV_DIR=.venv

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
            StackTach/klugman
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

screen -c screenrc
