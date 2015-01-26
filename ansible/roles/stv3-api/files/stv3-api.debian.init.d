#! /bin/sh
### BEGIN INIT INFO
# Provides:          Gunicorn HTTP service
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Gunicorn HTTP service.
# Description:       Gunicorn HTTP service.
### END INIT INFO

# Author: Sandy Walsh <sandy.walsh@rackspace.com>

# Do NOT "set -e"

# PATH should only include /usr/* if it runs after the mountnfs.sh script
PATH=/opt/stv3/bin:/sbin:/usr/sbin:/bin:/usr/bin
DESC="Gunicorn service control"
NAME=gunicorn
DAEMON=/opt/stv3/bin/$NAME
DAEMON_ARGS="--log-file=/var/log/stv3/gunicorn.log -b 0.0.0.0 quincy.api:get_api(config_location=\"/etc/stv3/quincy.conf\")"
PIDFILE=/var/run/stv3/$NAME.pid
SCRIPTNAME=/etc/init.d/$NAME
USER=stv3
GROUP=stv3

# Exit if the package is not installed
[ -x "$DAEMON" ] || exit 0

# Read configuration variable file if it is present
[ -r /etc/default/$NAME ] && . /etc/default/$NAME

# Load the VERBOSE setting and other rcS variables
. /lib/init/vars.sh

VERBOSE=yes

# Define LSB log_* functions.
# Depend on lsb-base (>= 3.2-14) to ensure that this file is present
# and status_of_proc is working.
. /lib/lsb/init-functions

#
# Function that starts the daemon/service
#
do_start()
{
    . /opt/stv3/bin/activate
    start-stop-daemon --start --name ${NAME} --chdir /var/run/stv3 \
                      --chuid ${USER}:${GROUP} --background \
                      --make-pidfile --pidfile ${PIDFILE} \
                      --exec ${DAEMON} -- ${DAEMON_ARGS}
}

#
# Function that stops the daemon/service
#
do_stop()
{
    . /opt/stv3/bin/activate
    log_daemon_msg "Stopping ${DAEMON}... " ${DAEMON}
    start-stop-daemon --stop --oknodo --pidfile ${PIDFILE} --retry=TERM/30/KILL/5
    log_end_msg $?
}

case "$1" in
  start)
    [ "$VERBOSE" != no ] && log_daemon_msg "Starting $DESC" "$NAME"
    do_start
    case "$?" in
        0|1) [ "$VERBOSE" != no ] && log_end_msg 0 ;;
        2) [ "$VERBOSE" != no ] && log_end_msg 1 ;;
    esac
    ;;
  stop)
    [ "$VERBOSE" != no ] && log_daemon_msg "Stopping $DESC" "$NAME"
    do_stop
    case "$?" in
        0|1) [ "$VERBOSE" != no ] && log_end_msg 0 ;;
        2) [ "$VERBOSE" != no ] && log_end_msg 1 ;;
    esac
    ;;
  status)
    status_of_proc "$DAEMON" "$NAME" && exit 0 || exit $?
    ;;
  restart|force-reload)
    log_daemon_msg "Restarting $DESC" "$NAME"
    do_stop
    do_start
    ;;
  *)
    #echo "Usage: $SCRIPTNAME {start|stop|restart|reload|force-reload}" >&2
    echo "Usage: $SCRIPTNAME {start|stop|status|restart|force-reload}" >&2
    exit 3
    ;;
esac

:

