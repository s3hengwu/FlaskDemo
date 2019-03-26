from flask import jsonify, request
from .bp import bp
from models import User, WxUser, Album
from .actions import account
from db import db
import json
import requests


@bp.route('/', methods=['GET', 'POST'])
def index():
    js = {
        'message': 1,
        'error': 0,
        'data': [{'pos': 1}, {'pos': 2}]
    }
    return jsonify(js)


@bp.route('/<string:name>/<int:pwd>')
def login(name, pwd):
    user = User(name, pwd)
    db.session.add(user)
    db.session.commit()
    return "创建用户 %s, 密码 %d" % (name, pwd)


@bp.route('/login/<string:name>')
def loginByName(name):
    user = User.query.filter(User.name == name).first()
    if user is None or user.name.strip == '':
        return '用户不存在'
    else:
        return '%s 用户登陆' % user.name


@bp.route('/checkout')
def checkAll():
    user = User.query.all()
    print(user)
    return json.dumps({'data': [{'name': u.name, 'pwd': u.thrust} for u in user]}, indent=4)


@bp.route('/update/<string:name>/<string:pwd>')
def update(name, pwd):
    user = User.query.filter(User.name == name).first()
    if user is not None:
        user.thrust = pwd
        db.session.commit()
        return '修改 用户 %s ,密码为：%s' % (name, pwd)
    else:
        return '用户不存在'


@bp.route('/delete/<string:name>/<string:pwd>')
def delete(name, pwd):
    user = User.query.filter(User.name == name, User.thrust == pwd).first()
    if user is not None:
        db.session.delete(user)
        db.session.commit()
        return '删除 用户 %s ,密码为：%s' % (name, pwd)
    else:
        return '用户不存在，或密码不正确'


@bp.route('/jscode2session', methods=['GET', 'POST'])
def jscode2session():
    """"
     获取openid
    {"session_key":"Ielf+tnXUWxosHpldzuAEg==","openid":"o9J6P4iDujBp9jyiIlqjXNAKBPwk"}
    {"errcode":40029,"errmsg":"invalid code, hints: [ req_id: 6EkbY7aLRa-se8T9 ]"}
    :return:
    """""
    code = request.args.get("code")
    print(code)
    params = {
        'appid': 'wxd3c680b23014dbe2',
        'secret': '524108b3a68da5db9f19f3ade206377b',
        'js_code': code,
        'grant_type': 'authorization_code'
    }
    r = requests.get('https://api.weixin.qq.com/sns/jscode2session', params=params)
    if r.status_code == 200:
        return r.text
    else:
        return json.dumps({'status': '-1', 'msg': '获取失败'}, ensure_ascii=False)


@bp.route('/wxlogin', methods=['GET', 'POST'])
def wxlogin():
    open_id = request.args.get("open_id")
    name = request.args.get("name")
    avatar = request.args.get("avatar")
    user = WxUser.query.filter_by(id=open_id).first()

    if user is None:
        # 不存在用户，创建用户
        user = WxUser(open_id="1", name=name, avatar=avatar)
        db.session.add(user)
        db.session.commit()

    return "session_key"


@bp.route('/ercode', methods=['GET', 'POST'])
def ercode():
    code = account.get_er_code()
    return str(code)


@bp.route('/album', methods=['GET', 'POST'])
def album():
    open_id = request.args.get("open_id")
    name = request.args.get("name")
    create_album = Album(open_id, name)
    db.session.add(create_album)
    db.session.commit()
    return json.dumps({'status': '1', 'msg': '创建成功'}, ensure_ascii=False)


@bp.route('/updated_album/<album_id>/<open_id>/<name>', methods=['GET', 'POST'])
def updated_album(album_id, open_id, name):
    update_album = Album.query.filter(Album.id == album_id).first()
    if update_album is not None:
        if open_id == update_album.open_id:
            print('可以修改')
            update_album.name = name
            db.session.commit()
        else:
            print('不是当前用户的，不可以修改')
            return json.dumps({'status': '-1', 'msg': '不是当前用户的，不可以修改'}, ensure_ascii=False)
    else:
        return '用户不存在'
    return json.dumps({'status': '1', 'msg': '修改成功成功'}, ensure_ascii=False)


@bp.route('/del_album/<album_id>', methods=['GET', 'POST'])
def del_album(album_id):
    will_del_album = Album.query.filter(Album.id == album_id).first()
    if album is not None:
        db.session.delete(will_del_album)
        db.session.commit()
        return json.dumps({'status': '1', 'msg': '删除成功'}, ensure_ascii=False)
    else:
        json.dumps({'status': '-1', 'msg': '删除失败'}, ensure_ascii=False)
