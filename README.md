sandbox
=======

Dev env for StackTach development. Uses Notigen event generator and yagi.

You can create a `local.sh` to override the defaults:

    SOURCE_DIR=git  # where the StackTach repos are cloned
    VENV_DIR=.venv  # name of the .venv

The `build.sh` script will create clone each of the StackTach projects
into the `$SOURCE_DIR` directory (so you can work on them in a running env). 

The virtualenv will be created and each of the projects 
(and their dependencies) installed into it. 

A `screen` session is started, based on `screenrc` which will start the 
`notigen` event generator. The event generator simulated OpenStack
notifications and pumps them into rabbitmq. `yagi-event` is also started
with the `shoebox.conf` configuration file. This will read events from
the rabbit queue and save them to local files. The working directory
and archive directory for `shoebox` is specified in `shoebox.conf`.

