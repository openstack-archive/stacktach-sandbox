echo "This will nuke all StackTach.v3 data in mysql and rabbitmq!"
read -p "Are you sure? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
mysql -u root --password=password < reset.sql
sudo rabbitmqctl stop_app
sudo rabbitmqctl reset
sudo rabbitmqctl start_app
fi







