sandbox
=======

Dev env for StackTach development. Uses Notigen event generator and yagi.

Prerequisites:

    make sure you have a working python dev environment (2.7+ ideally)
        including virtualenv.
    Install rabbitmq.
    If using the oahu pipeline engine, install mongodb.
    If using the winchester pipeline engine, install MySQL.

TL;DR:

    handle the prerequisites above.
    git clone https://github.com/StackTach/sandbox.git
    cd sandbox
    If running winchester:
        create a mysql database to use
        set the database url appropriately in winchester.yaml
    ./build.sh

Tweaks:

You can create a `local.sh` to override the defaults:

    SOURCE_DIR=git  # where the StackTach repos are cloned
    VENV_DIR=.venv  # name of the .venv
    PIPELINE_ENGINE=oahu # Name of pipeline processing library to run.

The `build.sh` script will create clone each of the StackTach projects
into the `$SOURCE_DIR` directory (so you can work on them in a running env).

The virtualenv will be created and each of the projects
(and their dependencies) installed into it.

A `screen` session is started, based on `screenrc.oahu` or
`screenrc.winchester`  which will start the
`notigen` event generator. The event generator simulated OpenStack
notifications and pumps them into rabbitmq. `yagi-event` is also started
with the `yagi.conf` configuration file. This will read events from
the rabbit queue and save them to local files. The working directory
and archive directory for `shoebox` is specified in `yagi.conf`.

The sandbox environment configures `shoebox` to upload archive files
to Swift automatically. This requires you create a credentials file
in the `.../sandbox/` directory (like in
`.../git/sandbox/etc/sample_rax_credentials.conf`) Call it
`swift_credentials.conf` or alter the `shoebox.conf` file accordingly. If
you don't have access to a Swift server, like CloudFiles, read
the config file for details on disabling this feature.
