from service.model import db

# 特征维度时128
FEATURE_DIMENSION = 128

# 数据库的一个表在flask中对应一个类
class Face(db.Model):
    # __tablename__用于定义表名
    __tablename__ = 'login_face'
    # 接下去的变量是字段名，用db.Column来定义字段属性
    uid = db.Column(db.String(32), primary_key=True)#用户id
    uid_type = db.Column(db.String(16))#用户id的类型
    name = db.Column(db.String(15))#用户名
    channel = db.Column(db.String(16))#提交渠道
    login_time = db.Column(db.String(19))#注册时间
    feature = db.Column(db.String(4096))#特征字串
    img_path = db.Column(db.String(4096))#图片存放路径

    # 构造方法
    def __init__(self, uid, uid_type, name, channel, login_time, feature_array, img_path):
        self.uid = uid
        self.uid_type = uid_type
        self.name = name
        self.channel = channel
        self.login_time = login_time
        self.feature = self.to_feature_string(feature_array)
        self.img_path = img_path

    def to_feature_string(self, feature_array):#将特征向量转化为特征字串
        feature_string = ''
        for i in range(FEATURE_DIMENSION - 1):
            feature_string += (str(feature_array[i]) + '|')
        feature_string += str(feature_array[FEATURE_DIMENSION - 1])
        return feature_string

    def serialize(self):
        faces = []
        faces.append(self.uid)
        faces.append(self.uid_type)
        faces.append(self.name)
        faces.append(self.channel)
        faces.append(self.login_time)
        faces.append(self.img_path)
        # 最后的空字符串是为了填充查看人脸照片的位置
        faces.append('')
        return faces
