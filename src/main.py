from service.WebService import WebService
from service.DomainService import *
import time

print('%s::Keep syncing...' % Helper.CurrentDatetime())
service = DomainService('data','/test')
while(1):
    try:
        service.Sync()
    except:
        print("Sync failed!")
    time.sleep(5)
print('Bye~')