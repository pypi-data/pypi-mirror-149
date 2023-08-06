# -*- coding: utf-8 -*-
from pkg_resources import packaging

_VERSION = (1, 6, 5, 'final', 0)


def get_version(version=_VERSION, form=None, no_commit_hash=False):
    if form == 'branch':
        return "{0}.{1}".format(version[0], version[1])

    main = '.'.join(str(x) for x in version[:3])
    if form == 'short':
        return main

    sub = ''
    append_hash = get_branch_name() not in ['main', 'master']
    if version[3] == 'alpha' and version[4] == 0:
        sub = '.dev'
        append_hash = True
    elif version[3] == 'final' and version[4] != 0:
        sub = '.post{0}'.format(version[4])
    elif version[3] != 'final':
        mapping = {'alpha': 'a', 'beta': 'b', 'rc': 'rc'}
        sub = mapping[version[3]] + str(version[4])
    if append_hash and not no_commit_hash:
        commit_hash = get_commit_hash()
        if commit_hash:
            sub += f'+{commit_hash}'
    return str(packaging.version.Version(main + sub))

def _run_cmnd(cmnd, decode=True, strip=True):
    import os
    import subprocess
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        proc = subprocess.Popen(cmnd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True, cwd=repo_dir)
        stdout = proc.communicate()[0]
        stdout = stdout.decode() if decode else stdout
        stdout = stdout.strip() if strip else stdout
        return stdout
    except OSError:
        return None

def get_branch_name():
    return _run_cmnd('git rev-parse --abbrev-ref HEAD')

def get_commit_hash():
    return _run_cmnd('git log -1 --pretty=format:"%h"')


BRANCH = get_version(form='branch')
VERSION = get_version()
SHORT_VERSION = get_version(form='short')


if __name__ == "__main__":
    print(VERSION)
