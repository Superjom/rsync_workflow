import sys
import logging
from rsync_workflow.RsyncContext import RsyncManager, RsyncContext, set_debug

if len(sys.argv) != 3:
    logging.error('missing arguments')
    logging.error('rsync_clone.py [remote_path] [local_path]')
    sys.exit(-1)

rsync_manager = RsyncManager()

rsync_manager.clone(*sys.argv[1:])
