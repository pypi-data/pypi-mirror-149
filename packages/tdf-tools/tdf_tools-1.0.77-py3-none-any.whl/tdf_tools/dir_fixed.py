#!/usr/bin/env python
# encoding=utf-8

import os

from tdf_tools.tdf_print import printDebug, printError

genDirName = '.tdf_flutter'

# 向上遍历寻找.tdf_flutter存在的目录，找到则


def goSearchDir():
    os.chdir(os.path.abspath(r".."))
    curDir = os.getcwd()

    if os.path.exists(genDirName):
        return

    ex = Exception('未发现.tdf_flutter目录')
    raise ex


global curDir
curDir = os.getcwd()


def getShellDir():
    return curDir


def goInShellDir():
    os.chdir(curDir)
    # os.chdir(os.path.abspath(os.path.dirname(__file__)))
    # printDebug(os.getcwd())

# 进入.tdf_flutter文件夹


def goInTdfFlutterDir():
    goInShellDir()
    if os.path.exists('pubspec.yaml'):
        try:
            goSearchDir()
        except:
            goInShellDir()
            os.chdir(os.path.abspath(r".."))
            os.mkdir('.tdf_flutter')
    os.chdir('.tdf_flutter')


# 进入缓存文件目录


def goTdfCacheDir():
    goInShellDir()
    if os.path.exists('tdf_cache'):
        os.chdir('tdf_cache')
    elif os.path.exists('tdf_cache') is not True:
        if os.path.exists('pubspec.yaml') is not True:
            printError('请确保当前在flutter壳目录内')
        create = input('当前目录没有找到tdf_cache缓存文件夹，是否创建？(y/n):')
        if create == 'y':
            os.mkdir('tdf_cache')
        else:
            print('Oh,it\'s disappointing.')
            exit(1)
