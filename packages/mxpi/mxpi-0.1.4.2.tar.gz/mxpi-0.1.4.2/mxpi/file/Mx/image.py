import requests
import base64
from aip import AipImageClassify
from aip import AipSpeech

class imageAI():
    def __init__(self,APP_ID,APIKey,SecretKey) -> None:
        self.SECRET_KEY=SecretKey
        self.API_KEY=APIKey
        self.APP_ID=APP_ID
        self.data=''
        self.err_code={
            1	:'服务器内部错误,请再次请求, 如果持续出现此类错误,请提交工单联系技术支持团队',
            2	:'服务暂不可用,请再次请求, 如果持续出现此类错误,请提交工单联系技术支持团队',
            3	:'调用的API不存在,请检查请求URL后重新尝试,一般为URL中有非英文字符,如“-”,可手动输入重试',
            4	:'集群超限额,请再次请求, 如果持续出现此类错误,请提交工单联系技术支持团队',
            6	:'无权限访问该用户数据,创建应用时未勾选相关接口,请登录百度云控制台,找到对应的应用,编辑应用,勾选上相关接口,然后重试调用',
            13	:'获取token失败',
            14	:'IAM鉴权失败',
            15	:'应用不存在或者创建失败',
            17	:'每天请求量超限额,已上线计费的接口,请直接在控制台开通计费,调用量不受限制,按调用量阶梯计费；未上线计费的接口,请提交工单联系申请提额',
            18	:'QPS超限额,已上线计费的接口,请直接在控制台开通计费,调用量不受限制,按调用量阶梯计费；未上线计费的接口,请提交工单联系申请提额',
            19	:'请求总量超限额,已上线计费的接口,请直接在控制台开通计费,调用量不受限制,按调用量阶梯计费；未上线计费的接口,请提交工单联系申请提额',
            100	:'无效的access_token参数,token拉取失败,可以参考“Access Token获取”重新获取',
            110	:'access_token无效,token有效期为30天,注意需要定期更换,也可以每次请求都拉取新token',
            111	:'access_token无效,token有效期为30天,注意需要定期更换,也可以每次请求都拉取新token',
            216100	:'请求中包含非法参数,请检查后重新尝试',
            216101	:'缺少必须的参数,请检查参数是否有遗漏',
            216102	:'请求了不支持的服务,请检查调用的url',
            216103	:'请求中某些参数过长,请检查后重新尝试',
            216110	:'appid不存在,请重新核对信息是否为后台应用列表中的appid',
            216200	:'图片为空,请检查后重新尝试',
            216201	:'上传的图片格式错误,现阶段我们支持的图片格式为：PNG、JPG、JPEG、BMP,请进行转码或更换图片',
            216202	:'上传的图片大小错误,现阶段我们支持的图片大小为：base64编码后小于4M,分辨率不高于4096*4096,请重新上传图片',
            216203	:'自定义菜品识别服务错误码：上传的图片中包含多个主体,请上传只包含一个主体的菜品图片入库',
            216204	:'logo识别服务错误码：后端服务超时,请工单联系技术支持团队',
            216630	:'识别错误,请再次请求,如果持续出现此类错误,请提交工单联系技术支持团队',
            216634	:'检测错误,请再次请求,如果持续出现此类错误,请提交工单联系技术支持团队',
            216681	:'添加入库的图片已经在库里,完全相同（Base64编码相同）的图片不能重复入库',
            282000	:'服务器内部错误,请再次请求, 如果持续出现此类错误,请提交工单联系技术支持团队',
            282003	:'请求参数缺失',
            282005	:'处理批量任务时发生部分或全部错误,请根据具体错误码排查',
            282006	:'批量任务处理数量超出限制,请将任务数量减少到10或10以下',
            282100	:'图片压缩转码错误',
            282101	:'长图片切分数量超限',
            282102	:'未检测到图片中识别目标',
            282103	:'图片目标识别错误',
            282110	:'URL参数不存在,请核对URL后再次提交',
            282111	:'URL格式非法,请检查url格式是否符合相应接口的入参要求',
            282112	:'url下载超时,请检查url对应的图床/图片无法下载或链路状况不好,您可以重新尝试一下,如果多次尝试后仍不行,建议更换图片地址',
            282113	:'URL返回无效参数',
            282114	:'URL长度超过1024字节或为0',
            282808	:'request id 不存在',
            282809	:'返回结果请求错误（不属于excel或json）',
            282810	:'图像识别错误',
            283300	:'入参格式有误,可检查下图片编码、代码格式是否有误',
            336000	:'服务器内部错误,请再次请求, 如果持续出现此类错误,请提交工单联系技术支持团队',
            336001	:'入参格式有误,比如缺少必要参数、图片base64编码错误等等,可检查下图片编码、代码格式是否有误。有疑问请提交工单联系技术支持团队',
        }

    def get_file_content(self,filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    def result(self):
        return self.data
    
    def err_msg(self,dat):
        try:
            if dat['error_code']:
                self.data={"error_code":dat['error_code'],"err_msg":self.err_code[dat['error_code']]}
                return self.data
        except:
            self.data=dat
            return self.data

    def advancedGeneral(self,image):
        # 通用场景识别
        client = AipImageClassify(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        image = self.get_file_content(image)
        dat=client.advancedGeneral(image)
        try:
            if dat['log_id']:
                self.data=dat['result'][0]
                return self.data
        except:
            self.err_msg(dat)
    
    def dishDetect(self,image):
        #菜品识别
        client = AipImageClassify(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        image = self.get_file_content(image)
        dat=client.dishDetect(image)
        try:
            if dat['log_id']:
                self.data=dat['result'][0]
                return self.data
        except:
            self.err_msg(dat)
    
    def logoSearch(self,image):
        #logo商标识别
        client = AipImageClassify(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        image = self.get_file_content(image)
        dat=client.logoSearch(image)
        try:
            if dat['log_id']:
                self.data=dat['result'][0]
                return self.data
        except:
            self.err_msg(dat)

    def animalDetect(self,image):
        #动物识别
        client = AipImageClassify(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        image = self.get_file_content(image)
        dat=client.animalDetect(image)
        try:
            if dat['log_id']:
                self.data=dat['result'][0]
                return self.data
        except:
            self.err_msg(dat)

    def plantDetect(self,image):
        #植物识别
        client = AipImageClassify(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        image = self.get_file_content(image)
        dat=client.plantDetect(image)
        try:
            if dat['log_id']:
                self.data=dat['result'][0]
                return self.data
        except:
            self.err_msg(dat)
    
    def objectDetect(self,image,with_face=1):
        #图像主体检测
        client = AipImageClassify(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        image = self.get_file_content(image)
        dat=client.objectDetect(image,{'with_face':with_face})
        try:
            if dat['log_id']:
                self.data=dat['result']
                return self.data
        except:
            self.err_msg(dat)

    def landmark(self,image):
        #地标识别
        client = AipImageClassify(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        image = self.get_file_content(image)
        dat=client.landmark(image)
        try:
            if dat['log_id']:
                self.data=dat['result']
                return self.data
        except:
            self.err_msg(dat)

    def ingredient(self,image):
        #果蔬识别
        client = AipImageClassify(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        image = self.get_file_content(image)
        dat=client.ingredient(image)
        try:
            if dat['log_id']:
                self.data=dat['result'][0]
                return self.data
        except:
            self.err_msg(dat)

    def currency(self,image):
        #货币识别
        client = AipImageClassify(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        image = self.get_file_content(image)
        dat=client.currency(image)
        try:
            if dat['log_id']:
                self.data=dat['result']
                return self.data
        except:
            self.err_msg(dat)

    def carDetect(self,image):
        #车辆识别
        client = AipImageClassify(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        image = self.get_file_content(image)
        dat=client.carDetect(image)
        try:
            if dat['log_id']:
                self.data=dat['result'][0]
                return self.data
        except:
            self.err_msg(dat)

    def asr(self,file,sd,ch):
        # 短语音识别
        client=AipSpeech(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        dat=client.asr(self.get_file_content(file), 'wav', sd, {
            'dev_pid': ch,
        })
        self.data=dat

    def get_file_content(self,filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()
    
    def synthesis(self,text,spd,pit,vol,per,file):
        #短语音合成
        client=AipSpeech(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        result  = client.synthesis(text, 'zh', 1, {
            'spd':spd,
            'pit':pit,
            'vol':vol,
            'per':per,
        })
        self.data=result
        if not isinstance(result, dict):
            with open(file, 'wb') as f:
                f.write(result)