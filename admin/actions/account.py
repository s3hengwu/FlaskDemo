from ..crypto import encode_er_code
from models import Code
from db import db


def remove_code(code, v):
    print("删除code:" + str(code))
    # exist_code = Code.query.filter_by(Code.code == code).first()
    # if exist_code:
    #     db.session.delete(exist_code)
    #     db.session.commit()


def add_code(code):
    print("添加code:"+str(code))
    code_created = Code(code)
    db.session.add(code_created)
    db.session.commit()


def get_er_code():
    # 生成随机二维码
    code = encode_er_code()
    print(code)
    add_code(code)
    # Timer(10, remove_code, (code, time.time())).start()
    return code
