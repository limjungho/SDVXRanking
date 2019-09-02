from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import sqlite3
from time import sleep

class SDVXTrack:
    def __init__(self):
        self.TrackID = 0
        self.TrackTitle = ''
        self.TrackDifficulty = []

    def set(self, id, title, diff, lev, score, grade, comp):
        self.TrackID = id
        self.TrackTitle = title
        self.TrackDifficulty.append((diff,lev,score,grade, comp))
    def setDiff(self,diff,lev,score,grade, comp):
        self.TrackDifficulty.append((diff, lev,score,grade,comp))
    def setID(self, id):
        self.TrackID = id

def DecideDiff(tracks):
    TrackLevel = tracks.find('div', attrs={'class': 'lv mxm'})
    if TrackLevel is not None:
        return 'MXM',TrackLevel.text
    TrackLevel = tracks.find('div', attrs={'class': 'lv gra'})
    if TrackLevel is not None:
        return 'GRV',TrackLevel.text
    TrackLevel = tracks.find('div', attrs={'class': 'lv vvd'})
    if TrackLevel is not None:
        return 'VVD',TrackLevel.text
    TrackLevel = tracks.find('div', attrs={'class': 'lv hvn'})
    if TrackLevel is not None:
        return 'HVN',TrackLevel.text
    TrackLevel = tracks.find('div', attrs={'class': 'lv inf'})
    if TrackLevel is not None:
        return 'INF',TrackLevel.text
    TrackLevel = tracks.find('div', attrs={'class': 'lv exh'})
    if TrackLevel is not None:
        return 'EXH',TrackLevel.text
    TrackLevel = tracks.find('div', attrs={'class': 'lv adv'})
    if TrackLevel is not None:
        return 'ADV',TrackLevel.text
    TrackLevel = tracks.find('div', attrs={'class': 'lv nov'})
    if TrackLevel is not None:
        return 'NOV',TrackLevel.text

def DecideComp(tracks):
    TrackComp = tracks.find('div', attrs={'class': 'cp play'})
    if TrackComp is not None:
        return 'PLAY'
    TrackComp = tracks.find('div', attrs={'class': 'cp comp'})
    if TrackComp is not None:
        return 'COMP'
    TrackComp = tracks.find('div', attrs={'class': 'cp comp_ex'})
    if TrackComp is not None:
        return 'COMP_EX'
    TrackComp = tracks.find('div', attrs={'class': 'cp uc'})
    if TrackComp is not None:
        return 'UC'
    TrackComp = tracks.find('div', attrs={'class': 'cp puc'})
    if TrackComp is not None:
        return 'PUC'
    return None

def findName():
    req = Request('http://anzuinfo.me/profile.html?search_id=' + AnzuID)
    res2 = urlopen(req)
    html2 = res2.read().decode('utf8')
    print(html2)
    bs2 = BeautifulSoup(html2, 'html.parser')
    profile = bs2.findAll('table', attrs={'class': 'profile'})
    print(profile)
    profileList = profile[0].findAll('td')
    print(profileList)


def CreateData(UserNum):
    SDVXNick = input('SDVX Nickname : ')
    sql = "insert into UserInfo(UserNumber, UserID, UserName) VALUES ("+UserNum+", '"+AnzuID+"', '"+SDVXNick+"');"
    cur.execute(sql)


def UpdateData(UserNum, UserName):
    ScoreID = ''

    for id in TrackIdDict:
        for dff in TrackIdDict[id].TrackDifficulty:
            ScoreID = str(UserNum)+str(id)+dff[0]
            sql = 'select ScoreID from ScoreData where ScoreID = ?;'
            cur.execute(sql,(ScoreID,))
            checksid = cur.fetchone()
            if checksid is not None:
                sql = "update ScoreData SET Score = ?, Grade = ?, Complete = ?;"
                cur.execute(sql, (str(dff[2]), dff[3], dff[4]))
            else:
                sql = "insert into ScoreData VALUES (?, ?, ?, ?, ?, ?, ?);"
                cur.execute(sql,(str(ScoreID), UserNum,id,dff[0],str(dff[2]),dff[3],dff[4]))
    conn.commit()


conn = sqlite3.connect("SDVXRanking.db")
cur = conn.cursor()

PrintImgSize = '50'

sql = 'select TrackID from TrackList;'
cur.execute(sql)
rows = cur.fetchall()
TrackSize = len(rows)

sql = 'select UserID from UserInfo;'
cur.execute(sql)
Usertuple = cur.fetchall()
UserList = []
for user in Usertuple:
    UserList.append(user[0])
#AnzuID = input('anzuinfo id : ')

for AnzuID in UserList:
    print(AnzuID)
    TrackDict = {}
    prevhtml = ''
    #TrackList = []

    for i in range(1,100):
        req = Request('http://anzuinfo.me/myScore.html?search_id='+AnzuID+'&sort=update_up&page='+str(i))
        res = urlopen(req)
        html = res.read().decode('utf8')
        if prevhtml == html:
            break
        prevhtml = html
        print('Loading...'+str(i))

        bs = BeautifulSoup(html, 'html.parser')
        TrackData = bs.findAll('table', attrs={'class': 'track'})

        for tracks in TrackData:
            TrackDifficulty, TrackLevel = DecideDiff(tracks)
            TrackTitle = tracks.find('div', attrs={'class': 'title'}).text
            TrackScore = tracks.find('div', attrs={'class': 'score'}).text
            TrackGrade = tracks.find('div', attrs={'class': 'grade'}).text
            TrackComp = DecideComp(tracks)
            sql = "select TrackID from TrackList where TrackTitle = ?;"
            cur.execute(sql,(TrackTitle,))
            TrackID = str(cur.fetchone()[0])

            if TrackTitle in TrackDict:
                TrackDict[TrackTitle].setDiff(TrackDifficulty, TrackLevel,TrackScore,TrackGrade,TrackComp)
            else:
                newTrack = SDVXTrack()
                newTrack.set(TrackID, TrackTitle, TrackDifficulty, TrackLevel,TrackScore,TrackGrade,TrackComp)
                TrackDict[TrackTitle] = newTrack
        sleep(0.01)

    TrackIdDict = dict((value.TrackID, value) for key, value in TrackDict.items())

    sql = 'select UserNumber, UserName from UserInfo where UserID = "'+AnzuID+'";'
    cur.execute(sql)
    Userinfo = cur.fetchone()
    if Userinfo is not None:
        UpdateData(str(Userinfo[0]), str(Userinfo[1]))
    else:
        sql = 'select UserNumber from UserInfo;'
        cur.execute(sql)
        rows = cur.fetchall()
        NewID = len(rows)+1
        CreateData(str(NewID))
        sql = 'select UserNumber, UserName from UserInfo where UserID = "' + AnzuID + '";'
        cur.execute(sql)
        Userinfo = cur.fetchone()
        UpdateData(str(Userinfo[0]), str(Userinfo[1]))

conn.close()