# Get the status of a STv3 deployment.
# Returns:
#  - tail of each worker log on each worker node
#  - status of each rabbit server queue
#
# Requires a config file that has:
#  - location of your worker nodes
#  - name of your rabbit vhost
#  - name of your rabbit queues
#
# You will need a credentials for a user that
# can access all of these servers.

"""stv3_status - StackTach.v3 diagnostics utility.
Usage:
  stv3_status.py <config_file>
  stv3_status.py <config_file> -u <username>
  stv3_status.py <config_file> -u <username> -p <password>
  stv3_status.py (-h | --help)
  stv3_status.py --version
  stv3_status.py --debug
Options:
  -h --help     Show this help message
  --version     Show klugman version
  --debug       Debug mode
"""

from docopt import docopt
import pxssh
import tempfile
import yaml

import pxssh


def ssh(host, cmds, user, password, port):
    s = pxssh.pxssh()
    if not s.login (host, user, password, port=port):
        print "SSH session failed on login."
        print str(s)
        return None
    outputs = []
    for cmd in cmds:
        print "Running:", cmd
        s.sendline(cmd)
        s.prompt()
        outputs.append(s.before)
    s.logout()
    return outputs


arguments = docopt(__doc__, options_first=True)

config = {}
config_file = arguments.get('<config_file>')
if config_file:
    with open(config_file, 'r') as f:
        config = yaml.load(f)

debug = arguments.get('--debug', False)

if debug:
    print config

cell_names = config['cell_names']
username = config.get('username')
password = config.get('password')
worker_hostnames = config['worker_hostnames']
rabbit_hostnames = config['rabbit_hostnames']
api_hostnames = config['api_hostnames']
port = int(config.get('ssh_port', 22))
lines = config.get('tail_lines', '100')
queue_prefixes = config.get('queue_prefixes', ['monitor'])
num_pipeline_workers = config.get('num_pipeline_workers', 2)

num_cells = len(cell_names)
for worker in worker_hostnames:
    commands = ["ps auxww | grep -E 'yagi-event|pipeline_worker'"]
    for cell in cell_names:
        commands.append("tail --lines %s /var/log/stv3/yagi-%s.log" %
                            (lines, cell))
    for x in range(num_pipeline_workers):
        commands.append(
            "tail --lines %s /var/log/stv3/pipeline_worker_%d.log"
                % (lines, x+1))
    archive_directories = ["/etc/stv3/%s/events"
                                % cell for cell in cell_names]
    commands.append("du -ch --time %s /etc/stv3/tarballs"
                        % " ".join(archive_directories))
    commands.append("ls -lah /etc/stv3/tarballs")

    print "--- worker: %s" % (worker, )
    ret = ssh(worker, commands, username, password, port)

    print ret[0]
    for i, cell in enumerate(cell_names):
        print "Writing %s-yagi-%s.log" % (worker, cell)
        with open("%s-yagi-%s.log" % (worker, cell), "w") as o:
            o.write(ret[i+1])

    index = 2 + num_pipeline_workers
    for x in range(num_pipeline_workers):
        print "Writing pipeline worker: %s-pipeline_worker_%d.log" \
                % (worker, x+1)
        with open("%s-pipeline_worker_%d.log" % (worker, x+1), "w") as o:
            o.write(ret[-index + x])

    print ret[-2]
    print ret[-1]

for api in api_hostnames:
    commands = ["ps auxww | grep gunicorn",
                "tail --lines %s /var/log/stv3/gunicorn.log" % (lines, )]

    print "--- api: %s" % (api, )
    ret = ssh(api, commands, username, password, port)

    print ret[0]
    print "Writing %s-gunicorn.log" % (api,)
    with open("%s-gunicorn.log" % (api,), "w") as o:
        o.write(ret[1])

prefixes = '|'.join(queue_prefixes)
for rabbit_conf in rabbit_hostnames:
    host = rabbit_conf['host']
    vhost = rabbit_conf.get('vhost', '/')
    print "--- RabbitMQ: %s vhost: %s" % (host, vhost)
    ret = ssh(host, ["sudo rabbitmqctl list_queues -p %s | grep -E '%s'" %
                            (vhost, prefixes)],
                       username, password, port)
    for r in ret:
        print r
