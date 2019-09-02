import sqlite3

# SQLite DB 연결
conn = sqlite3.connect("SDVXRanking.db")

# Connection 으로부터 Cursor 생성
with conn:
    cur = conn.cursor()

    # SQL 쿼리 실행
    sql = "insert into TrackList(TrackID, TrackTitle) VALUES (1057, 'ヘヴン （かめりあs NEKOMATAelectroRMX）')"
    # sql = "select * from TrackList"
    cur.execute(sql)
    conn.commit()

    '''
    # 데이타 Fetch
    rows = cur.fetchall()
    for row in rows:
        print(row)
    '''

# Connection 닫기
conn.close()