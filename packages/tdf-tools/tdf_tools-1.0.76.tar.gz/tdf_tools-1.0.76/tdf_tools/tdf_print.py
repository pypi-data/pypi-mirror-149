#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 输出

import sys


def printStr(content):
    print(content)
    sys.stdout.flush()


def printDebug(content):
    print('============= debug info start=============')
    print(content)
    print('============= debug info end=============')
    sys.stdout.flush()


def printStage(content):
    print('\033[0;32mStage：{0} \033[0m'.format(
        content))
    # print('Stage：{0}'.format(content))
    sys.stdout.flush()


def printTitle(content):
    # print('Stage：{0}'.format(content))
    print('\033[0;32m<-----{0}----> \033[0m'.format(
        content))
    sys.stdout.flush()


def printError(content, shouldExit=True):
    # print('Error：{0}'.format(content))
    print('\033[0;31m {0} \033[0m'.format(content))
    sys.stdout.flush()
    if shouldExit:
        exit(-1)
