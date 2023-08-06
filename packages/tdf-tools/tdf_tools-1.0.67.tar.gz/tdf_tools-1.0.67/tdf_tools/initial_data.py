#!/usr/bin/env python
# encoding=utf-8

import json
import os
import subprocess
from tdf_tools.dir_fixed import goTdfCacheDir, goInShellDir
from tdf_tools.python_gitlab_api import GitlabAPI
from tdf_tools.tdf_print import printDebug, printStage, printStr
from ruamel import yaml

from tdf_tools.tdf_print import printError
from tdf_tools.dir_fixed import goInTdfFlutterDir


def _runCmd(cmd):
    subprocess_result = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE)
    subprocess_return = subprocess_result.stdout.read()
    return subprocess_return.decode('utf-8')


def getShellBranch():
    featureBranch = _runCmd(
        'git rev-parse --abbrev-ref HEAD').replace("\n", "")
    return featureBranch


def shellModuleSet():
    appList = []
    idList = []
    for item in moduleJson:
        if moduleJson[item]['type'] == 'app':
            appList.append(item)
    printStr("壳模块列表：")
    i = 0
    for item in appList:
        i = i + 1
        idList.append(str(i))
        printStr("{0}.{1}".format(i, item))

    global selectedId
    while True:
        selectedId = input('请从以上模块中选择一个壳模块，输入序号即可：')
        if selectedId in idList:
            break

    i = 0
    for item in appList:
        i = i + 1
        if i == int(selectedId):
            print('选择模块：{0}'.format(item))
            return item


def createCache(moduleJson):
    global featureBranch
    global shellModule
    global moduleList
    # 初始化开发分支
    featureBranch = getShellBranch()
    # 初始化壳模块
    goInShellDir()

    with open('pubspec.yaml', 'r', encoding='utf-8') as rF:
        dic = yaml.round_trip_load(rF.read())
        if dic != None and dic.__contains__("name"):
            shellModule = dic['name']
        else:
            printError('读取壳模块模块名失败，请确保壳模块的pubspec.yaml配置了name属性')

    # 初始化开发的模块列表
    moduleList = []
    while True:
        moduleName = input('输入需要开发的模块名:(添加:+name，删除:-name，完成输入:!):')
        if moduleName != '':
            if moduleName == '!' or moduleName == '！':
                break
            if moduleJson.get(moduleName[1:], -1) != -1:
                if moduleName[0] == '+':
                    moduleList.append(moduleName[1:])
                    print('模块{0}已添加'.format(moduleName[1:]))
                elif moduleName[0] == '-':
                    moduleList.remove(moduleName[1:])
                    print('模块{0}已移除'.format(moduleName[1:]))
            else:
                if moduleName[0] == '+':
                    print("未从仓库中找到模块{0}，添加失败".format(moduleName[1:]))
                elif moduleName[0] == '-':
                    print("已添加模块列表中未找到模块{0}".format(moduleName[1:]))
            moduleList = list(dict.fromkeys(moduleList))

            print('已选模块列表：{0}'.format(moduleList))

    goTdfCacheDir()

    with open('initial_config.json', 'w', encoding='utf-8') as wf:
        initialDic = dict()
        initialDic['featureBranch'] = featureBranch
        initialDic['shellName'] = shellModule
        initialDic['moduleNameList'] = moduleList
        wf.write(json.dumps(initialDic, indent=2))
        wf.close()


def initModuleConfigJson():
    gitlabApi = GitlabAPI()
    moduleJson = gitlabApi.getModuleConfigJson()

    goTdfCacheDir()
    with open('module_config.json', 'w', encoding='utf-8') as wF:
        wF.write(json.dumps(moduleJson, indent=2))
        wF.close()
    return moduleJson


def getInitJsonData():  # 获取项目初始化数据
    goTdfCacheDir()
    with open('initial_config.json', 'r', encoding='utf-8') as readF:
        fileData = readF.read()
        readF.close()
        return json.loads(fileData)


def initialJsonFunc():
    global moduleJson

    goTdfCacheDir()

    if os.path.exists('module_config.json') == False:
        printStr('未发现module_config.json文件')
        printStr('创建module_config.json文件...')
        moduleJson = initModuleConfigJson()
        printStr('创建完成')
    else:
        with open('module_config.json', 'r', encoding='utf-8') as readF:
            moduleJson = json.loads(readF.read())
            readF.close()

    goTdfCacheDir()

    if os.path.exists('initial_config.json') == False:
        createCache(moduleJson)


def getModuleJsonData():  # 获取模块 git相关配置信息
    goTdfCacheDir()
    with open('module_config.json', 'r', encoding='utf-8') as readF:
        fileData = readF.read()
        readF.close()
        return json.loads(fileData)


def getModuleNameList():
    initJsonData = getInitJsonData()
    if (initJsonData.__contains__('moduleNameList') and isinstance(initJsonData['moduleNameList'], list)):
        moduleNameList = initJsonData['moduleNameList']
        return moduleNameList
    else:
        printError("❌ 请配置moduleNameList的值,以数组形式")
