import datetime
from flask import Blueprint
from flask import request
from service.common.utils import get_data, gen_img_name, decode_img, save_img, \
                                face_encoding, get_most_related_face, addLog, \
                                face_compare
from service.common.responser import *
from service import parameters


check_person_module = Blueprint("check_person_module", __name__)

# 人脸验证服务
@check_person_module.route('/faceService/checkPerson', methods=['POST'])
def check_person():
    '''
    程序流程：
    1、检查请求参数
    2、读取数据库中对应的图片编码
    3、解码并保存图片
    4、人脸编码
    5、两张照片对比
    6、对比记录存数据库
    '''

    # 检查请求参数，同时获取这些数据，赋值给对应变量，如果数值不存在，则返回输入字段缺失错误
    try:
        uid, uid_type, name, channel, encoded_img =\
                get_data(request.form, ['uid', 'uid_type', 'name', 'channel', 'img'])
    except KeyError:
        return InputIntegrityException.wrap()
    
    # 给该请求标记一个timestamp，后续作为统一的标记
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

    # 生成图片路径，将图片解码并保存
    img_name = gen_img_name(uid, timestamp)

    try:
        img = decode_img(encoded_img)
        img_path = save_img(img, parameters['check_image_root'], img_name)
    # 读取参数时如果没有login_image_root键，就回报错
    except KeyError:
        return SystemParametersException.wrap()

    # 读取文件夹下的图片，进行人脸编码
    encoded_face = face_encoding(img_path)
    # 找不到人脸时，编码为空
    if encoded_face is None:
        return CannotFoundFaceException.wrap()

    '''
        此处设计了两种模式：
            1vN模式表示没有上传uid，直接匹配人脸
            1v1模式表示上传了uid，将uid对应的人脸和上传人脸进行一对一对比
    '''
    if 'mode' not in request.form:
        mode = '1v1'
    else:
        mode = request.form['mode']

    if mode == '1vN':
        logined_face = get_most_related_face(encoded_face)
        uid, uid_type, name = logined_face.uid, logined_face.uid_type, logined_face.name
        print('The most related user: uid = %s, uid_type=%s name = %s' % (uid, uid_type, name))
    elif mode == '1v1':
        # 读取数据库中的注册人脸
        try:
            logined_face = get_login_face(uid)
        except NoResultFound:
            return FaceAbsentException.wrap()
        if not logined_face:
            return FaceAbsentException.wrap()

    # 将encoded_face（上传的人脸）和logined_face（注册时的人脸）进行比较
    # 返回的sim为相似度，sim_result为对比结果
    sim, result = face_compare(logined_face, encoded_face, parameters['tolerance'])

    # 将对比记录存放到数据库
    flow_no = addLog(
        uid=uid, 
        uid_type=uid_type,
        name=name,
        channel=channel,
        check_time=timestamp,
        img_path=img_path,
        sim=sim,
        result=result
    )

    return CheckFaceSuccess.wrap(uid=uid, uid_type=uid_type, name=name, \
        sim=round(sim, 5), simResult=result, imgFlowNo=flow_no, mode=mode)
