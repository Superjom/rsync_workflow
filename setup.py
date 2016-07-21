from setuptools import setup

setup(
    name='sync_workflow',
    version='0.1.1',
    description='A tool to help synchronize projects between remote and local environments',
    url='https://github.com/Superjom/rsync_workflow',
    author='Superjom',
    author_email='yanchunwei@outlook.com',
    license='MIT',
    packages=['rsync_workflow'],
    zip_safe=False,
    keywords='zsync workflow',
    scripts=['bin/rsync_pull.py', 'bin/rsync_push.py', 'bin/rsync_clone.py',
             'bin/rsync_init.py'], )
