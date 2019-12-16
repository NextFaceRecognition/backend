import datetime
from flask import Blueprint
from flask import request
from sqlalchemy.exc import IntegrityError
from service.common.utils import get_data, gen_img_name, save_img, face_encoding, decode_img, save_face
from service.common.responser import *
from service import parameters

add_face_module = Blueprint("add_face_module", __name__)

# 人脸注册服务
@add_face_module.route('/faceService/addFaces', methods=['POST'])
def add_face():
    '''
    程序流程：
    1、检查请求参数
    2、解码并保存照片
    3、人脸编码
    4、存数据库
    '''

    # 检查请求参数，同时获取这些数据，赋值给对应变量，如果数值不存在，则返回输入字段缺失错误
    try:
        uid, uid_type, name, channel, encoded_img = \
                        get_data(request.form, ['uid', 'uid_type', 'name', 'channel', 'img'])
    except KeyError:
        return InputIntegrityException.wrap()

    # 给该请求标记一个timestamp，后续作为统一的标记
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

    # 生成图片路径，将图片解码并保存
    img_name = gen_img_name(uid, timestamp)

    try:
        img = decode_img(encoded_img)
        img_path = save_img(img, parameters['login_image_root'], img_name)
    # 读取参数时如果没有login_image_root键，就回报错
    except KeyError:
        return SystemParametersException.wrap()

    # 读取文件夹下的图片，进行人脸编码
    encoded_face = face_encoding(img_path)
    # 找不到人脸时，编码为空
    if encoded_face is None:
        return CannotFoundFaceException.wrap()

    # 保存人脸到数据库
    try:
        save_face(
            uid=uid,
            uid_type=uid_type,
            name=name,
            channel=channel,
            timestamp=timestamp,
            encoded_face=encoded_face,
            img_path=img_path
        )
    # 已经注册过了
    except IntegrityError: 
        return FaceAlreadyLoginedException.wrap()


    return AddFaceSuccess.wrap()

