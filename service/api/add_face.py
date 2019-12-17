import datetime
from flask import Blueprint
from flask import request
from sqlalchemy.exc import IntegrityError
from service.common.utils import gen_img_name, save_img, face_encoding, decode_img, save_face
from service.common.responser import *
from service import parameters

add_face_module = Blueprint("add_face_module", __name__)

@add_face_module.route('/faceService/addFaces', methods=['POST'])
def add_face():
    """Login face service.
    
    Program flow：:
    1. Get and check parameters
    2. Decode and save image.
    3. Encode image into face vector.
    4. Save to database.
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

    try:
        img = decode_img(encoded_img)
        img_path = save_img(img, parameters['login_image_root'], img_name)
    except KeyError:
        return SystemErrorResponser.wrap()

    # Encode face from image in file system.
    encoded_face = face_encoding(img_path)
    if encoded_face is None:
        return CannotFoundFaceResponser.wrap()

    # Save to database.
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
    # This means the face is already logined.
    except IntegrityError: 
        return FaceAlreadyLoginedResponser.wrap()

    return AddFaceSuccessResponser.wrap()
