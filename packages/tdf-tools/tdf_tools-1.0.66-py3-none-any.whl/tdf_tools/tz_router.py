# for example:
# python3 tz_router.py    # 遍历所有子模块生成路由map并注册到壳内
# python3 tz_router.py 模块名   # 为模块（如：tdf_account_module）生成路由描述文件，并遍历所有子模块生成路由map并注册到壳内

# 上述命令执行完会自动更新壳应用的路由文档

import os
from hashlib import md5
import shutil
import sys
import platform
from tdf_tools.dir_fixed import goInShellDir, getShellDir

isWindow = platform.system().lower() == 'windows'

osTargetCommand = ''
if(isWindow):
    osTargetCommand = 'cd'
else:
    osTargetCommand = 'pwd'

isUpdateTargetModule = False
targetModule = ''

macDownDataList = []  # 文档数据
mainPageData = []  # 业务入口页列表

packagesList = []  # 包含TZRouter注解页面的模块lib目录列表 item => {libPath:"", libName: ""}

entryPagePath = 'tdf-flutter://2dfire.com/business/entry'
entryPageNote = 'flutter entry'
entryPageWidget = 'TZRouterBusinessEntryPage'


class PackageNode:
    def __init__(self):
        self.packageName = ''
        # 存储的路径都是相对于shellPath的路径，所以在进入前需要先执行os.chdir(shellPath)
        self.packagePath = ''
        self.isRemote = False


# 备份壳模块路径
shellPath = os.popen(osTargetCommand).read().split('\n')[0]

# 判断业务组件下是否有依赖必须的build_runner和tdf_router_anno两个模块


def judgeHasBuildRunnerPackage(dirPath):
    hasBuildRunner = False
    hasRouterAnno = False
    os.chdir(dirPath)
    if (os.path.exists('.packages')):
        with open(".packages") as lines:
            for line in lines:
                if (line.find("build_runner") != -1):
                    hasBuildRunner = True
                if (line.find("tdf_router_anno") != -1):
                    hasRouterAnno = True
    return hasBuildRunner and hasRouterAnno

# 源码依赖模块路径获取


def getSourceCodePackagePath(line):
    packageName = line.split(':')[0]
    packagePath = line.split(':')[1].replace("%25", "%")
    if (packageName.find('tdf') != -1):
        packageNode = PackageNode()
        packageNode.packageName = packageName
        packageNode.packagePath = packagePath[0:len(packagePath) - 5]
        packageNode.isRemote = False
        return packageNode

# 远程依赖的模块生成代码


def getRemoteCodePackagePath(line):
    packageName = line.split(':file://')[0]
    packagePath = line.split(':file://')[1].replace("%25", "%")
    if (packageName.find('tdf') != -1):
        packageNode = PackageNode()
        packageNode.packageName = packageName
        if (isWindow):
            packageNode.packagePath = packagePath[1:len(packagePath) - 5]
        else:
            packageNode.packagePath = packagePath[0:len(packagePath) - 5]
        packageNode.isRemote = True
        return packageNode

# 生成代码


def generatorFunc():
    os.system('flutter packages pub run build_runner clean')
    os.system(
        'flutter packages pub run build_runner build --delete-conflicting-outputs')

# 判断指定目录下是否存在.tdf_router.dart结尾的文件


def hasRouterDartFile(dirPath):
    os.chdir(dirPath)
    nowaPath = os.popen(osTargetCommand).read().split("\n")[0]
    for root, dirs, files in os.walk(nowaPath):
        for file in files:
            src_file = os.path.join(root, file)
            if src_file.endswith('.tdf_router.dart'):
                return True
    return False


def defaultImportCreator(mFileWriter, content):
    mFileWriter.write("import {0}\n".format(content))

# 生成import数据


def importDataCreator(mFileWriter, itemModuleName, mFilePath, itemFileAlias):
    mFileWriter.write(
        "import \"package:{0}/{1}\" as {2};\n".format(itemModuleName, mFilePath, itemFileAlias))

# 路由map类生成器


def groupRouterClassCreator(mFileWriter, moduleName, list):
    content = """
routerMap() {{
    Map<String, TDFPageBuilder> map = Map();
    {1}
    return map;
}}


"""
    mFileWriter.write(content.format(moduleName, mapAddListCreator(list)))


def mapAddListCreator(list):
    content = ""
    for item in list:
        content += """map.putIfAbsent({0}.getRouterPath(), () =>  (String pageName, Map params, String _) => {1}.getPageWidget(params));
    """.format(item, item)
    return content


def mapMainPageAddListCreator(list):
    content = ""
    for item in list:
        content += """mainPageMap.putIfAbsent({0}.getNote(), {1}.getRouterPath());
    """.format(item, item)
    return content


def mapListCombineCreater(list):
    content = ""
    for item in list:
        content += "map.addAll({0}.routerMap());\n".format(item)
    content += "map.putIfAbsent(\"{0}\", () => (String pageName, Map params, String _) => {1}(params));".format(
        entryPagePath, entryPageWidget)
    return content


class routerNode:
    def __init__(self):
        self.package = ''
        self.routerPath = ''
        self.filePath = ''
        self.note = ''
        self.pageWidget = ''
        self.isMainPage = False


def addInMacDownData(routerFileList):
    for fileItem in routerFileList:
        with open(fileItem) as lines:
            node = routerNode()
            for line in lines:
                if (line.find("//#package#//") != -1):
                    node.package = line.split(
                        "//#package#//")[1].split("\n")[0]
                if (line.find("//#routerPath#//") != -1):
                    node.routerPath = line.split(
                        "//#routerPath#//")[1].split("\n")[0]
                if (line.find("//#filePath#//") != -1):
                    node.filePath = line.split(
                        "//#filePath#//")[1].split("\n")[0]
                if (line.find("//#note#//") != -1):
                    node.note = line.split("//#note#//")[1].split("\n")[0]
                if (line.find("//#pageWidget#//") != -1):
                    node.pageWidget = line.split(
                        "//#pageWidget#//")[1].split("\n")[0]
                if (line.find("//#isMainPage#//") != -1):
                    node.isMainPage = line.split(
                        "//#isMainPage#//")[1].split("\n")[0] == 'true'
            macDownDataList.append(node)
            if (node.isMainPage == True):
                mainPageData.append(node)


def addInWindowDownData(routerFileList):

    bytesTemp = bytes("\n", encoding="utf8")
    for fileItem in routerFileList:
        result = fileItem
        if(len(fileItem) > 260):
            temp = "\\\\?\\"
            temp2 = fileItem
            result = temp+fileItem
        with open(result, 'rb') as lines:
            node = routerNode()
            for line in lines:
                if (line.find(bytes(" //#package#//", encoding="utf8")) != -1):
                    node.package = line.split(
                        bytes("//#package#//", encoding="utf8"))[1].split(bytesTemp)[0]
                if (line.find(bytes("//#routerPath#//", encoding="utf8")) != -1):
                    node.routerPath = line.split(
                        bytes("//#routerPath#//", encoding="utf8"))[1].split(bytesTemp)[0]
                if (line.find(bytes("//#filePath#//", encoding="utf8")) != -1):
                    node.filePath = line.split(
                        bytes("//#filePath#//", encoding="utf8"))[1].split(bytesTemp)[0]
                if (line.find(bytes("//#note#//", encoding="utf8")) != -1):
                    node.note = str(line.split(
                        bytes("//#note#//", encoding="utf8"))[1].split(bytesTemp)[0], encoding="utf8")
                if (line.find(bytes("//#pageWidget#//", encoding="utf8")) != -1):
                    node.pageWidget = line.split(
                        bytes("//#pageWidget#//", encoding="utf8"))[1].split(bytesTemp)[0]
                if (line.find(bytes("//#isMainPage#//", encoding="utf8")) != -1):
                    node.isMainPage = line.split(
                        bytes("//#isMainPage#//", encoding="utf8"))[1].split(bytesTemp)[0] == 'true'
            macDownDataList.append(node)
            if (node.isMainPage == True):
                mainPageData.append(node)


def generateRouter(targetModule):
    goInShellDir()
    # 遍历壳应用.packages下的所有package,将所有tdf开头的模块都添加入packagesList中
    with open(".packages") as lines:
        for line in lines:
            goInShellDir()
            # os.chdir(shellPath)
            if (line.startswith('# ') is False):
                if (line.find(':file') != -1):
                    remotePackage = getRemoteCodePackagePath(line)
                    if (remotePackage != None):
                        packagesList.append(remotePackage)
                else:
                    sourcePackage = getSourceCodePackagePath(line)
                    if (sourcePackage != None):
                        packagesList.append(sourcePackage)

    # 上面已经拿到了所有的tdf库与其本地路径与是否是远程依赖
    isFind = False
    for item in packagesList:
        if (item.packageName == targetModule):
            isFind = True
            if (item.isRemote == False):
                if (judgeHasBuildRunnerPackage(item.packagePath)):
                    goInShellDir()
                    os.chdir(item.packagePath)
                    generatorFunc()
                else:
                    print("请确保模块{0}已依赖build_runner和tdf_router_anno两个包，可参考其他模块进行依赖配置❌".format(
                        targetModule))
            else:
                print("检测到模块{0}当前是远程依赖，无法生成路由描述文件❌".format(targetModule))

    if isFind == False and isUpdateTargetModule:
        print("未检测到模块{0}❌".format(targetModule))
        sys.exit(2)

    goInShellDir()
    os.chdir('lib')
    # os.chdir(shellPath + '/lib')
    if (os.path.exists('tz_router')):
        shutil.rmtree(r'tz_router')
    os.mkdir('tz_router')
    os.chdir('tz_router')
    os.mkdir('group')

    for packageItem in packagesList:
        # 存在路由描述文件才进行遍历
        goInShellDir()
        # os.chdir(shellPath)
        if (hasRouterDartFile(packageItem.packagePath)):
            os.chdir(shellPath + "/lib/tz_router/group/")
            os.mkdir(packageItem.packageName)
            os.chdir(packageItem.packageName)
            f = open('router_map.dart', 'w+')
            defaultImportCreator(f, "\'package:tdf_router/tdf_router.dart\';")

            goInShellDir()
            # os.chdir(shellPath)
            os.chdir(packageItem.packagePath + "/lib/")

            nowaPath = os.popen(osTargetCommand).read().split("\n")[0]

            routerAliasFileList = []
            routerFileList = []
            for root, dirs, files in os.walk(nowaPath):
                for file in files:
                    src_file = os.path.join(root, file)
                    if src_file.endswith('.tdf_router.dart'):
                        itemModuleName = packageItem.packageName
                        if(isWindow):
                            temp = src_file.split("\lib\\")[1]
                            itemFilePath = temp.replace("\\", "/")
                        else:
                            itemFilePath = src_file.split("/lib/")[1]
                        itemFileAlias = "tdf_router_" + \
                            md5(itemFilePath.encode()).hexdigest()[8:-8]

                        importDataCreator(f, itemModuleName,
                                          itemFilePath, itemFileAlias)
                        routerAliasFileList.append(itemFileAlias)
                        routerFileList.append(src_file)
            if (len(routerAliasFileList) > 0):
                print("模块{:>30}  检测到  {:>3}  个路由".format(
                    packageItem.packageName, len(routerAliasFileList)))
                groupRouterClassCreator(
                    f, packageItem.packageName, routerAliasFileList)
                if(isWindow):
                    addInWindowDownData(routerFileList)
                else:
                    addInMacDownData(routerFileList)

            f.close()

    goInShellDir()
    os.chdir('lib/tz_router')
    # os.chdir(shellPath + "/lib/tz_router")

    initF = open('init.dart', 'w+')

    # 生成初始化init文件
    if (os.path.exists("group") == False):
        os.mkdir('group')
    os.chdir('group')
    nowaPath = os.popen(osTargetCommand).read().split("\n")[0]
    defaultImportCreator(initF, "\'package:tdf_router/tdf_router.dart\';")
    # 添加flutter业务入口页面import
    defaultImportCreator(initF, "\'entry/tz_router_entry_page.dart\';")
    mapList = []
    for root, dirs, files in os.walk(nowaPath):
        for file in files:
            src_file = os.path.join(root, file)
            if (src_file.find("init.dart") != -1):
                continue
            if(isWindow):
                tmpItemFilePath = src_file.split("tz_router")[1]
                itemFilePath = tmpItemFilePath.replace("\\", "/")
            else:
                itemFilePath = src_file.split("tz_router")[1]
            itemFileAlias = "router_map_" + \
                md5(itemFilePath.encode()).hexdigest()[8:-8]
            importContent = "import \".{0}\" as {1};\n".format(
                itemFilePath, itemFileAlias)
            initF.write(importContent)
            mapList.append(itemFileAlias)

    initF.write(
        """

    class TZRouterManager {{
        static combineMap() {{
            Map<String, TDFPageBuilder> map = Map();
            {0}
            return map;
        }}
    }}
    """.format(mapListCombineCreater(mapList)))

    initF.close()

    def mainPageDataCreator():
        content = ""
        for item in mainPageData:
            if (item.isMainPage):
                content += "\"{0}\":\"{1}\",\n".format(
                    item.note, item.routerPath)
        return content

    goInShellDir()
    os.chdir('lib/tz_router')
    # os.chdir(shellPath + "/lib/tz_router")
    if (os.path.exists("entry") == False):
        os.mkdir('entry')

    os.chdir('entry')

    entryPageF = open('tz_router_entry_page.dart', 'w+')

    defaultImportCreator(entryPageF, "\'package:flutter/material.dart\';")
    defaultImportCreator(entryPageF, "\'package:tdf_router/tdf_router.dart\';")
    defaultImportCreator(
        entryPageF, "\'package:tdf_router_anno/router/router_anno.dart\';")
    defaultImportCreator(
        entryPageF, "\'package:tdf_base_utils/tdf_base_utils.dart\';")
    defaultImportCreator(
        entryPageF, "\'package:tdf_widgets/tdf_common_btn/tdf_btn.dart\';")
    defaultImportCreator(
        entryPageF, "\'package:tdf_widgets/title_bar/tdf_title_bar.dart\';")
    defaultImportCreator(
        entryPageF, "\'package:tdf_widgets/background/tdf_native_background.dart\';")
    entryPageF.write("""

    @TZRouter(path: '{0}', note: '{1}')
    class {2} extends StatefulWidget {{
        final Map params;

        {2}(this.params);

        @override
        _{2}State createState() => _{2}State();
    }}

    class _{2}State extends State<{2}> {{
        final TextEditingController routerController = new TextEditingController();
        final TextEditingController controller = new TextEditingController();
        final Map<String, String> pageMap = {{
        {3}
        }};

        @override
        Widget build(BuildContext context) {{
            TDFScreen.init(context);
            return Scaffold(
                backgroundColor: Color(0xffffffff),
                appBar: TDFTitleBar(
                    titleContent: \"{4}\",
                    backType: TDFTitleBackWidgetType.DEFAULT_BACK,
                ),
                body: SingleChildScrollView(
                    child: Column(
                        children: _getButtonList(),
                    ),
                ),
            );
        }}

        List<Widget> _getButtonList() {{
            List<Widget> list = [];
            list.add(_routerJumpWidget());
            list.add(Padding(
            padding: EdgeInsets.only(top: 20.w),
            child: TDFButton(
                content: \"根据路由跳转\",
                bgColor: 0xff0088ff,
                contentColor: 0xffffffff,
                onClick: () {{
                FocusScope.of(context).requestFocus(FocusNode());
                TDFRouter.open(routerController.text);
                }},
            ),
            ));
            list.add(_searchWidget());

            List<Widget> wrapEntrylist = [];
            pageMap.forEach((key, value) {{
            if (key.contains(controller.text)) {{
                wrapEntrylist.add(GestureDetector(
                    onTap: () {{
                    FocusScope.of(context).requestFocus(FocusNode());
                    TDFRouter.open(value);
                    }},
                    child: ClipRRect(
                    borderRadius: BorderRadius.all(Radius.circular(3.w)),
                    child: Container(
                        color: Colors.blue,
                        padding: EdgeInsets.only(
                            left: 7.w, right: 7.w, top: 4.w, bottom: 4.w),
                        child: Text(
                        key,
                        style: TextStyle(fontSize: 13.w),
                        ),
                    ),
                    )));
            }}
            }});
            list.add(SizedBox(
            height: 20.w,
            ));
            list.add(Wrap(
            spacing: 15.w,
            runSpacing: 10.w,
            children: wrapEntrylist,
            ));
            return list;
        }}

        Widget _routerJumpWidget() {{
            return TextField(
            controller: routerController,
            autofocus: false,
            decoration: InputDecoration(hintText: "输入页面路由"),
            onChanged: (value) {{
                setState(() {{}});
                }},
            );
        }}

        Widget _searchWidget() {{
            return TextField(
                controller: controller,
                autofocus: false,
                decoration: InputDecoration(hintText: "筛选"),
                onChanged: (value) {{
                    setState(() {{}});
                }},
            );
        }}
        

    }}
    """.format(entryPagePath, entryPageNote, entryPageWidget, mainPageDataCreator(), entryPageNote))
    entryPageF.close()

    goInShellDir()
    # os.chdir(shellPath)
    if (os.path.exists("路由文档") == True):
        shutil.rmtree(r'路由文档')
    os.mkdir("路由文档")
    os.chdir("路由文档")

    f = open('document.md', 'w+')

    goInShellDir()
    # os.chdir(shellPath)
    curDir = getShellDir()
    for root, dirs, files in os.walk(curDir):
        for file in files:
            src_file = os.path.join(root, file)
            if (src_file.find("pubspec.yaml") != -1):
                if(isWindow):
                    with open("pubspec.yaml", "rb") as lines:
                        for line in lines:
                            if (line.find(bytes("name: ", encoding="utf8")) != -1):
                                f.write("## Flutter壳应用（{0}）路由表\n".format(line.split(
                                    bytes("name: ", encoding="utf8"))[1].split(bytes("\n", encoding="utf8"))[0]))
                            break
                else:
                    with open("pubspec.yaml") as lines:
                        for line in lines:
                            if (line.find("name: ") != -1):
                                f.write("## Flutter壳应用（{0}）路由表\n".format(
                                    line.split("name: ")[1].split("\n")[0]))
                            break

    f.write("<table><thead><tr><th>{0}</th><th style = \"min-width:150px !important\">{1}</th><th>{2}</th><th>{3}</th><th>{4}</th></tr></thead>".format(
        "组件名", "描述", "路由path", "类名", "文件路径"))
    f.write("<tbody>")

    currentPackage = ""
    for item in macDownDataList:
        if (currentPackage == item.package):
            f.write("<tr><th>{0}</th><th>{1}</th><th>{2}</th><th>{3}</th><th>{4}</th></tr>\n".format(
                "", item.note, item.routerPath, item.pageWidget, item.filePath))
        else:
            currentPackage = item.package
            f.write("<tr><th>{0}</th><th>{1}</th><th>{2}</th><th>{3}</th><th>{4}</th></tr>\n".format(
                item.package, item.note, item.routerPath, item.pageWidget, item.filePath))

    f.write("</tbody></table>")

    f.close()
