from RsyncContext import RsyncManager, RsyncContext, set_debug

set_debug(True)

rsync_manager = RsyncManager()
rsync_manager.push()
