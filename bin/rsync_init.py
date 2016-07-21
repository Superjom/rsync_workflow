import os
import sys
import logging
from rsync_workflow.RsyncContext import CONFIG_NAME

pwd = os.curdir
path = os.path.join(pwd, CONFIG_NAME)

if os.path.exists(path):
    logging.error("path %s exists, will not init!")
    sys.exit(-1)

with open(path, 'w') as f:
    lines = [
        "[remote]",
        "# remote node's IP",
        "ip: xxx.xxx.xxx.xxx",
        "# the rsync service's port",
        "port: 8019",
        "",
        "[project]",
        "# the project's path in the remote node",
        "remote_path: projects/_tmp/",
    ]
    f.write('\n'.join(lines))

    logging.warning('init config in %s' % path)
