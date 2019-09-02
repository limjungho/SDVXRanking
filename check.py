from urllib.request import Request, urlopen
from time import sleep

for i in range(1406,1415):
    if(i%10 == 0):
        print(i)
    num = str(i).zfill(4)
    #print(num)
    req = Request('http://anzuinfo.me/images/track_img/'+num+'n.jpg')
    res = urlopen(req)
    jpgdata = res.read()
    if not(jpgdata[0] == 0xff and jpgdata[1]==0xd8):
        print('--------------------------------------')
        print(num)
        print('--------------------------------------')
    sleep(0.1)
