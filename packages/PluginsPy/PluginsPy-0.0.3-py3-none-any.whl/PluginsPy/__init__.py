#!/usr/bin/env python3

import argparse
import importlib
import re
import sys
import inspect
from os import walk

def getFiles(path) :
    for (dirpath, dirnames, filenames) in walk(path) :
        dirpath = dirpath
        dirnames = dirnames
        filenames = filenames
        return filenames

    return []

def getPluginFiles(dirpath):
    return getFiles(dirpath)

def getClassMethods(clazz):
    methods = dict()
    for item in dir(clazz):
        if item.startswith("_"):
            continue

        method = getattr(clazz, item)
        methods[item] = [str(method.__doc__).strip()] 
    
    return methods

def addRun(clazz):

    @classmethod
    def run(clazz, kwargs):
        """
        使用装饰的方法给Plugin进行统一添加该方法，便于统一修改
        """

        print(">>> enter plugin run method")
        # print("cmd line args: " + str(kwargs))
        if len(inspect.signature(getattr(clazz, "__init__")).parameters) == 2: 
            obj = clazz(kwargs)
        else:
            obj = clazz()

        invert_op = getattr(obj, "start", None)
        if callable(invert_op):
            print(">>> enter plugin start method")
            if len(inspect.signature(invert_op).parameters) > 0:
                invert_op(kwargs)
            else:
                invert_op()
            print("<<< end plugin start method")
        print("<<< end plugin run method")

    # print(">>> start add plugin run method")
    setattr(clazz, 'run', run)
    # print(dir(clazz))
    # items = getClassMethods(clazz)
    # for item in items:
    #     if item == "run":
    #         print(item + ": " + items[item][0])
    # print("<<< end add plugin run method")

    return clazz

def PluginsPy(cmd, skipedPlugins=[], pluginsDir="Plugins") :

    parser = argparse.ArgumentParser(prog=cmd)
    subparsers = parser.add_subparsers(help='commands help')

    # tensorflow加载太慢，有需要的情况下通过-s参数判定加载
    argv = sys.argv[1:]
    skipOption = True
    if "-s" in argv and len(argv) >= 1 and argv[0] == "-s":
        if len(argv) == 1:
            argv = []
        elif len(argv) > 1:
            argv = argv[1:]

        skipOption = False

    # 处理插件
    for file in getPluginFiles(pluginsDir):
        if file == "__init__.py":
            continue

        # skip config: Plugins/__init__.py
        if skipOption:
            skipedPlugin = False
            for plugin in skipedPlugins:
                if file == plugin or file.split(".")[0] == plugin:
                    skipedPlugin = True
            if skipedPlugin:
                print("skiped pulgin: " + file)
                continue

        """
        1. 使用文件名获取模块名，
        2. 导入模块，
        3. 获取模块同名类，
        4. 获取类方法
        """
        moduleString = file.split(".")[0]
        print(moduleString)
        module = importlib.import_module(pluginsDir + "." + moduleString)
        clazz = getattr(module, moduleString)

        clazzDoc = clazz.__doc__
        # 从类注释中获取类说明，也就是帮助
        parser_item = subparsers.add_parser(moduleString, help = clazzDoc.split("@")[0].strip())

        # 从类注释中获取类参数及参数说明，格式@argument: argument doc
        keyValues = {}
        for arg in clazzDoc.split("\n"):
            keyValue = arg.strip().split(":")
            if len(keyValue) == 2 and keyValue[0].strip().startswith("@"):
                keyValues[keyValue[0].strip().replace("@", "")] = keyValue[1].strip()

        # 转换为命令行参数
        for arg in keyValues:
            matchObj = re.match(r'(\S*)\((\S*)\)', arg)
            if matchObj:
                # print("-----------matchObj-----------")
                # print(matchObj.group(1))
                # print(matchObj.group(2))
                # print("------------------------------")
                parser_item.add_argument('-' + matchObj.group(1), default=matchObj.group(2), help=keyValues[arg])
            else:
                parser_item.add_argument('-' + arg, help=keyValues[arg])

        # 获取当前处理方法并设置为该命令的回调函数
        method = getattr(clazz, "run")
        parser_item.set_defaults(func=method)

    #执行函数功能
    args = parser.parse_args(argv)
    if args :
        if len(args.__dict__) > 0:
            print(">>> start call Plugin run or CmdMaps method")
            args.func(args.__dict__)
            print("<<< end call Plugin run or CmdMaps method")
        else:
            parser.parse_args(["-h"])

if __name__ == "__main__" :
    pass
