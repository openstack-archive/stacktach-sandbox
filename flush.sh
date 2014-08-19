#!/bin/bash
sudo rabbitmqctl list_queues
sudo rabbitmqctl stop_app
sudo rabbitmqctl reset
sudo rabbitmqctl start_app
sudo rabbitmqctl list_queues
