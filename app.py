from flask import Flask, request, make_response
from flask_cors import CORS
from show.get_show import get_shop
from show.get_show import get_tab, get_buyer_show_list
from login.login import user_sign_in, user_login
from shopping.shopping import search_shopping, get_shopping, get_info, clear_shopping
from show.show_pic import get_shop as get_pic_to

app = Flask(__name__)
CORS(app, supports_credentials=True)


# @app.after_request
# def add_cors_headers(response):
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
#     # response.headers.add('Access-Control-Allow-Referer', 'http://localhost:5173/')
#     response.headers.add('Referrer-Policy', 'strict-origin-when-cross-origin')
#     response.headers.add('Access-Control-Allow-Credentials', True)
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#     response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
#
#     return response
@app.route('/response', methods=['POST'])
def response():
    if request.method == 'POST':
        data = request.get_json()['data']
        return data
    else:
        return '传入的参数不正常'


@app.route('/get_pic', methods=['POST'])
def get_pic():
    if request.is_json:
        data = request.get_json()['mode']
        return get_pic_to(cat_id=data)
    else:
        return {'code': 400, 'message': "格式不正确"}


@app.route('/get_info', methods=['POST'])
def get_shop_info():
    data = request.get_json()
    return get_info(data['product'])


@app.route('/get_shopping_list', methods=['POST'])
def get_shopping_list():  # 查询购物车列表
    cookie_value = request.cookies.get('token')
    if cookie_value:
        try:
            return {'code': 200, 'data': search_shopping(cookie_value)}
        except Exception as e:
            print(e)
            return {'code': 400, 'msg': '用户尚未登录'}
    else:
        return {'code': 400, 'msg': '用户尚未登录'}


@app.route('/clear', methods=['POST'])
def clear_shop():
    cookie_value = request.cookies.get('token')
    if cookie_value:
        return {'code': 200, 'data': clear_shopping(cookie_value)}
    else:
        return {'code': 400, 'msg': '用户尚未登录'}


@app.route('/get_shopping', methods=['POST'])
def get_shopping_():  # 修改购物车
    if request.is_json:
        data = request.get_json()
        cookie_value = request.cookies.get('token')
        if cookie_value:
            return {'code': 200, 'data': get_shopping(cookie_value, data['shopping'])}
        else:
            return {'code': 400, 'msg': '用户尚未登录'}
    else:
        return {'code': -1}


@app.route('/get_login_in', methods=['POST'])
def get_login_in():
    if request.is_json:
        # 请求参数是 JSON 类型
        try:
            result = user_login()
            if result['code'] == 0:
                response_ = make_response({'code': 200, 'token': f'{result["token"]}'})
                response_.set_cookie('token', result['token'], path='/', secure=True, samesite='None',
                                     httponly=True)
                return response_
            else:
                return {'code': 1, 'msg': '登录失败'}
        except IndexError:
            return {'code': 2, 'msg': '参数不对'}
    else:
        # 请求参数不是 JSON 类型
        return {'code': -1}


@app.route('/get_login', methods=['POST'])
def get_login():
    if request.is_json:
        # 请求参数是 JSON 类型
        try:
            data = request.get_json()
            username = data['account']
            password = data['password']
            college = data['college']
            age = int(data['age'])
            content_url = data['content']['url']
            date = data['date']
            email = data['email']
            desc = data['description']
            course = data['course']
            gender = data['gender']
            return user_sign_in(username, password, college, age, content_url, date, email, desc, course, gender)
        except IndexError:
            return {'code': 400, 'msg': '参数不对'}
    else:
        # 请求参数不是 JSON 类型
        return {'code': -1}


@app.route('/get_show', methods=['POST'])
def get_show():
    if request.is_json:
        # 请求参数是 JSON 类型
        _type = request.get_json()['type']
        if _type == 0:
            data = request.get_json()['id']
        else:
            data = 0
        return get_shop(data, _type)
    else:
        # 请求参数不是 JSON 类型
        return {'code': -1}


@app.route('/get_show_1', methods=['POST'])
def get_show_1():
    if request.is_json:
        # 请求参数是 JSON 类型
        _type = request.get_json()['type']
        return get_tab(_type)
    else:
        # 请求参数不是 JSON 类型
        return {'code': -1}


@app.route('/buyer_show_list', methods=['POST'])
def buyer_show_list():
    if request.is_json:
        _id = request.get_json()['product_id']
        page_index = request.get_json()['page_index']
        page_size = request.get_json()['page_size']
        session_id = request.get_json()['session_id']
        return get_buyer_show_list(_id, page_index, page_size, session_id)
    else:
        return {'code': 400, 'msg': '你传入的参数格式不正确'}


@app.route('/process_data', methods=['POST'])
def process_data():
    if request.is_json:
        # 请求参数是 JSON 类型
        # data = request.get_json()
        # 处理 JSON 数据
        # ...
        return "Success"
    else:
        # 请求参数不是 JSON 类型
        return "Request is not JSON", 400


@app.route('/set_cookie')
def set_cookie():
    response_ = make_response('Cookie is set.')
    response_.set_cookie('cookie_name', 'cookie_value')
    return response_


@app.route('/get_cookie')
def get_cookie():
    cookie_value = request.cookies.get('cookie_name')
    if cookie_value:
        return f'The cookie value is {cookie_value}'
    else:
        return 'The cookie does not exist.'


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
