import json

__all__ = [
    'InputMissingResponser', 
    'SystemErrorResponser', 
    'AddFaceSuccessResponser',
    'FaceAlreadyLoginedResponser',
    'CannotFoundFaceResponser',
    'FaceAbsentResponser',
    'CheckFaceSuccessResponser'
]


class Responser(object):
    """Interface of responser."""
    def wrap(self):
        # 实现了直接根据变量构造返回体
        return json.dumps(self.__dict__)


class CommonResponser(Responser):
    """Common part of a Responser.
    """
    def __init__(self, code, message):
        self.code = code
        self.message = message



class CheckFaceResponser(CommonResponser):
    """Responser for check person service.
    """
    
    def __init__(self, code, message):
        super().__init__(code, message)
    
    def wrap(self, uid, uid_type, name, sim, simResult, imgFlowNo, mode):
        self.uid = uid
        self.uid_type = uid_type
        self.name = name
        self.sim = sim
        self.simResult = simResult
        self.imgFlowNo = imgFlowNo
        self.mode = mode
        return super().wrap()


InputMissingResponser = CommonResponser(code=1, message='请求输入参数中，有缺失参数')
SystemErrorResponser = CommonResponser(code=12, message='系统参数读取错误')
AddFaceSuccessResponser = CommonResponser(code=0, message='注册成功')
FaceAlreadyLoginedResponser = CommonResponser(code=10, message='该人脸已经注册过了')
CannotFoundFaceResponser = CommonResponser(code=8, message='找不到图片中的人脸')
FaceAbsentResponser = CommonResponser(code=9, message='人脸未注册')
CheckFaceSuccessResponser = CheckFaceResponser(code=0, message='成功请求人脸识别服务')

