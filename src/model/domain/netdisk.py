class DiskPath():
    def __init__(self, name, path, size, isDir):
        self.SubPaths = []
        self.Name = name        
        self.Path = path
        self.Size = size
        self.IsDir = isDir

class LocalDiskPath(DiskPath):
    def __init__(self, name='',path='',size=0,isDir=True):
        super().__init__(name,path,size,isDir)

class NetDiskPath(DiskPath):
    def __init__(self, name='',path='',size=0,isDir=True,fileId="",dlink=""):
        super().__init__(name,path,size,isDir)
        self.FileId = fileId
        self.Dlink = dlink
