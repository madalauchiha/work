#!/usr/local/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import stat
import sys

proj_dir = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.join(proj_dir, 'venv/lib/python3.5/site-packages')
if lib_path not in sys.path:
    sys.path.append(lib_path)

import compileall


def handle_pycache(root_dir, findname, del_str):
    for root, subdirs, files in os.walk(root_dir):
        for subdir in subdirs:
            if findname == subdir:
                pyc_dir = os.path.join(root, findname)
                for pyc in os.listdir(pyc_dir):
                    os.chdir(pyc_dir)
                    newname = pyc.replace(del_str, '')
                    os.rename(pyc, newname)
                    src_path = os.path.join(pyc_dir, newname)
                    dst_path = os.path.join(os.path.dirname(pyc_dir), newname)
                    shutil.move(src_path, dst_path)

                os.rmdir(pyc_dir)
            else:
                handle_dir = os.path.join(root, subdir)
                handle_pycache(handle_dir, findname, del_str)


def del_file_ext(rootdir, extension):
    for root, subdirs, files in os.walk(rootdir):
        if 'testsuite' == os.path.basename(root) and '.py' == extension:
            continue

        for file in files:
            if 'conftest.py' == file:
                continue
            if extension == os.path.splitext(file)[-1]:
                fpath = os.path.join(root, file)
                # print('del', fpath)
                os.remove(fpath)

        for subdir in subdirs:
            deldir = os.path.join(rootdir, subdir)
            del_file_ext(deldir, extension)


if '__main__' == __name__:
    if 2 != len(sys.argv):
        print('Error: please input like [python3 release.py vername]')
        sys.exit(1)

    rel_name = sys.argv[1]
    src_name = 'src'
    pycache_name = '__pycache__'
    del_str = '.cpython-35'
    dirs_link = ['configs', 'data', 'log', 'report', 'testcases']

    # define path
    rel_dir = os.path.join(proj_dir, rel_name)
    src_dir = os.path.join(rel_dir, src_name)
    os.mkdir(rel_dir)
    os.mkdir(src_dir)

    excluded_files = [__file__, 'README.md', 'README.html']
    # generate tree from project
    for item in os.listdir(proj_dir):
        from_path = os.path.join(proj_dir, item)
        to_path = os.path.join(src_dir, item)
        if os.path.isdir(from_path):
            if 'log' == item or 'data' == item:
                os.mkdir(to_path)
            elif rel_name != item:
                shutil.copytree(from_path, to_path)

            if 'data' == item:
                for data_sub in os.listdir(from_path):
                    make_src = os.path.join(from_path, data_sub)
                    make_dst = os.path.join(to_path, data_sub)
                    if os.path.isdir(make_src):
                        os.mkdir(make_dst)
        elif item not in excluded_files:
            shutil.copyfile(from_path, to_path)

    # compile to pyc
    compileall.compile_dir(src_dir)

    # del .py files
    del_file_ext(src_dir, '.py')

    # handle .pyc files
    handle_pycache(src_dir, pycache_name, del_str)

    # handle testsuite dir and conftest file
    suite_dir = os.path.join(src_dir, 'testsuite')
    del_file_ext(suite_dir, '.pyc')
    os.remove(os.path.join(src_dir, 'conftest.pyc'))

    pytest_pyc = os.path.join(src_dir, 'conftest-PYTEST.pyc')
    if os.path.exists(pytest_pyc):
        os.remove(pytest_pyc)

    # generate symlink
    for dir_link in dirs_link:
        src = os.path.join('./src', dir_link)
        dst = os.path.join(rel_dir, dir_link)
        if not os.path.exists(dst):
            os.symlink(src, dst)

    # generate run_test.sh
    # stat.S_IXUSR
    run_sh_path = os.path.join(rel_dir, 'run_test.sh')
    if not os.path.exists(run_sh_path):
        open(run_sh_path, 'w').write('./src/venv/bin/python3 ./src/run.pyc')
        os.chmod(run_sh_path, stat.S_IRWXU | stat.S_IXGRP | stat.S_IXOTH)

    # tar -zcvf
    os.chdir(proj_dir)
    os.system('tar -zcf %s %s' % (rel_name + '.tar.gz', rel_name))

