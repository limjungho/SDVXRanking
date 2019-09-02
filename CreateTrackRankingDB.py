from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import sqlite3
from time import sleep

def CreateTrackRanking(tid, diff):
    sql = 'CREATE TABLE "' + str(tid) + '_' +diff +'" ('
    sql += '''
        "UserNumber" TEXT,
        "UserName" TEXT,
        "Score"	INTEGER,
        "Grade"	TEXT,
        "Complete"	TEXT
    );
    '''
    #print(sql)
    cur2.execute(sql)

conn = sqlite3.connect("SDVXRanking.db")
cur = conn.cursor()

conn2 = sqlite3.connect("SDVXTrackRanking.db")
cur2 = conn2.cursor()

sql = 'select TrackID from TrackList;'
cur.execute(sql)
rows = cur.fetchall()
TrackSize = len(rows)

for tid in range(1001,2406):
    CreateTrackRanking(tid, 'NOV')
    CreateTrackRanking(tid, 'ADV')
    CreateTrackRanking(tid, 'EXH')
    CreateTrackRanking(tid, 'ELSE')
    print(tid)
conn2.commit()

conn.close()
conn2.close()