import sqlite3
from time import sleep

file2 = open('SDVXTrackListHEAD.html','r')
HTMLcomp = file2.read()
file2.close()

conn = sqlite3.connect("SDVXRanking.db")
cur = conn.cursor()
sql = "select * from TrackList"
cur.execute(sql)
rows = cur.fetchall()
HTMLbody = ''
PrintImgSize = '80'
for row in rows:
    print(row)
    Bodytemp = '<tr><td>'+str(row[0])+'</td><td>'+row[1]+'</td>'
    LvList = []
    DiffList = ['NOV','ADV','EXH','MXM','INF','GRV','HVN','VVD']
    for i in range(2,10):
        LvList.append(row[i])
    #print(LvList)

    nowID = row[0]
    '''
    Bodytemp += '<td><img src="http://anzuinfo.me/images/track_img/'+str(nowID-1000).zfill(4)+'n.jpg" width="'+PrintImgSize+'" height="'+PrintImgSize+'"><br/><a href="RankNOV/'+str(nowID)+'.html" target="_blank">'+NOVlv+'</td>'
    Bodytemp += '<td><img src="http://anzuinfo.me/images/track_img/'+str(nowID-1000).zfill(4)+'a.jpg" width="'+PrintImgSize+'" height="'+PrintImgSize+'"><br/><a href="RankADV/'+str(nowID)+'.html" target="_blank">' + ADVlv + '</td>'
    Bodytemp += '<td><img src="http://anzuinfo.me/images/track_img/'+str(nowID-1000).zfill(4)+'e.jpg" width="'+PrintImgSize+'" height="'+PrintImgSize+'"><br/><a href="RankEXH/'+str(nowID)+'.html" target="_blank">' + EXHlv + '</td>'
    Bodytemp += '<td><a href="RankELSE/'+str(nowID)+'.html" target="_blank">' + elsLv + '</td>'
    '''
    for i in range(0,8):
        if LvList[i] is None:
            Bodytemp += '<td>-</td>'
        else:
            Bodytemp += '<td><a href="RankingHTML/' + str(nowID) + '_'+DiffList[i]+'.html" target="_blank">' + LvList[i] + '</td>'
    Bodytemp += '</tr>\n'
    HTMLbody += Bodytemp

HTMLcomp += HTMLbody

file2 = open('SDVXTrackListTAIL.html','r')
HTMLcomp = HTMLcomp + file2.read()
file2.close()
file = open('SDVXTrackList.html','w',encoding='utf8')
file.write(HTMLcomp)
file.close()


'''
def CreateHTML(path, trcID, nowdiff):
    htmlhead = open('SDVXTrackRankingHEAD.html','r').read()
    htmlbody=''
    htmlbody += '<div align="center"><img src="http://anzuinfo.me/images/track_img/'+str(trcID-1000).zfill(4)+imgchr+'.jpg" width="300" height="300"><div>\n'
    htmlbody += '<div align="center"><h1>'+TrackIdDict[trcID].TrackTitle+' '+nowdiff+'</h1></div>'
    htmlbody += '<table border="1" width=1080px align="center">\n'
    htmlbody += '<th>Rank</th>'
    htmlbody += '<th>ID</th>'
    htmlbody += '<th>Score</th>'
    htmlbody += '<tr><td align="center">'+'1'+'</td><td align="center">'+'WF.HOWLS'+'</td><td align="center">'+'10000000'+'</td></tr>'
    htmltail = open('SDVXTrackRankingTAIL.html','r').read()

    file = open(path+'/'+str(trcID)+'.html','w',encoding='utf8')
    file.write(htmlhead)
    file.write(htmlbody)
    file.write(htmltail)
    file.close()

CreateHTML('RankingHTML')
'''

# print(html)


conn.close()