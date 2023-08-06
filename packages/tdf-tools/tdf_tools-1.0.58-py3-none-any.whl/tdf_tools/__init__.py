#!/usr/bin/env python
# encoding=utf-8

import getopt
import json
import os
import shutil
import subprocess
import sys
# sys.path.append(r"/Users/xujian/Documents/2022_2dfire/flutter/package_tools")
from tdf_tools.tz_router import generateRouter
from tdf_tools.seal_off_package_utils import tagInfoObj, changeVersionAndDependencies, createAndPushTag
from tdf_tools.dependencies_analysis import DependencyAnalysis
from tdf_tools.gitlab_utils import GitlabUtils
from tdf_tools.module_dependencies_rewrite import ModuleDependenciesRewriteUtil
from tdf_tools.python_gitlab_api import GitlabAPI
from tdf_tools.tdf_print import printError, printStage, printStr
from tdf_tools.initial_data import getShellBranch, initialJsonFunc, getInitJsonData, getModuleNameList, getModuleJsonData
from tdf_tools.dir_fixed import goInTdfFlutterDir
from tdf_tools.tdf_print import printTitle
from tdf_tools.dir_fixed import goInShellDir
from tdf_tools.translate import generateTranslate


def init():

    # 初始化json数据
    initialJsonFunc()

    goInTdfFlutterDir()

    global initJsonData
    initJsonData = getInitJsonData()

    global featureBranch
    featureBranch = initJsonData['featureBranch']

    global shellName
    shellName = initJsonData['shellName']

    global moduleNameList
    moduleNameList = getModuleNameList()

    global moduleJsonData
    moduleJsonData = getModuleJsonData()

    extraFunc()

    process()


def processHelp():
    txt = \
        """
        -h or --help:           输出帮助文档
        -c :                  对所有模块执行自定义 git 命令, 例如: -c git status.

        项目初始化
        ------------------------------------------------------------------------
        init                    请确保已配置initial_config.json文件，然后会执行以下步骤：
                                1.clone所有配置的模块
                                2.切换所有模块的分支到配置的feature分支
                                3.重写所有依赖为本地依赖
        deps                    修改initial_config.json文件后，执行该命令，更新依赖
        upgrade                 升级tdf_tools包版本
        module-update           更新存储项目git信息的json文件
        open                    打开vscode，同时将所有模块添加入vscode中


        封包工具相关
        ------------------------------------------------------------------------
        map                     以二维数组形式输出模块的依赖顺序，每一item列表代表可同时打tag的模块
        tagInfo                 输出一个json，每一节点包含一个模块，内部包含
                                remote：远程最新版本号，current：模块内配置的版本号，upgrade：对比自增后的版本号，sort模块打tag顺序
                                sort相同即代表可同时打tag
        prepareTagTask          修改yaml中的tag号和所有的依赖，该命令可看成是做打tag前的准备工作，把依赖规范化
        tag                     批量tag操作，参数通过逗号隔开，不要有空格。如tdf_tools tag tdf_widgets,tdf_event


        路由相关
        ------------------------------------------------------------------------
        router                  执行tdf_tools router后，会以交互式进行路由操作，对指定的模块执行路由生成和路由注册逻辑


        国际化相关
        ------------------------------------------------------------------------
        translate                  执行tdf_tools translate后，会以交互式进行路由操作，对指定的模块执行国际化代码生成


        git相关
        ------------------------------------------------------------------------
        status                              聚合展示所有模块的仓库状态
        commit                              对所有模块执行add 和 commit
        diff                                对所有模块执行 git diff --name-only 当前分支..master
        diff [branch]                       对所有模块执行 git diff --name-only 当前分支..[branch]
        pull or sync                        对所有模块执行 git pull
        checkout                            对所有模块执行 git checkout 切换到配置在initial_config.json中的feature分支
        checkout [branch]                   对所有模块执行 git checkout branch
        cfb [branch] -p                     对所有模块执行 git checkout 并push到远程，跟踪来自 'origin' 的远程分支
        merge                               对所有模块执行 git merge
        branch                              聚合展示所有模块的当前分支
        push                                对所有模块执行 git push origin 当前分支
        mr -c sourceBranch targetBranch     对所有模块提交一个merge request 源分支sourceBranch，目标分支targetBranch
        """
    print(txt)


name = "tdf_tools"

# 校验配置是否正确，所有需要开发的库是否存在于模块配置json文件中


def validateConfig(moduleJsonData):
    moduleNameList = getModuleNameList()
    for module in moduleNameList:
        if module not in moduleJsonData.keys():
            printError(
                "配置的开发模块{0}没有找到git仓库信息。请确保 1. 模块名配置正确； 2. 执行 tdf_tools module-update 更新git信息配置文件".format(module))


# 更新模块配置信息
def initModuleConfig():
    FLUTTER_GROUP_ID = "1398"  # Flutter仓库组

    HPP_FLUTTER_GROUP_ID = "1489"  # 火拼拼的Flutter仓库组
    FLUTTER_REPOSITORY_GROUP_IDS = [FLUTTER_GROUP_ID, HPP_FLUTTER_GROUP_ID]

    # start
    projectInfo = dict()

    api = GitlabAPI()

    for groupId in FLUTTER_REPOSITORY_GROUP_IDS:
        groupProjectList = api.get_all_projects_in_group(groupId)
        for project in groupProjectList:
            tup = api.getContent(project.id, project.name)
            if tup[0] == True:
                print("{0}, {1}, {2}, {3}".format(
                    tup[1], project.id, project.ssh_url_to_repo, project.namespace['name']))
                projectInfo[tup[1]] = dict()
                projectInfo[tup[1]]['id'] = project.id
                projectInfo[tup[1]]['git'] = project.ssh_url_to_repo
                projectInfo[tup[1]]['type'] = project.namespace['name']

    goInTdfFlutterDir()
    os.chdir('flutter_module_config')
    file = 'module_config.json'
    if os.path.exists(file):
        os.remove(file)
    f = open(file, 'w+')
    f.write(json.dumps(projectInfo, indent=2))
    f.close()
    printStr(projectInfo)


def extraFunc():
    options, args = getopt.getopt(
        sys.argv[1:], 'chd:r:', ['help', 'dr', 'rd'])
    for name, value in options:
        if name in ('-h', '--help'):
            processHelp()
            exit(0)
        elif name == '-c':
            rawCMD(args)
            exit(0)
    if len(args) >= 1:
        arg = args[0]
        if arg == 'upgrade':
            os.system("python3 -m pip install --upgrade tdf-tools --user")
            exit(0)
        if arg == 'module-update':
            goInTdfFlutterDir()
            if (os.path.exists('flutter_module_config')):
                shutil.rmtree(r'flutter_module_config')

            # TODO 地址要换
            os.system(
                'git clone git@git.2dfire.net:app/flutter/tools/flutter_module_config.git')
            os.chdir('flutter_module_config')
            initModuleConfig()

            goInTdfFlutterDir()
            os.chdir('flutter_module_config')

            os.system('git add .')
            os.system('git commit -m \'更新模块git信息配置文件\'')
            os.system('git push')

            goInTdfFlutterDir()

            if (os.path.exists('flutter_module_config')):
                shutil.rmtree(r'flutter_module_config')
            exit(0)


def initCMDInvalidate():
    goInTdfFlutterDir()
    mDir = os.getcwd()

    for root, dirs, files in os.walk(mDir):
        if len(files) > 0:
            printError("请确保下面的目录中不存在子模块,请手动删除\n{0}".format(mDir))

# 初始化操作


def initCMD():
    gitlabUtils = GitlabUtils()
    gitlabApi = GitlabAPI()

    for module in moduleNameList:
        printTitle(module)
        goInTdfFlutterDir()
        gitlabUtils.clone(module, moduleJsonData[module]['git'])
        os.chdir(module)
        gitlabApi.createBranch(moduleJsonData[module]['id'], featureBranch)
        gitlabUtils.pull()
        gitlabUtils.checkout(featureBranch)
    # 依赖 重写
    reWrite = ModuleDependenciesRewriteUtil()
    reWrite.rewrite()


def statusCMD():
    gitlabUtils = GitlabUtils()
    for module in moduleNameList:
        printTitle(module)
        goInTdfFlutterDir()
        os.chdir(module)
        gitlabUtils.status()
    # 壳
    printTitle(shellName)
    goInShellDir()
    gitlabUtils.status()


def diffCMD(args):
    gitlabUtils = GitlabUtils()
    for module in moduleNameList:
        printTitle(module)
        goInTdfFlutterDir()
        os.chdir(module)
        if len(args) > 1:
            gitlabUtils.diff(args[1])
        else:
            gitlabUtils.diff()
    # 壳
    printTitle(shellName)
    goInShellDir()
    if len(args) > 1:
        gitlabUtils.diff(args[1])
    else:
        gitlabUtils.diff()


def commitCMD(args):
    gitlabUtils = GitlabUtils()
    for module in moduleNameList:
        printTitle(module)
        goInTdfFlutterDir()
        os.chdir(module)

        if len(args) > 1:
            gitlabUtils.commit("\"{0}\"".format(''.join(args[1:])))
        else:
            printError(
                "no commit message, please exec Example: tdf_tools commit \"message\"")
    # 壳
    printTitle(shellName)
    goInShellDir()
    if len(args) > 1:
        gitlabUtils.commit("\"{0}\"".format(''.join(args[1:])))
    else:
        printError(
            "no commit message, please exec Example: tdf_tools commit \"message\"")


def syncCMD():
    gitlabUtils = GitlabUtils()
    for module in moduleNameList:
        printTitle(module)
        goInTdfFlutterDir()
        os.chdir(module)
        gitlabUtils.pull()
    # 壳
    printTitle(shellName)
    goInShellDir()
    gitlabUtils.pull()


def rawCMD(args):
    gitlabUtils = GitlabUtils()
    for module in moduleNameList:
        printTitle(module)
        goInTdfFlutterDir()
        os.chdir(module)
        rawGitCommand = ' '.join(args)
        gitlabUtils.executeRawCommand(rawGitCommand)
    # 壳
    printTitle(shellName)
    goInShellDir()
    rawGitCommand = ' '.join(args)
    gitlabUtils.executeRawCommand(rawGitCommand)


def pushCMD():
    gitlabUtils = GitlabUtils()
    for module in moduleNameList:
        printTitle(module)
        goInTdfFlutterDir()
        os.chdir(module)
        gitlabUtils.push()
    # 壳
    printTitle(shellName)
    goInShellDir()
    gitlabUtils.push()


def branchCMD():
    gitlabUtils = GitlabUtils()
    for module in moduleNameList:
        printTitle(module)
        goInTdfFlutterDir()
        os.chdir(module)
        printStr(gitlabUtils._getCurBranch())

    # 壳
    printTitle(shellName)
    goInShellDir()
    printStr(gitlabUtils._getCurBranch())


def checkoutCMD(args):
    branch = featureBranch
    gitlabUtils = GitlabUtils()
    if len(args) == 2:
        branch = args[1]

    for module in moduleNameList:
        printTitle(module)
        goInTdfFlutterDir()
        os.chdir(module)
        gitlabUtils.checkout(branch)
    # 壳
    printTitle(shellName)
    goInShellDir()
    gitlabUtils.checkout(branch)


def createAndCheckoutCMD(args):
    branch = featureBranch
    shouldPush = False
    gitlabUtils = GitlabUtils()
    if len(args) > 2:
        if args[2] == "-p":
            branch = args[1]
            shouldPush = True
        else:
            branch = args[1]
    elif len(args) > 1:
        branch = args[1]

    for module in moduleNameList:
        printTitle(module)
        goInTdfFlutterDir()
        os.chdir(module)
        gitlabUtils.createAndCheckout(branch, shouldPush)
    # 壳
    printTitle(shellName)
    goInShellDir()
    gitlabUtils.createAndCheckout(branch, shouldPush)


def mergeCMD(args):
    gitlabUtils = GitlabUtils()
    for module in moduleNameList:
        printTitle(module)
        goInTdfFlutterDir()
        os.chdir(module)
        if len(args) > 1:
            gitlabUtils.merge(args[1])
        else:
            printStr("请指定需要合并的分支")

    # 壳
    printTitle(shellName)
    goInShellDir()
    if len(args) > 1:
        gitlabUtils.merge(args[1])
    else:
        printStr("请指定需要合并的分支")


def mr(sourceBranch, targetBranch):
    gitlabUtils = GitlabUtils()
    gitlabUtils.mergeRequestCreate(sourceBranch, targetBranch)


def mrCMD(args):
    if len(args) > 2:
        if args[1] == '-c' and len(args) == 4:
            mr(args[2], args[3])
        elif args[1] == '-c' and len(args) != 4:
            printError("参数不正确，请使用：tdf_tools mr -c sourceBranch targetBranch")
    else:
        printError("参数不正确，请使用：tdf_tools mr -c sourceBranch targetBranch")


def depsCMD():
    gitlabUtils = GitlabUtils()
    gitlabApi = GitlabAPI()

    for module in moduleNameList:
        printTitle(module)
        goInTdfFlutterDir()
        if os.path.exists(module) is not True:
            gitlabUtils.clone(module, moduleJsonData[module]['git'])
        os.chdir(module)
        gitlabApi.createBranch(moduleJsonData[module]['id'], featureBranch)
        gitlabUtils.fetch()  # deps时拉取远程commit和所有分支，不合并，所以不能用pull
        gitlabUtils.checkout(featureBranch)
    # 依赖 重写
    reWrite = ModuleDependenciesRewriteUtil()
    reWrite.rewrite(reWriteOnlyChange=True)


def mapCMD():
    analysis = DependencyAnalysis()
    json = analysis.generate()
    exit(json)


def vscodeOpen():
    goInShellDir()
    os.chdir(os.path.abspath(r".."))

    os.system('code -n')

    shellName = initJsonData['shellName']

    os.system('code -a .tdf_flutter -a {0}'.format(shellName))


def _runCmd(cmd):
    subprocess_result = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE)
    subprocess_return = subprocess_result.stdout.read()
    return subprocess_return.decode('utf-8')


def statusValidate():
    global shouldExit
    shouldExit = False
    # 壳模块文件修改校验
    if (_runCmd('git status -s') == '') is not True:
        shouldExit = True
        printError(shellName + '模块有文件更新，限制继续执行')

    for module in moduleNameList:
        goInTdfFlutterDir()
        os.chdir(module)
        if (_runCmd('git status -s') == '') is not True:
            shouldExit = True
            printError(module + '模块有文件更新，限制继续执行')
    if shouldExit:
        exit(1)

    goInShellDir()


def tagInfoCMD():
    tagInfoObj()


def prepareTagTask(jsonData):
    changeVersionAndDependencies(jsonData)


def tag(moduleNameStr):
    createAndPushTag(moduleNameStr.split(','))


def tzRouter():
    businessModuleList = []
    for item in moduleNameList:
        if moduleJsonData[item]['type'] == 'modules' or moduleJsonData[item]['type'] == 'libs':
            businessModuleList.append(item)

    print('检测到以下模块可执行路由脚本：')
    print(businessModuleList)
    while True:
        inputStr = input('请输入需要执行路由脚本的模块名(input ! 退出)：')
        if inputStr == '!' or inputStr == '！':
            exit(0)
        if inputStr in businessModuleList:
            generateRouter(inputStr)
            exit(0)


def translate():
    businessModuleList = []
    for item in moduleNameList:
        if moduleJsonData[item]['type'] == 'modules' or moduleJsonData[item]['type'] == 'libs':
            businessModuleList.append(item)

    print('检测到以下模块可执行路由脚本：')
    print(businessModuleList)
    while True:
        inputStr = input('请输入需要执行路由脚本的模块名(input ! 退出)：')
        if inputStr == '!' or inputStr == '！':
            exit(0)
        if inputStr in businessModuleList:
            print("国家化脚本开始执行")
            generateTranslate(inputStr)
            exit(0)


def process():

    validateConfig(moduleJsonData)

    try:
        options, args = getopt.getopt(
            sys.argv[1:], 'chd:r:', ['help', 'dr', 'rd'])
        if len(args) >= 1:
            arg = args[0]
            if arg == 'init':
                initCMDInvalidate()
                initCMD()
                vscodeOpen()
            elif arg == 'open':
                vscodeOpen()
            elif arg == 'status':
                statusCMD()
            elif arg == 'diff':
                diffCMD(args)
            elif arg == 'commit':  # add . and commit
                commitCMD(args)
            elif arg == 'pull' or arg == 'sync':
                syncCMD()
            elif arg == 'push':
                pushCMD()
            elif arg == 'branch':
                branchCMD()
            elif arg == 'checkout':
                checkoutCMD(args)
            elif arg == 'cfb':
                createAndCheckoutCMD(args)
            elif arg == 'merge':
                mergeCMD(args)
            elif arg == 'mr':
                mrCMD(args)
            elif arg == 'deps':
                # statusValidate()
                depsCMD()
            elif arg == 'map':
                mapCMD()
            elif arg == 'tagInfo':
                tagInfoCMD()
            elif arg == 'prepareTagTask':
                if len(args) > 1:
                    jsonData = json.loads(''.join(args[1:]).replace(" ", ""))
                    prepareTagTask(jsonData)
            elif arg == 'tag':
                if len(args) == 2:
                    tag(args[1])
            elif arg == 'router':
                tzRouter()
            elif arg == 'translate':
                translate()
            exit(0)

    except getopt.GetoptError as err:
        printError(f"{err}, see 'tdf_tools -h or --help'")


# init()
