import os
import base64

import numpy as np
from werkzeug.utils import secure_filename
import face_recognition

from service.model import db
from service.model.face import Face
from service.model.log import Log


def gen_img_name(uid, timestamp):
    """Generate image name according to user id and timestamp."""
    uid = secure_filename(uid)
    timestamp = secure_filename(timestamp)
    img_name = '{}-{}.jpg'.format(uid, timestamp)
    return img_name


def decode_img(encoded_img):
    """Decode base64 code to an image."""
    img = base64.b64decode(encoded_img)
    return img


def save_img(img, file_dir, file_name):
    """Save image to file system."""
    file_path = os.path.join(file_dir, file_name)
    # In case image folder not exits.
    if not os.path.exists(file_dir):
        os.mkdir(file_dir)
    with open(file_path, 'wb') as f:
        f.write(img)
    return file_path


def face_encoding(img_path):
    """Read image from file system, and encode to a vector."""
    img = face_recognition.load_image_file(img_path)
    # Use hog algorithm first.
    boxes = face_recognition.face_locations(img, model='hog')
    if len(boxes) == 0:
        print('WARNING:using CNN!')
        boxes = face_recognition.face_locations(img, model='cnn')
    # We only need the most significant face.
    encoded_faces = face_recognition.face_encodings(img, boxes)
    if len(encoded_faces) > 0:
        return encoded_faces[0]
    return None


def save_face(uid, uid_type, name, channel, 
              timestamp, encoded_face, img_path):
    """Save information of face to database."""
    user = Face(
        feature_array=encoded_face,
        uid=uid, 
        uid_type=uid_type, 
        name=name, 
        channel=channel, 
        login_time=timestamp, 
        img_path=img_path
    )
    db.session.add(user)
    db.session.commit()


def get_most_related_face(encoded_face):
    """Find the most related face from database."""
    all_face = Face.query.all()
    most_related_face = None
    min_disrance = None
    for face in all_face:
        feature = face.feature.split('|')
        feature = list(map(float, feature))
        distance = np.linalg.norm(feature - encoded_face)
        if min_disrance is None or distance < min_disrance:
            min_disrance = distance
            most_related_face = face
    return most_related_face


def add_log(uid, uid_type, name, channel, check_time, img_path, sim, result):
    """Write a log to Log table in database.
    """
    log = Log(
        uid=uid, 
        uid_type=uid_type, 
        name=name, 
        channel=channel, 
        check_time=check_time, 
        img_path=img_path, 
        sim=sim, 
        result=result
    )
    db.session.add(log)
    # Get the flow number.
    db.session.flush()
    flow_no = log.num
    db.session.commit()
    return flow_no


def face_compare(logined_face, encoded_face, tolerance):
    """Compare two face and return result.
    
    Args:
        logined_face: a vector of face logined in database.
        encoded_face: a vector of uploaded face.
    
    Return:
        sim: similarity of two faces.
        sim_result: result of comparation, 
                    '1' represents two faces are same, 
                    '0' not.
    """
    logined_face_encoding = logined_face.feature.split('|')

    logined_face_encoding = list(
                                 map(lambda x: float(x), 
                                     logined_face_encoding)
                                )
    distances = face_recognition.face_distance(
        [logined_face_encoding], encoded_face)
    face_distance = float(distances[0])
    sim_result = '1' if face_distance < tolerance else '0'
    sim = 1 - face_distance
    return sim, sim_result

