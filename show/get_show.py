# from typing import Tuple, Dict, Any, List
import json
import requests


def read_scan_data():
    with open("./show/show.json", 'rt', encoding='utf-8') as f:
        content = f.read()
        f.close()
    return content


def get_picture():
    with open("./show/navbar.json", 'rt', encoding='utf-8') as f:
        content = f.read()
        f.close()
    return content


def _read_scan_data(_name=''):
    with open(_name, 'rt', encoding='utf-8') as f:
        content = f.read()
        f.close()
    return content


def get_shop(cat_id, _type=0):
    # print(json.loads(read_scan_data())[str(cat_id)])
    if _type == 0:
        return json.loads(read_scan_data())[str(cat_id)]
    else:
        return json.loads(get_picture())


def get_buyer_show_list(product_id, page_index, page_size, session_id):
    url = "https://m.mi.com/v1/communicate/mizone_buyer_show_list"
    data = {
        "client_id": "180100031058",
        "channel_id": "",
        "webp": "1",
        "commodity_id": product_id,
        "page_size": page_size,
        "page_index": page_index,
        "need_detail": "true",
        "orderby": "best",
        "showimg": "1",
        "profile_id": "",
        "session_id": session_id
    }
    if page_index != 0:
        data["need_detail"] = "false"

    headers = {
        # "content-type": "application/x-www-form-urlencoded",
        "Origin": "https://m.mi.com",
        "Referer": f"https://m.mi.com/micircle?product_id={product_id}&from=buy",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, "
                      "like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
    }

    return requests.post(url, data=data, headers=headers).text


# print(get_buyer_show_list(19019, 1, 10))


def get_all_product(title_search_id):
    url = "https://m.mi.com/v1/product/all_product"

    data = {
        "client_id": "180100031051",
        "channel_id": "",
        "webp": "1",
        "cat_id": f"{title_search_id}"
    }

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/119.0.0.0 Safari/537.36",
        "Origin": 'https://m.mi.com',
        "referer": "https://m.mi.com/category",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    res = requests.post(url, data=data, headers=headers).json()
    return res['data']['product']


def get_info(product_id):
    url = "https://m.mi.com/mtop/xiaomishop/product/info"

    headers = {
        'user-agent': "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/119.0.0.0 Mobile Safari/537.36",
        "Origin": 'https://m.mi.com',
        "referer": "https://m.mi.com/commodity/detail/19288"
    }

    data = [{}, {"productId": product_id}]

    res = requests.post(url, json=data, headers=headers).json()

    return res


def _get_shop(cat_id, show=0):
    url = "https://m.mi.com/v1/home/category_v2"

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/119.0.0.0 Safari/537.36",
        "Origin": 'https://m.mi.com',
        "referer": "https://m.mi.com/category",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "client_id": "180100031051",
        "channel_id": "",
        "webp": "1",
        "cat_id": f"{cat_id}"
    }

    res = requests.post(url, headers=headers, data=data).json()
    result = {}
    img = []
    tab = {}
    tab_name = res['data'][0]['category_name']
    item_dict = []
    for i in range(len(res['data'][0]['category_list'])):
        if show == 0:
            if len(item_dict) > 5:
                break
        if res['data'][0]['category_list'][i]['view_type'] == 'cells_auto_fill':
            for _ in range(len(res['data'][0]['category_list'][i]['body']['items'])):
                if res['data'][0]['category_list'][i]['body']['items'][_]['path_type'] == 'image':
                    img.append(res['data'][0]['category_list'][i]['body']['items'][_]['img_url_webp'])  # 获取分类页面的图片
        if res['data'][0]['category_list'][i]['view_type'] == 'category_group':
            tab_title = res['data'][0]['category_list'][i]['body']['title']
            if res['data'][0]['category_list'][i]['body']['is_expand']:
                tab[tab_title] = res['data'][0]['category_list'][i]['body']['product_list']
                item_dict.extend(res['data'][0]['category_list'][i]['body']['product_list'])
            else:
                for _ in range(len(res['data'][0]['category_list'][i]['body']['items'])):
                    product_name = res['data'][0]['category_list'][i]['body']['items'][_]['product_name']
                    path = res['data'][0]['category_list'][i]['body']['items'][_]['action']['path']
                    if res['data'][0]['category_list'][i]['body']['items'][_]['action']['type'] == 'product':
                        tab[product_name] = res['data'][0]['category_list'][i]['body']['items'][_]
                    else:
                        result_ = get_all_product(path)
                        tab[product_name] = result_
                        item_dict.extend(result_)
    result[tab_name] = tab
    # print(item_dict)
    return result, item_dict, img, tab


def get_tab(_type=0):
    if _type == 0:
        _name = 'intelligent.json'
    elif _type == 1:
        _name = 'computer.json'
    elif _type == 2:
        _name = 'air.json'
    elif _type == 3:
        _name = 'watchtv.json'
    elif _type == 4:
        _name = 'wear.json'
    else:
        _name = 'sound.json'

    return _read_scan_data(f'./show/{_name}')

# print(get_info(19492))
# print(json.dumps(_get_shop(1053)[3]))
# print(get_all_product(1598))
