import requests
import json
import math
from tqdm import tqdm

#YOUR_CLIENT_ID = 'ucigOowbGKEBcQmMjmsmGhsl'
#YOUR_REGISTERED_REDIRECT_URI = 'oob'
ACCESS_TOKEN = '121.55b755add7fbb0d3f9d2e39bf310d9c2.Y7QYIwODQiwm4OXCbu9bwOaQN-688selF3StEW-.vbFydw'
DEFALT_HEADER = {
        'User-agent':'pan.baidu.com',
        'cache-control':'no-cache'}  

def query(url,params={},headers=DEFALT_HEADER):
    return requests.get(url=url,headers=headers,params=params)

def verify(url,params={},headers=DEFALT_HEADER,data = {}):
    return requests.post(url=url,headers=headers,params=params,data=data)

def targetUrl(target):
    return 'https://pan.baidu.com/rest/2.0/xpan/%s' % (target)

class WebService():
    @staticmethod
    def GetFileList(dir=''):
        url = targetUrl('file')
        params = {
            'method':'list',
            'access_token':ACCESS_TOKEN,
            'dir':dir
        }
        headers = {
            'User-agent':'pan.baidu.com'
        }
        response = requests.get(url=url,params=params,headers=headers)
        domain = json.loads(response.content)
        return domain['list']

    @staticmethod
    def GetFileDlink(targetFile):
        url = targetUrl("multimedia")
        params = {
            'method':'filemetas',
            'access_token':ACCESS_TOKEN,
            'fsids':'[%s]'% targetFile.FileId,
            'dlink':1
        }
        headers = {
            'User-agent':'pan.baidu.com'
            }
        response = requests.get(url=url,params=params,headers=headers)
        domain = json.loads(response.content)
        return domain['list'][0]['dlink']

    @staticmethod
    def DownloadFile(targetFile,localPath):
        url = targetFile.Dlink
        params = {
            'access_token':ACCESS_TOKEN
        }
        headers = {
            'User-agent':'pan.baidu.com'
            }
        response = requests.get(url=url,params=params,headers=headers,stream=True)
        totalLength = targetFile.Size

        with open(localPath, 'wb') as fs:
            #for chunk in progress.bar(response.iter_content(chunk_size=1024), expected_size=(totalLength/1024) + 1, width=100):
            for chunk in tqdm(response.iter_content(chunk_size=1024),total=math.ceil(totalLength/1024),unit='kb',desc=targetFile.Name,mininterval=5):
                if chunk:
                    fs.write(chunk)