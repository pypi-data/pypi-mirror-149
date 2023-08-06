#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# gitlab api

import gitlab
from ruamel import yaml
import json
import os

from tdf_tools.tdf_print import printStr

HOST = "https://git.2dfire.net"


def getPrivateToken():
    homedir = os.path.expanduser('~')
    os.chdir(homedir)
    global token
    token = ''
    if os.path.exists('.tdf_tools_config'):
        f = open(".tdf_tools_config")
        line = f.readline()
        while line:
            if line.__contains__('='):
                key = line.split('=')[0]
                value = line.split('=')[1]
                if key == 'git_private_token':
                    token = value.replace("\n", "")
            line = f.readline()

        f.close()
    else:
        print(
            "不存在~/.tdf_tools_config文件，请创建并配置相关必需属性如下")
        print("git_private_token=***")
        exit(-1)
    return token


class GitlabAPI(object):

    def __init__(self):
        private_token = getPrivateToken()
        self.gl = gitlab.Gitlab(HOST, private_token=private_token,
                                api_version='4')

    def get_all_projects_in_group(self, group_id):
        # 拿到顶层group
        print("读取groupId为{0}的仓库内所有项目...".format(group_id))
        group = self.gl.groups.get(group_id)
        projects = group.projects.list(include_subgroups=True, all=True)
        print("读取完成")
        return projects

    # 通过项目id获取yaml文件内容
    def getContent(self, project_id, project_name):
        project = self.gl.projects.get(project_id)
        try:
            print("读取模块：{0}".format(project_name))
            f = project.files.get(file_path='pubspec.yaml', ref='master')
            doc = yaml.round_trip_load(f.decode())
            print("写入配置文件")
            return (True, doc['name'], True)
        except:
            print("没有yaml文件，不是flutter模块")
            return (False, '', False)

    # 获取module_config.json文件内容
    def getModuleConfigJson(self):
        project = self.gl.projects.get(6093)
        try:
            f = project.files.get(file_path='module_config.json', ref='master')
            return json.loads(f.decode())
        except:
            print("读取module_config.json失败")

    # 为project创建分支
    def createBranch(self, project_id, branch):
        project = self.gl.projects.get(project_id)
        try:
            project.branches.get(branch)
            printStr("远端分支{0}已存在".format(branch))
        except:
            printStr("远程分支不存在，创建...")
            project.branches.create({'branch': branch, 'ref': 'master'})

    def createMR(self, project_id, source_branch, target_branch, title='default'):
        project = self.gl.projects.get(project_id)
        try:
            project.mergerequests.create(
                {'source_branch': source_branch, 'target_branch': target_branch, 'assignee_id': 819, 'title': title})
        except Exception as e:
            printStr("MR创建失败")
            printStr(e)
            # sys.stdout.flush()
