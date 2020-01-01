import datetime
import json
import base64

from flask import Blueprint
from flask import request

from service import parameters

data_service_module = Blueprint('data', __name__)


@data_service_module.route('/admin/parameters', methods=['GET'])
def get_parameters():
	return json.dumps(parameters)


@app.route('/admin/parameters', methods=['POST'])
def set_parameters():
	new_param = request.get_json()
	new_param['sim_threshold'] = float(new_param['sim_threshold'])
	with open('service/parameters.json', 'w') as f:
		json.dump(new_param, f, indent=4)
	return '''success'''


@app.route('/admin/faces', methods=['GET'])
def get_face():
	return query_all('Face')


@app.route('/admin/log', methods=['GET'])
def get_log():
	return query_all('Log')


def query_all(class_name):
	ins_list = eval(class_name).query.all()
	for i in range(len(ins_list)):
		ins_list[i] = ins_list[i].serialize()
	data = {'data': ins_list}
	return json.dumps(data)


@app.route('/admin/image', methods=['POST'])
def get_image():
	path = json.loads(request.form.get('data'))['path']
	print(path)
	try:
		with open(path, "rb") as image_file:
			encoded_string = base64.b64encode(image_file.read())
	except IOError:
		print('WARNING:file open error!')
		return '''failed'''

	return encoded_string
	

# 给出id，查出注册照片路径
@app.route('/admin/image/path/<uid>', methods=['GET'])
def get_image_path(uid):
    path = ''
    try:
        face = Face.query.filter_by(uid=uid).all()
    except BaseException as e:
        # print(e)
        print('WARNING:图片路径查询失败，该id可能尚未注册')
        return path
    
    if (len(face) != 1):
        print('WARNING:图片路径查询失败，出现多个结果')
        return path

    path = face[0].img_path
    return path

