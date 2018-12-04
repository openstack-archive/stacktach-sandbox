stv3-config
==============

Configuration playbooks for StackTach.v3 deployments

Assumes an inventory value that has nodes or groups that start with "stv3-api" or "stv3-workers".

Execution would look like:

```bash
ansible-playbook workers.yaml
```

Assumes a stv3-db setup already exists.

There are also roles for database and api. The `common` role is responsible for installing the tarball and creating the necessary user/group accounts. Both the API and workers depend on the common role since they both require the codebase and winchester configuration files.

What it does
------------

* Creates `stv3` user and `stv3` group
* Creates `/etc/stv3` directory for configuration data
* Creates `/var/run/stv3` directory for pid files
* Creates `/var/log/stv3` directory for log files
* Copies config files to `/etc/stv3`
* Copies init.d files to `/etc/init.d` for yagi-events and pipeline-worker
* Copies and expands the StackTach.v3 tarball to `/opt/stv3`
* Starts the yagi worker daemon and the winchester worker
    (yagi-events and pipeline-worker respectively)

The init.d files handle the .pid file creation and running as stv3 user.

While yagi-events and pipeline-worker are capable to running daemonized, we don't use that code.
Instead, we let the init.d scripts handle the backgrounding and process management.

The connection from the host machine to the target machine has to have a secure account already created for ansible to run. Currently it assumes an account called `stacktach` and it has root capabilities. When the daemons run, they run as `stv3` ... which is just a service account.
