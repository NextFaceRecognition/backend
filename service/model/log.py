from service.model import db

class Log(db.Model):
    __tablename__ = 'check_log'

    num = db.Column(db.Integer, primary_key=True, autoincrement=True)#图片流水号
    uid = db.Column(db.String(32))#用户id
    uid_type = db.Column(db.String(16))#用户id的类型
    name = db.Column(db.String(15))#用户名
    channel = db.Column(db.String(16))#提交渠道
    check_time = db.Column(db.String(19))#验证时间
    img_path = db.Column(db.String(4096))#图片存放路径
    result = db.Column(db.Integer)#验证结果
    sim = db.Column(db.Float)#验证相似度

    # 构造方法
    def __init__(self, uid, uid_type, name, channel, check_time, img_path, sim, result):
        self.uid = uid
        self.uid_type = uid_type
        self.name = name
        self.channel = channel
        self.check_time = check_time
        self.img_path = img_path
        self.sim = sim
        self.result = result

    def serialize(self):
        log = []
        log.append(self.num)
        log.append(self.uid)
        log.append(self.uid_type)
        log.append(self.name)
        log.append(self.channel)
        log.append(self.check_time)
        log.append(self.sim)
        log.append(self.result)
        log.append(self.img_path)
        # 最后的空字符串是为了填充查看对比结果的位置
        log.append('')
        return log
