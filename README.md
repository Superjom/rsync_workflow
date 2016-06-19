# Rsync Workflow

A tool to help synchronizing project directory between remote and local environments.

## Setup

    python setup.py install

## Usage

First, you should start the remote rsync service.

Write a rsync configuration, and start like this:

       rsync --daemon --port 8003 --config ~/conf/rsyncd.conf

Then, prepare a local project's `rsync_workflow` configuration named `_rsync_project.conf`,
and the content like:

    [remote]
    # remote node's IP
    ip: xxx.xxx.xxx.xxx
    # the rsync service's port
    port: 8019

    [project]
    # the project's path in the remote node
    remote_path: projects/_tmp/

In the local node:

### Pull to download remote project's update

    rsync_pull.py

### Push to update local project's update


    rsync_push.py


## Clone to download directories in the remote node

    rsync_clone.py remote_path local_path
