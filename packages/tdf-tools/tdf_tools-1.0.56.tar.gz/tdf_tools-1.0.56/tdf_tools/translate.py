# 如果本地没有googletrans，请使用3.1.0a0这个版本，以下为安装示例：

# 如果是python3
# sudo python3 -m pip install googletrans==3.1.0a0

# 如果是python
# pip install googletrans==3.1.0a0

from email.policy import strict
import re
import os
import shutil
import json
from googletrans import Translator
import sys
import platform
from tdf_tools.dir_fixed import goInTdfFlutterDir, goInShellDir

isWindow = platform.system().lower() == 'windows'

osTargetCommand = ''
if(isWindow):
    osTargetCommand = 'cd'
else:
    osTargetCommand = 'pwd'

# 备份壳模块路径
# shellPath = os.popen(osTargetCommand).read().split('\n')[0]

# targetModule = ''

# 源码依赖模块路径获取


def getSourceCodePackagePath(line):
    if line.startswith("#") == False:
        packagePath = line.split(':')[1].replace("%25", "%")
        return packagePath[0:len(packagePath) - 5]


# refre = False
# localRefre = True
# sourcePackage = ''
# with open(".packages") as lines:
#     for line in lines:
#         goInShellDir()
#         # os.chdir(shellPath)
#         if line.find(':file') == -1:
#             if line.find(targetModule) != -1:
#                 refre = True
#                 sourcePackage = getSourceCodePackagePath(line)
#         if line.find(targetModule) != -1 and line.find(':file') != -1:
#             localRefre = False
#     if refre == False:
#         print("未引用模块{0}❌".format(targetModule))
#         sys.exit(2)
#     if localRefre == False:
#         print("本地引用的模块才能生成国际化代码❌")
#         sys.exit(2)

# if (sourcePackage != None or sourcePackage != ''):
#     os.chdir(sourcePackage)


# translator = Translator()


def getCurrentPath():
    return os.popen(osTargetCommand).read().split('\n')[0]


def tdf_translate(content, dest_lan):
    try:
        translator = Translator()
        text = translator.translate(content, src='zh-cn', dest=dest_lan).text
        return text
    except:
        print("{0} 翻译失败".format(content))
        return ""


genDir = getCurrentPath()


# def getCurrentModuleName():
#     os.chdir(genDir)
#     if(isWindow):
#         return getCurrentPath().split("\\")[len(getCurrentPath().split("\\")) - 1]
#     else:
#         return getCurrentPath().split("/")[len(getCurrentPath().split("/")) - 1]

# 获取目标文件内已经存在的所有字段名


def getTargetFileParamsList(targetFileName):
    with open(targetFileName, 'r', encoding='utf8') as readF:
        try:
            print("解析{0}文件内json数据".format(targetFileName))
            fileData = readF.read()
            fileJsonData = correctJsonData(
                "".join(fileData.split("=")[1:]).replace(";", ""))
            jsonData = json.loads(fileJsonData, strict=False)
            jsonKeyList = []
            for item in jsonData:
                jsonKeyList.append(item)
            return jsonKeyList
        except Exception as e:
            print(e)
            exit(-1)


def correctJsonData(content):
    return content.replace("\n", "").replace(",}", "}")


def getManagerClassName(moduleName):
    strList = moduleName.split("_")
    result = ""
    for item in strList:
        result = result + item.capitalize()
    return result


def mapListCreater(emptyParams):
    if emptyParams:
        return ""
    with open(tdfIntlDir + '/i18n.json', 'r', encoding='utf8') as jsonF:
        json_data = json.loads(jsonF.read())
        result = ""
        for keyItem in json_data:
            if(isWindow):
                result = result + \
                    "  /// -  {0}\n".format(
                        json_data[keyItem].replace("\n", ""))
            else:
                result = result + \
                    "  /// -  {0}\n".format(
                        json_data[keyItem].replace("\n", ""))
                result = result + \
                    "  static String get {0} => getKey(\"{1}\");\n".format(
                        keyItem, keyItem)
        jsonF.close()
        return result


# emptyParams参数是否为空
def generateManagerClass(emptyParams, moduleName):
    # 生成manager类
    os.chdir(tdfIntlDir)

    with open(moduleName + "_i18n.dart", "w+", encoding='utf8') as managerF:
        managerF.truncate()
        managerF.write("""
import 'package:{0}/tdf_intl/i18n/{0}_th.dart';
import 'package:{0}/tdf_intl/i18n/{0}_en.dart';
import 'package:{0}/tdf_intl/i18n/{0}_zh_ch.dart';
import 'package:{0}/tdf_intl/i18n/{0}_zh_tw.dart';
import 'package:tdf_base_utils/src/data/language_data.dart';

class {1}I18n {{

  static Map<String, Map<String, String>>? i18nMap;
  static Map<String, Map<String, String>> getInstance() {{
    if (i18nMap == null) {{
      i18nMap = Map();
      i18nMap!["zh-ch"] = zhchMap;
      i18nMap!["zh-tw"] = zhtwMap;
      i18nMap!["en"] = enMap;
      i18nMap!["th"] = thMap;
    }}
    return i18nMap!;
  }}

  static String getKey(String key) {{
    return getInstance()[TDFLanguage.getLanguage()]?[key] ??
        getInstance()[TDFLanguage.getDefaultLanguage()]
        ?[key] ??
        "";
  }}
}}
""".format(moduleName, getManagerClassName(moduleName)))


# 入口
def generateTranslate(targetModule):

    global tdfIntlDir
    tdfIntlDir = ""
    if (os.path.exists('lib')):

        os.chdir(genDir + '/lib')
        if (os.path.exists('tdf_intl') == False):
            os.mkdir('tdf_intl')

    # 进入tdf_intl目录
    # tdf_intl文件夹下包含i18n文件夹，其中存放4个dart文件，分别对应四种语言
    # tdf_intl文件夹下还包含一个origin.txt文件，用于存放需要转化的文案，每个文案为一行
    goInTdfFlutterDir()
    os.chdir(targetModule)
    os.chdir('lib')
    if os.path.exists('tdf_intl') == False:
        os.mkdir('tdf_intl')
    os.chdir('tdf_intl')
    tdfIntlDir = getCurrentPath()
    os.chdir(tdfIntlDir)
    # 如果没有i18n文件夹则生成
    if (os.path.exists('i18n') == False):
        os.mkdir('i18n')

    os.chdir(tdfIntlDir)

    i18nList = ['zh-ch', 'en', 'th', 'zh-tw']

    if (os.path.exists('i18n.json') == False):
        initF = open(tdfIntlDir + '/i18n.json', 'w+', encoding='utf8')
        initF.write("{}")
        initF.close

        for targetFileNameSuffix in i18nList:
            os.chdir(tdfIntlDir + '/i18n')
            targetFileName = targetModule + "_" + \
                targetFileNameSuffix.replace("-", "_") + ".dart"

            if os.path.exists(targetFileName) == False:
                newI18nFile = open(targetFileName, "w+")
                newI18nFile.write(
                    "Map<String, String> " + targetFileNameSuffix.replace("-", "") + "Map = {\n};")
                newI18nFile.close

            generateManagerClass(True, targetModule)
    else:
        with open(tdfIntlDir + '/i18n.json', 'r', encoding='utf8') as originF:
            json_data = json.loads(originF.read())

            # 遍历i18n目录下的四个存放语言的dart文件
            for targetFileNameSuffix in i18nList:
                os.chdir(tdfIntlDir + '/i18n')
                print(
                    "------------------------------------------------------------------------------------")
                targetFileName = targetModule + "_" + \
                    targetFileNameSuffix.replace("-", "_") + ".dart"

                paramsResultList = getTargetFileParamsList(targetFileName)

                os.chdir(tdfIntlDir + '/i18n')

                with open(targetFileName, 'r', encoding='utf8') as targetFile:
                    fileContent = targetFile.read()
                    keyNode = fileContent.find("}")

                    addStr = ""
                    for item in json_data:
                        if len(paramsResultList) > 0 and item in paramsResultList:
                            continue
                        else:
                            if keyNode != -1:
                                if (targetFileNameSuffix.find('zh-ch') != -1):
                                    # print(json_data[item])
                                    addStr = addStr + \
                                        "\n  \"{0}\": \"{1}\",\n".format(
                                            item, json_data[item])
                                elif (targetFileNameSuffix.find('zh-tw') != -1):
                                    print(json_data[item])
                                    translateText = tdf_translate(
                                        json_data[item], targetFileNameSuffix)
                                    if translateText != "":
                                        addStr = addStr + "\n  \"{0}\": \"{1}\",\n".format(
                                            item, translateText)
                                # 其他语言不再进行翻译，自行填写
                                # else:
                                    # addStr = addStr + "\n  \"{0}\": \"{1}\",\n".format(item, tdf_translate(json_data[item], targetFileNameSuffix))

                    newFileContent = fileContent[:keyNode] + \
                        addStr + fileContent[keyNode:]
                    targetInertFile = open(
                        targetFileName, 'w+', encoding='utf8')
                    targetInertFile.write(newFileContent)
                    targetInertFile.close
                    print("\n新增: \n{0}\n".format(addStr))
                    targetFile.close
            originF.close()
            generateManagerClass(False, targetModule)
