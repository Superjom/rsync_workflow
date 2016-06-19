import os
import sys
import logging
import configparser
import subprocess

CONFIG_NAME = '.zsync_project.conf'
logging.basicConfig(level=logging.DEBUG)

def wrap_async_prefix(path):
    '''
    path should be remote
    '''
    rsync_prefix = 'rsync://'
    if not path.startswith(rsync_prefix):
        path = rsync_prefix + path
    return path
        
DEBUG = False
def set_debug(debug=True):
    global DEBUG
    DEBUG = debug

class RsyncContext(object):
    '''
    record fields needed by rsync command

    the config file is like:

    <<<D

    [remote]
    ip: xxx.xxx.xxx
    port: xxxx

    [project]
    remote_path: xxx
    D

    the local project's path will be speculated from PWD 
    '''
    def __init__(self, path):
        print 'path', path
        self.init_from_config(path)

    def init_from_args(self, **dargs):
        for key,value in dargs.items():
            setattr(self, key, value)

    def init_from_config(self, path):
        conf_path = os.path.join(path, CONFIG_NAME)
        self.conf = configparser.ConfigParser()
        self.conf.read(conf_path)
        self.local_project_path = path
        self.remote_port = self.conf.getint('remote', 'port')
        self.remote_ip = self.conf.get('remote', 'ip')
        self.remote_project_path = self._wrap_zsync_ip(
            self.conf.get('project', 'remote_path'))

    def _wrap_zsync_ip(self, path):
        '''
        add ip to path, to generate remote rsync path
        '''
        return wrap_async_prefix(self.remote_ip) + '/' + path

    def __str__(self):
        lines = ["<RsyncContext "]
        lines.append('local_project_path:%s' % self.local_project_path)
        lines.append('remote_port:%d' % self.remote_port)
        lines.append('remote_ip:%s' % self.remote_ip)
        lines.append('remote_project_path:%s' % self.remote_project_path)
        lines.append('>')
        return '\n'.join(lines)


class RsyncCommand(object):
    def __init__(self, context):
        '''
        rsync cmd generator

        @context: object of RsyncContext
        '''
        self.context = context

    def trans_cmd(self, path1, path2):
        return "rsync -azP --port {port} {path1} {path2}".format(
            path1 = path1,
            path2 = path2,
            port = self.context.remote_port,
        )

    def pull_cmd(self):
        return self.trans_cmd(
            path1 = self.context.remote_project_path,
            path2 = self.context.local_project_path,
        )

    def push_cmd(self):
        return self.trans_cmd(
            path1 = self.context.local_project_path,
            path2 = self.context.remote_project_path,
        )

    def clone_cmd(self, remote_path, local_path):
        return self.trans_cmd(
            path1 = remote_path,
            path2 = local_path,
        )

def run_shell(cmd):
    logging.warning('running cmd: %s' % cmd)
    process = subprocess.Popen(cmd.split(),
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
    out, err = process.communicate()
    logging.warning('shell output: %s' % out)
    return out.strip(), err

def speculate_project_path():
    '''
    find the nearest path with contains the file .rsync_project.conf

    @return:
    path, if project is detected
    None, if no project is dected
    '''
    #pwd = os.path.dirname(os.path.abspath(__file__))
    pwd, _ = run_shell('pwd')
    if _: logging.error('run_shell [error]: %s' % _)
    while pwd != '/':
        conf_path = os.path.join(pwd, CONFIG_NAME)
        if (os.path.exists(conf_path)):
            return pwd
        logging.warning('searching %s for config' % conf_path)
        pwd = os.path.dirname(pwd)
    return pwd


class RsyncManager(object):
    def __init__(self):
        '''
        @context: RsyncContext
        '''
        pwd = speculate_project_path()
        logging.warning('get project path: %s' % pwd)
        if not pwd:
            logging.error('no %s found in current path and its parent paths' %
                          CONFIG_NAME)
            sys.exit(-1)
        logging.debug('load config from %s/%s' % (pwd, CONFIG_NAME))
        context = RsyncContext(pwd)
        self.rsync = RsyncCommand(context)

    def push(self):
        '''
        sync and update local change to remote
        '''
        cmd = self.rsync.push_cmd()
        if not DEBUG:
            run_shell(cmd)
        logging.debug('run cmd %s' % cmd)

    def pull(self):
        '''
        sync and download remote project to local
        '''
        cmd = self.rsync.pull_cmd()
        logging.debug('run cmd %s' % cmd)
        if not DEBUG:
            run_shell(cmd)
        
    def clone(self, remote_path, local_path):
        '''
        just download a path from remote_path to local_path
        '''
        cmd = self.rsync.clone_cmd(remote_path, local_path)
        if not DEBUG:
            run_shell(cmd)
        logging.debug('run cmd %s' % cmd)


if __name__ == '__main__':
    pwd = speculate_project_path()
    print pwd
    context = RsyncContext(pwd)
    print context

    rsync = RsyncCommand(context)

    print rsync.trans_cmd('path1', 'path2')
    print rsync.pull_cmd()
    print rsync.push_cmd()
