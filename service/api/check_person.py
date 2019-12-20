import datetime

from flask import Blueprint
from flask import request

from service.common.utils import gen_img_name, decode_img, save_img, \
                                 face_encoding, get_most_related_face, \
                                 add_log, face_compare, get_login_face
from service.common.responser import *
from service import parameters

check_person_module = Blueprint('check_person_module', __name__)

@check_person_module.route('/faceService/checkPerson', methods=['POST'])
def check_person():
    """Verify person service
    
    Program flow
    1. Get and check parameters.
    2. Decode and save image.
    3. Read from face(s) to be compared from database.
    4. Compare face.
    5. Log the request.
    """

    # Get paramters.
    key_list = ['uid', 'uid_type', 'name', 'channel', 'img']
    try:
        uid, uid_type, name, channel, encoded_img = \
            [request.form[key] for key in key_list]
    except KeyError:
        return InputMissingResponser.wrap()
    
    # Generate a timestamp to mark this request.
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

    img_name = gen_img_name(uid, timestamp)

    img = decode_img(encoded_img)
    img_path = save_img(img, parameters['check_image_root'], img_name)

    # Encode face from image in file system.
    encoded_face = face_encoding(img_path)
    # Cannot found face.
    if encoded_face is None:
        return CannotFoundFaceResponser.wrap()

    # There are two modes:
    #   1) one vs one: given the user's id, and 
    #      match the face in database directly.
    #   2) one vs n: retrieve the most related
    #      face and compare it with uploaded face.
    if 'mode' not in request.form:
        mode = '1v1'
    else:
        mode = request.form['mode']

    if mode.lower() == '1vn':
        logined_face = get_most_related_face(encoded_face)
        if logined_face is None:
            return FaceAbsentResponser.wrap()
        uid, uid_type, name = logined_face.uid, logined_face.uid_type, logined_face.name
    elif mode.lower() == '1v1':
        # Read face from database.
        logined_face = get_login_face(uid)
        if not logined_face:
            return FaceAbsentResponser.wrap()
    else:
        # mode is not allowed.
        ModeNotAllowedResponser.wrap()

    # sim is the similarity of two faces.(0-1, the larger, the more similar)
    sim, result = face_compare(logined_face, encoded_face, parameters['tolerance'])

    # Save log to database.
    flow_no = add_log(
        uid=uid, 
        uid_type=uid_type,
        name=name,
        channel=channel,
        check_time=timestamp,
        img_path=img_path,
        sim=sim,
        result=result
    )

    return CheckFaceSuccessResponser.wrap(uid=uid, 
                                          uid_type=uid_type, 
                                          name=name, 
                                          sim=round(sim, 5), 
                                          simResult=result, 
                                          imgFlowNo=flow_no, 
                                          mode=mode)
