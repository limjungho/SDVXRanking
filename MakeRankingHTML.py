import sqlite3
from time import sleep

def CreateHTML(path, trcID, nowdiff):
    imgchrList = ['n','a','e','m','i','g','h','v']
    imgchr = imgchrList[nowdiff]

    sql = "select TrackTitle from TrackList where TrackID ='"+str(trcID)+"';"
    cur.execute(sql)
    TrackTitle = str(cur.fetchone()[0])

    htmlhead = open('SDVXTrackRankingHEAD.html','r').read()
    htmlbody=''
    htmlbody += '<div align="center"><img src="http://anzuinfo.me/images/track_img/'+str(trcID-1000).zfill(4)+imgchr+'.jpg" width="300" height="300"><div>\n'
    htmlbody += '<div align="center"><h1>'+TrackTitle+' '+DiffList[nowdiff]+'</h1></div>'
    htmlbody += '<table border="1" width=960px align="center">\n'
    htmlbody += '<th>Rank</th>'
    htmlbody += '<th>ID</th>'
    htmlbody += '<th>Score</th>'
    htmlbody += '<th>Grade</th>'
    htmlbody += '<th>Complete</th>'

    sql = "select UserNumber, Score, Grade, Complete from ScoreData where TrackID = ? and Difficulty = ?;"
    cur.execute(sql,(trcID,DiffList[nowdiff]))
    RankList = cur.fetchall()
    #print(RankList)
    sortedRankList = sorted(RankList, key=lambda x: x[1], reverse=True)
    for rank, data in enumerate(sortedRankList):
        sql = "select UserName from UserInfo where UserNumber = ?;"
        cur.execute(sql, (data[0],))
        UserName = cur.fetchone()[0]
        htmlbody += '<tr><td align="center">'+str(rank+1)+'</td><td align="center">'+UserName+'</td>'
        htmlbody += '<td align="center">'+str(data[1])+'</td><td align="center">'+data[2]+'</td><td align="center">'+data[3]+'</td></tr>\n'
    htmltail = open('SDVXTrackRankingTAIL.html','r').read()

    file = open(path+'/'+str(trcID)+'_'+DiffList[nowdiff]+'.html','w',encoding='utf8')
    file.write(htmlhead)
    file.write(htmlbody)
    file.write(htmltail)
    file.close()

conn = sqlite3.connect("SDVXRanking.db")
cur = conn.cursor()
DiffList = ['NOV','ADV','EXH','MXM','INF','GRV','HVN','VVD']

sql = "select * from TrackList;"
cur.execute(sql)
rows = cur.fetchall()
for row in rows:
    for i in range(2,10):
        if row[i] is not None:
            CreateHTML('RankingHTML', row[0], i-2)
    #print('Loading...' + str(tid))
    print("Loading.."+str(row[0]))

conn.close()