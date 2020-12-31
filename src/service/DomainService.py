import os
import os.path
import datetime
from model.domain.netdisk import *
from service.Conversion import *
from service.WebService import WebService

class Helper():
    @staticmethod
    def MakeNetDisk(basePath):
        return NetDiskPath(name=basePath,path=basePath)

    @staticmethod
    def MakeLocalDisk(basePath):
        return LocalDiskPath(name=basePath,path=basePath)

    @staticmethod
    def CurrentDatetime():
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class DomainService():
    def __init__(self,baseLocalPath,targetPath):
        if (not os.path.exists(baseLocalPath)): os.mkdir(baseLocalPath)
        self._targetPath = targetPath
        self._baseLocalPath = baseLocalPath
        self._netDisk = NetDiskPath()

    def UpdateNetPathToLocal(self,path):
        webPath = WebService.GetFileList(path.Path)
        domainPaths = [NetPathToDomain(p) for p in webPath]
        path.SubPaths.extend(domainPaths)
        for subPath in path.SubPaths:
            if subPath.IsDir:
                self.UpdateNetPathToLocal(subPath)

    def SyncFile(self,netFile,targetPath):
        if (not netFile.Dlink):
            netFile.Dlink = WebService.GetFileDlink(netFile)
        WebService.DownloadFile(netFile,targetPath)

    def SyncPath(self,netPath,count=0):
        targetPath = self._baseLocalPath + netPath.Path
        firstUpdate = True
        if not os.path.exists(targetPath):
            os.mkdir(targetPath)
        for subPath in netPath.SubPaths:
            if subPath.IsDir:
                count = self.SyncPath(subPath,count)
            else:
                targetFile = self._baseLocalPath + subPath.Path
                if (not os.path.exists(targetFile) or os.path.getsize(targetFile) != subPath.Size) :
                    if firstUpdate:
                        print('%s::Updating directory - %s' % (Helper.CurrentDatetime(),netPath.Path))
                        firstUpdate = False
                    self.SyncFile(subPath,targetFile)   
                    count += 1
        return count

    def Sync(self):
        self._netDisk = Helper.MakeNetDisk(self._targetPath)
        self.UpdateNetPathToLocal(self._netDisk)
        updatedCount = self.SyncPath(self._netDisk,0)
        if updatedCount:
            print('%s::Totally update %s files' % (Helper.CurrentDatetime(),updatedCount))
            print('%s::Keep updating...' % Helper.CurrentDatetime())

