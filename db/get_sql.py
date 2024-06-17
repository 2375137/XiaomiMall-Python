import sqlite3


def select(sql: str, number: int):
    sql = str(sql)
    conn = sqlite3.connect('./db/data.db')
    cursor = conn.cursor()
    try:
        if number == 0:
            response = cursor.execute(sql).fetchall()
        else:
            response = cursor.execute(sql).fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return response
    except Exception as e:
        print(e)
        conn.commit()
        cursor.close()
        conn.close()
        return []


def update(sql: str):
    if sql is None:
        return None
    conn = sqlite3.connect('./db/data.db')
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(e)
        conn.commit()
        cursor.close()
        conn.close()
