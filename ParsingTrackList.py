from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import sqlite3
from time import sleep

imgchrList = ['n','a','e','m','i','g','h','v']
DiffList = ['nov','adv','exh','mxm','inf','grv','hvn','vvd']

conn = sqlite3.connect("SDVXRanking.db")
cur = conn.cursor()

for tid in range(164,1412):
    print('Loading...' + str(tid))
    sql = "insert into TrackList (TrackID) VALUES (?);"
    cur.execute(sql,(str(tid+1000),))
    for i in range(0,8):
        req = Request('http://anzuinfo.me/trackData.html?trackID='+str(tid).zfill(4)+imgchrList[i])
        res = urlopen(req)
        html = res.read().decode('utf8')

        bs = BeautifulSoup(html, 'html.parser')
        TrackData = bs.findAll('table', attrs={'class': 'trackData'})

        for tracks in TrackData:
            findlv = 'lv '+DiffList[i]
            TrackLevel = tracks.find('div', attrs={'class': findlv})
            if TrackLevel is None:
                continue
            TrackLevel = TrackLevel.text
            TrackDifficulty = DiffList[i].upper()
            TrackTitle = tracks.find('td', attrs={'class': 'title'}).text
            sql = "update TrackList SET TrackTitle = :Title, "+TrackDifficulty+" = :Lv where TrackID = :ID;"
            cur.execute(sql,{'Title': TrackTitle, 'Lv': TrackLevel, 'ID':str(tid+1000)})
    conn.commit()
    sleep(0.02)

conn.close()