#!/usr/bin/python
# _*_ coding:utf8 _*_
########################################
# OhMyLineNum
# Author: duian
# email: chenanze@live.com
########################################
import os
import pdb 
import sys
import linecache
import re
import time

path = '.'
dirList = []
dirStack = []
isOpenFilePrint = False
isShowFilePath = False
isShowEmptyFile = False
isWritePrintToFile = False
fileReadMode = 0

def stackTop(stack):
    return stack[len(stack) - 1]

def getPath(name):
    path + '/' + name

def getListSubPath(path):
    listFile = []
    listSubFile = os.listdir(path)
    for file in listSubFile:
        listFile.append(path + '/' +file)
    return listFile

def getDirList(pathList):
    dirPathList = []
    for file in pathList:
        if os.path.isdir(file):
            dirPathList.append(file)
    return dirPathList

def isAllFileInPath(path):
    listSubFile = os.listdir(path)
    for file in listSubFile:
        if os.path.isdir(path + '/' + file):
            return False
    return True

def isInList(str, list):
    for i in xrange(len(list)-1,-1,-1):
        if str == list[i]:
            return True
    return False

def isAllFileDirUsed(stackTop, dirList):
    isAllUsed = True
    listSubDir = getDirList(getListSubPath(stackTop))
    for fileDir in listSubDir:
        if not isInList(fileDir, dirList):
            isAllUsed = False
    return isAllUsed

def traverseFileSystemTree():
    if os.path.isdir(path):
        dirStack.append(path)

    while len(dirStack) != 0:
        if not isAllFileInPath(stackTop(dirStack)): # 存在文件夹
            if isAllFileDirUsed(stackTop(dirStack), dirList): # 文件夹全被使用
                # 将栈顶文件夹出栈 并放入dirList队列中
                dirList.append(dirStack.pop())         
            else: # 文件夹未全被使用   
                    # 获取栈顶路径下所有文件夹路径列表
                listSubDir = getDirList(getListSubPath(stackTop(dirStack)))
                # 遍历head文件夹下所有子文件夹路径 并判断是否已存在与dirList中
                for fileDir in listSubDir:
                    # 判断文件路径在dirList中是否已存在
                    if not isInList(fileDir, dirList): # 不存在
                        # 将子文件夹路径入栈
                        dirStack.append(fileDir)
                        break
        else: # 不存在文件夹
            # 将栈顶文件夹出栈 并放入dirList队列中
            dirList.append(dirStack.pop())
        # print '<======'
        # for dir in dirList:
        #     print 'dirList: '+ dir
        # for dir in dirStack:
        #     print 'dirStack: '+dir
        # print '======>'


def getLineNumerOfFile(path):
    if fileReadMode == 0:
        if os.path.exists(path):
            return len(open(path,'r').readlines())
        return 0
    if fileReadMode == 1:
            return len(linecache.getlines(path))

def getFileListFromDirPath(path):
    fileList = []
    listPath = os.listdir(path)
    for filePath in listPath:
        if os.path.isfile(path + '/' +filePath):
            # filePathList.append(path + '/' +filePath)
            fileList.append(filePath)
    return fileList

def getFileName():
    return 'print_'+str(time.time())+'.log'

def writePrintToFile(fileName, list):
    list = [line+'\n' for line in list]
    file_object = open(fileName, 'a')
    file_object.writelines(list)

def getPrintTmpStr(num, path, file, tmpLineNumber):
    global isShowFilePath
    if isShowFilePath:
        tmpStr =  'filePath:['+ str(num) +']' + path + '/' + file + ' lineNumber: '+ str(tmpLineNumber)
    else:
        tmpStr =  'fileName:['+ str(num) +']: '+ file +' lineNumber: '+ str(tmpLineNumber)
    return tmpStr

def computeLineNumberOfFileTree():
    lineNumber = 0
    num = 0
    tmpFileName = ''
    if isWritePrintToFile:
        tmpFileName = getFileName()
    for path in dirList:
        tmpFileList = []
        # print 'dirList item path: '+path
        for file in getFileListFromDirPath(path):
            tmpLineNumber = getLineNumerOfFile(path + '/'+ file)

            if isOpenFilePrint == True:
                if tmpLineNumber != 0 or isShowEmptyFile:
                    print getPrintTmpStr(num, path, file, tmpLineNumber)

            if isWritePrintToFile:
                 if tmpLineNumber != 0 or isShowEmptyFile:
                    tmpFileList.append(getPrintTmpStr(num, path, file, tmpLineNumber))

            lineNumber += tmpLineNumber
            num += 1
        if isWritePrintToFile:
                writePrintToFile(tmpFileName, tmpFileList)

    print 'All lineNumber: ' + str(lineNumber)

    if isWritePrintToFile:
        tmpFileList = []
        tmpFileList.append('All lineNumber: ' + str(lineNumber))
        writePrintToFile(tmpFileName, tmpFileList)

def showHelp():
    print '======================Help: ======================\
        \n     python filepath [n|N|f|F|p|P|e|E|s|S|l|L|w|W|-h|-H|--help]\
        \n          -h|-H: print this help doc\
        \n          n|N: only show all line number\
        \n          f|F: print file name \
        \n          p|P: print file path\
        \n          e|E: is print empty file\
        \n          s|S: print match to small size file\
        \n          l|L: print match to large size file\
        \n          w|W: write the print to log file'

def checkHelp():
    showHelp()
    sys.exit()

def checkArgv1():
    global path 
    if sys.argv[1] == '-h' or sys.argv[1] == '-H' or sys.argv[1] == '--help':
        checkHelp()
    else:
        path = sys.argv[1]

def checkArgv2():
    checkArgv1()
    global isOpenFilePrint
    global isShowFilePath
    global isShowEmptyFile
    global isWritePrintToFile
    global fileReadMode

    if re.search(r'[n|N]', sys.argv[2]):
        isOpenFilePrint = False
    if re.search(r'[f|F]', sys.argv[2]):
        isOpenFilePrint = True
    if re.search(r'[p|P]', sys.argv[2]):
        isOpenFilePrint = True
        isShowFilePath = True
    if re.search(r'[e|E]', sys.argv[2]):
        isOpenFilePrint = True
        if re.search(r'[p|P]', sys.argv[2]):
            isShowFilePath = True
        isShowEmptyFile = True
    if re.search(r'[s|S]', sys.argv[2]):
        fileReadMode = 0
    if re.search(r'[l|L]', sys.argv[2]):
        fileReadMode = 1
    if re.search(r'[w|W]', sys.argv[2]):
        isWritePrintToFile = True
    if re.search(r'[\-h|\-H]', sys.argv[2]):
        checkHelp()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        checkArgv1()
    elif len(sys.argv) == 3:
        checkArgv2()
    else:
        checkHelp()

    traverseFileSystemTree()
    computeLineNumberOfFileTree()

