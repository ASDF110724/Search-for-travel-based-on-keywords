import pymysql
import pandas as pd


def load_csv(filename):

    file_path = f"{filename}.csv"
    csv_data = pd.read_csv(file_path, mode="w", newline="", encoding="utf-8")
    csv_data.drop_deplicate(inplace=True)

    return csv_data


def input_place(csv_data):

    conn = pymysql.connect(
        host="192.168.0.103",
        user="user1",
        password="u1234",
        db="sql_testdb",
        charset="utf8",
    )

    cur = conn.cursor()

    query = "INSERT INTO places (contentid,place_name,addr1,addr2,mapx,mapy) VALUES(%s,%s,%s,%s,%s,%s)"

    for index, row in csv_data.iterrows():
        cur.execute(
            query,
            (
                row["contentid"],
                row["title"],
                row["addr1"],
                row["addr2"],
                row["mapx"],
                row["mapy"],
            ),
        )

    conn.commit()
    conn.close()
