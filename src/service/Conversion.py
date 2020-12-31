from model.domain.netdisk import *

def NetPathToDomain(webPath):
    return NetDiskPath(
        name=webPath['server_filename'],
        path=webPath['path'],
        fileId=webPath['fs_id'],
        size=webPath['size'],
        isDir=webPath['isdir']
    )

def LocalPathToDomain(path,isdir):
    return LocalDiskPath(
        name=path,
        path=path,
        isdir=isdir
    )
    