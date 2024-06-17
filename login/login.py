import time

from flask import request
from db.get_sql import select, update
import random
import string


def generate_random_string(length):
    # 生成包含数字、字母、符号的字符串集合
    chars = string.ascii_letters + string.digits

    # 生成指定长度的随机字符串
    random_string = ''.join(random.choice(chars) for _ in range(length))

    return random_string


def user_sign_in(username, password, college, age, content_url, date, email, desc, course, gender):
    if request.is_json:
        if password != '' and username != '':
            user_id = random.randint(10000, 99999999999)
            sql = f"select count(user_id) from user_info where user_id = '{user_id}'"
            while select(sql, 1)[0] == 1:
                user_id = random.randint(10000, 99999999999)
            sql = (f"insert into user_info(nickname, user_id, user_pwd, age, collage, course, email, gender, desc) "
                   f"VALUES "
                   f"('{username}', '{user_id}', '{password}','{age}',"
                   f"'{college}','{course[0]}','{email}','{gender}','{desc}')")
            # update(sql)
            # return {'code': 0, 'user_id': user_id}
            try:
                update(sql)
                return {'code': 0, 'user_id': user_id}
            except Exception as e:
                return {'code': 2, 'msg': f'{e}'}
        else:
            return {'code': 1}
    else:
        return {'code': -1}


def user_login():
    if request.is_json:
        data = request.get_json()
        user_id = data['account']
        user_pwd = data['password']
        sql = f"select count(*) from user_info where user_id = '{user_id}' and user_pwd = '{user_pwd}'"
        if select(sql, 1)[0] == 1:
            cookie = generate_random_string(36)
            sql = f"update user_info set cookie = '{cookie}' where user_id = '{user_id}'"
            update(sql)
            return {'code': 0, 'token': cookie}
        else:
            return {'code': 1}
    else:
        return {'code': -1}


def check_cookie():
    token = request.cookies.get('token')
    if token:
        sql = f"select end_time from user_info where cookie = '{token}'"
        if select(sql, 1)[0] > int(time.time()):
            return {'code': 0}
        else:
            return {'code': 1}
    else:
        return {'code': -1}
