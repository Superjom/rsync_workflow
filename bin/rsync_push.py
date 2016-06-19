from RsyncContext import RsyncManager, RsyncContext, set_debug

set_debug(False)

rsync_manager = RsyncManager()
rsync_manager.push()
