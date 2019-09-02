from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import sqlite3

# 1. 조회
def ex1():
    # 위의 html 문자열에 대해서, html 파싱하겠다.
    bs = BeautifulSoup(html, 'html.parser')
    print(bs, type(bs))
    # <td id="td1" class="title"><div class="tit3"><a href="/movie/bi/mi/basic.nhn?code=161242" title="범죄도시">범죄도시</a></div></td> <class 'bs4.BeautifulSoup'>

    # a 태그 출력
    tag = bs.a
    print(tag, type(tag))
    # <a href="/movie/bi/mi/basic.nhn?code=161242" title="범죄도시">범죄도시</a> <class 'bs4.element.Tag'>


# 2. Attribute 값 받아오기
def ex2():
    bs = BeautifulSoup(html, 'html.parser')

    tag = bs.td
    print(tag['class'])  # ['title']     => 리스트
    print(tag['id'])  # td1
    print(tag.attrs)  # {'id': 'td1', 'class': ['title']}   => 딕셔너리

    tag = bs.div
    print(tag['id'])  # id가 없으므로 error


# 3. Attribute 검색
def ex3():
    bs = BeautifulSoup(html, 'html.parser')

    # div 태그 중, class가 tit3인 태그를 찾는다.
    tag = bs.find('div', attrs={'class': 'tit3'})
    print(tag)  # <div class="tit3"> <a href="/movie/bi/mi/basic.nhn?code=161242" title="범죄도시">범죄도시</a> </div>

    tag = bs.find('div')
    print(tag)  # <div class="tit3"> <a href="/movie/bi/mi/basic.nhn?code=161242" title="범죄도시">범죄도시</a> </div>

    # 없는 태그를 조회할 경우
    tag = bs.find('td', attrs={'class': 'not_exist'})
    print(tag)  # None

    # 전체 태그에 대해 title이 범죄도시인 태그를 찾는다.
    tag = bs.find(attrs={'title': '범죄도시'})
    print(tag)  # <a href="/movie/bi/mi/basic.nhn?code=161242" title="범죄도시">범죄도시</a>


# 4. select(), content() 메서드
def ex4():
    bs = BeautifulSoup(html, 'html.parser')

    # CSS 처럼 셀렉터를 지정할 수 있다.
    tag = bs.select("td div a")[0]
    print(tag)  # <a href="/movie/bi/mi/basic.nhn?code=161242" title="범죄도시">범죄도시</a>

    text = tag.contents[0]
    print(text)  # 범죄도시


# 5. extract() 메서드
def ex5():
    bs = BeautifulSoup(html, 'html.parser')
    tag = bs.select("td")[0]
    print(
        tag)  # <td class="title" id="td1"> <div class="tit3"> <a href="/movie/bi/mi/basic.nhn?code=161242" title="범죄도시">범죄도시</a> </div></td>

    # div요소를 제거
    div_elements = tag.find_all("div")
    for div in div_elements:
        div.extract()

    print(tag)  # <td class="title" id="td1"> </td>

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


class SDVXTrack:
    def __init__(self):
        self.TrackID = 0
        self.TrackTitle = ''
        self.TrackDifficulty = []

    def set(self, id, title, diff, lev):
        self.TrackID = id
        self.TrackTitle = title
        self.TrackDifficulty.append((diff,lev))
    def setDiff(self,diff,lev):
        self.TrackDifficulty.append((diff, lev))
    def setID(self, id):
        self.TrackID = id


ID = ['howlingsoul']
TrackDict = {}
prevhtml = ''
#TrackList = []
setTrackID = 1001

for i in range(1,100):
    req = Request('http://anzuinfo.me/myScore.html?search_id='+ID[0]+'&sort=update_up&page='+str(i))
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
        if TrackTitle in TrackDict:
            TrackDict[TrackTitle].setDiff(TrackDifficulty, TrackLevel)
        else:
            newTrack = SDVXTrack()
            newTrack.set(setTrackID, TrackTitle, TrackDifficulty, TrackLevel)
            TrackDict[TrackTitle] = newTrack
            setTrackID += 1
            if setTrackID == 2087 or setTrackID ==2259:
                setTrackID += 1

TrackIdDict = dict((value.TrackID, value) for key, value in TrackDict.items())

# SQLite DB 연결
conn = sqlite3.connect("SDVXRanking.db")
with conn:
    cur = conn.cursor()
    for id in TrackIdDict:
        #print(id, TrackIdDict[id].TrackTitle)
        sql = "insert into TrackList(TrackID, TrackTitle) VALUES (:Id, :title);"
        cur.execute(sql,{"Id":id, "title":TrackIdDict[id].TrackTitle})

        for dff in TrackIdDict[id].TrackDifficulty:
            sql = "update TrackList SET "+dff[0]+" = "+dff[1]+" where TrackID=:Id;"
            #print(dff[0], dff[1])
            cur.execute(sql,{"Id":id})

    sql = "insert into TrackList(TrackID, TrackTitle) VALUES (2087, 'cobalt');"
    cur.execute(sql)
    sql = "update TrackList SET MXM ='17' where TrackID=2087;"
    cur.execute(sql)
    sql = "insert into TrackList(TrackID, TrackTitle) VALUES (2259, 'MODEL FT4');"
    cur.execute(sql)
    sql = "update TrackList SET MXM ='18' where TrackID=2259;"
    cur.execute(sql)

    conn.commit()
    # 데이타 Fetch
    '''
    rows = cur.fetchall()
    for row in rows:
        print(row)
    '''


