#!/usr/bin/env python3
# coding = utf8
import platform
import shutil
import sys
import os
current_user_path = os.path.abspath('.')
if platform.system() == 'Windows':
    path_separator = '\\'
else:
    path_separator = '/'


def make_path(
        path: str = None,
        overwrite: bool = False,  # 是否覆盖
        silence: bool = False
):
    """
    按照目录逐级创建
    """
    if path is None:
        return
    else:
        path_list = str(path).split(path_separator)
        path_temp = ""
        for each_path in path_list:
            path_temp = path_temp + each_path + path_separator
            if overwrite is False:
                if os.path.exists(path_temp) is True:
                    if silence is True:
                        pass
                    else:
                        print("==> 目录[ %s ]已存在..." % path_temp)
                else:
                    if silence is True:
                        pass
                    else:
                        print("==> 目录[ %s ]创建中..." % path_temp, end=" ==> ")
                    os.mkdir(path_temp)
            else:
                if os.path.exists(path_temp) is True:
                    if silence is True:
                        pass
                    else:
                        print("==> 目录[ %s ]已存在，将覆盖..." % path_temp)
                    shutil.rmtree(path_temp)
                    os.mkdir(path_temp)
                else:
                    if silence is True:
                        pass
                    else:
                        print("==> 目录[ %s ]创建中..." % path_temp, end=" ==> ")
                    os.mkdir(path_temp)
        return path


def make_data_path(
        file_name: str
):
    file_name = os.path.basename(file_name).replace(".py", "")
    path = "data%s%s" % (path_separator, file_name)
    if os.path.exists(path) is True:
        pass
    else:
        make_path("data")
        os.mkdir(path)
    return path


def project_path(
        project_name
):
    # 获取项目的根目录，需要输入项目名称
    cur_path = os.path.abspath(os.path.dirname(__file__))
    _project_path = cur_path[:cur_path.find("%s%s" % (project_name, path_separator)) + len("%s%s" % (project_name, path_separator))]
    return _project_path


def file_path():
    """
    os.path.dirname(os.path.abspath(__file__))  单纯的文件地址
    os.path.dirname(os.path.realpath(__file__))  可能会存在的文件指向的真实地址
    """
    return os.path.dirname(os.path.abspath(__file__))


def get_all_top_dir():
    """
    枚举当前文件所处的文件夹的所有明细路径
    """
    file_dir = sys.argv[0]
    dir_list = file_dir.split(path_separator)
    dir_list_length = len(dir_list)
    new_dir_list = list()
    for i in range(dir_list_length):
        dir_list.pop(dir_list_length - i - 1)
        if len(dir_list) > 0:
            temp_dir = path_separator.join(dir_list)
            if len(temp_dir) > 0:
                new_dir_list.append(temp_dir)
            else:
                continue
        else:
            continue
    return new_dir_list


def visit_dir(
        path
):
    total_size = 0
    file_num = 0
    dir_num = 0
    for lists in os.listdir(path):
        sub_path = os.path.join(path, lists)
        # print(sub_path)
        if os.path.isfile(sub_path):
            file_num = file_num+1
            # print(fileNum)# 统计文件数量
            total_size = total_size+os.path.getsize(sub_path)  # 文件总大小
        elif os.path.isdir(sub_path):
            dir_num = dir_num+1  # 统计文件夹数量
            visit_dir(sub_path)  # 递归遍历子文件夹
    return file_num


def file_list(
        file_dir=os.path.dirname(os.path.realpath(__file__))
):
    return os.listdir(file_dir)
