import requests
from flask import request
from db.get_sql import select, update


def search_shopping(token) -> list:
    sql = "select shopping from user_info where cookie = '{}'".format(token)
    result = select(sql, 1)[0]
    if result == '':
        return []
    else:
        return eval(result)


def get_shopping(token, new_list: list):
    sql = "select count(shopping) from user_info where cookie = '{}'".format(token)
    if select(sql, 1)[0] == 1:
        sql = "select shopping from user_info where cookie = '{}'".format(token)
        result = select(sql, 1)[0]
        new_list_ = []
        for i in new_list:
            new_list_.append(int(i))
        list_1 = list(new_list_) + eval(result)
        list_without_duplicates = list(set(list_1))
        sql = update(f"update user_info set shopping = '{list(list_without_duplicates)}' where cookie = '{token}'")
        update(sql)
    else:
        new_list_ = []
        for i in new_list:
            new_list_.append(int(i))
        update(f"update user_info set shopping = '{str(new_list_)}' where cookie = '{token}'")
    return 'ok'


def delete_shopping(token, new_list: list):
    list_ = search_shopping(token)
    for item in new_list:
        list_ = list_.remove(item)
    sql = update(f"update user_info set shopping = '{list_}' where cookie = '{token}'")
    update(sql)


def clear_shopping(token):
    update(f"UPDATE user_info SET shopping = '[]' where cookie = '{token}'")


def get_shopping_list():
    data = request.get_json()
    list_ = []
    for i in data:
        list_.append(get_info(i))
    return list_


def get_info(product_id):
    url = "https://m.mi.com/mtop/xiaomishop/product/info"

    headers = {
        'user-agent': "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/119.0.0.0 Mobile Safari/537.36",
        "Origin": 'https://m.mi.com',
        "referer": f"https://m.mi.com/commodity/detail/{product_id}"
    }

    data = [{}, {"productId": product_id}]
    print(data)

    res = requests.post(url, json=data, headers=headers).json()

    return res

# print(get_info(19436))
