import requests
from common.logger import Logger
from common.exchange_data import ExchangeData
import allure,json,re
from common.read_file import ReadFile
from common.condition import Condition
from common.redis_ops import RedisOps


class Api_Request():


    @classmethod
    def api_data(cls,cases,env_url):
        (
            case_mod,
            case_id,
            case_title,
            header_ex,
            path,
            case_severity,
            skips,
            method,
            parametric_key,
            file_obj,
            data,
            extra,
            sql,
            expect,
        ) = cases

        # Logger.info(f'用例名称：{case_mod}-{case_id}-{case_title}')
        allure.dynamic.story(case_mod)
        Condition().skip_if(cases)  # 根据条件判断是否跳过用例

        # 环境，url ---- 此信息跟着run.py 中的--env=xxx, 对应config.xml 中的server.XXX
        url,env=env_url
        ExchangeData.extra_pool.update({
            "url": url,
            "env": env,
        })

        # 获取配置信息

        # 获取配置文件config.yaml中的用例级别（p1-p5）
        allure.dynamic.severity(ReadFile.read_config('$..cor_rel_case_severity')[case_severity])
        # 获取配置文件config.yaml中的请求头 request_headers
        request_headers=str(ReadFile.read_config('$.request_headers'))
        # 获取配置文件config.yaml中的请求参数 request_parameters
        request_parameters=str(ReadFile.read_config('$.request_parameters'))

        case_title=ExchangeData.rep_expr(case_title,return_type='srt')
        path=ExchangeData.rep_expr(path,return_type='srt')
        # header_ex : excel 用例中的header请求头，其中参数可以从提取参数中通过${XXX}直接获取，如${key},${access_token}
        header_ex=ExchangeData.rep_expr(header_ex,return_type='dict')
        request_headers=ExchangeData.rep_expr(request_headers,return_type='dict')
        data=ExchangeData.rep_expr(data,return_type='dict')
        file_obj=ExchangeData.rep_expr(file_obj,return_type='dict')

        request_parameters = ExchangeData.rep_expr(request_parameters, return_type='dict')

        header_ex.update(request_headers) #合并配置文件中请求头
        #request_headers.update(header_ex)#配置文件中的请求头和获取excel请求头合并
        print("request_headers is {}".format(request_headers))
        print("header_ex is {}".format(header_ex))


        data.update(request_parameters) #合并配置文件中请求参数

        allure.dynamic.title(case_title)
        #allure.dynamic.link('%s%s'%(url,path), name='%s%s'%(url,path))  # 关联的连接

        pattern = re.compile(r'^((https|http|ftp|rtsp|mms)?:\/\/)[^\s]+')
        if (pattern.search(path)) == None:  # 判断读取的地址是否有前缀地址http://192.168.1.153:8562
            if url[-1] == '/':
                url = url[:-1]
            urls ="%s/%s"%(url,path)  # 无前缀读取配置文件添加前缀

        else:
            urls = path  # 有前缀使用读取的完整地址

        allure.dynamic.description("【用例名称】：%s_%s\n\n【请求地址】：%s\n\n【请求参数】：%s"%(case_mod,case_title,urls,data))

        res=Api_Request().api_request(urls,method,parametric_key,header_ex,(data),file_obj)

        ExchangeData.Extract(res,extra)
        #
        # ExchangeData.extra_allure(extra)#显示提取参数路径
        # Logger.info('提取参数路径：%s' % extra)
        # Logger.info('参数池：%s' % ExchangeData.extra_pool)

        return res


    def api_request(self,url, method, parametric_key, header=None, data=None, file_obj=None) -> dict:
        if parametric_key=="params":
            parametric={"params":data}
        elif parametric_key=="data":
            parametric={"data":data}
        elif parametric_key=="json":
            parametric={"json":data}
        else:
            raise ValueError("“parametric_key”的可选关键字为params, json, data")

        if file_obj:
            # files = {
            #     'avatarfile': open('./config/1.jpg', 'rb'),
            # }
            file_objs={}
            for k,v in file_obj.items():
                file_objs[k]=open(v, 'rb')
        else:
            file_objs={}

        req_info = {
            "请求地址": url,
            "请求头": header,
            "请求方法": method,
            '参数类型':parametric_key,
            "请求数据": data,
            "上传文件": file_obj,
        }
        with allure.step('请求数据：'):
            allure.attach(
                json.dumps(req_info, ensure_ascii=False, indent=4),
                "附件内容",
                allure.attachment_type.JSON,
            )

        Logger.info('接口地址：%s' % url)
        Logger.info('请求头：%s' % header)
        Logger.info('请求方法：%s' % method)
        Logger.info('参数类型：%s' % parametric_key)
        Logger.info('请求参数：%s' % data)
        Logger.info('上传文件：%s' % file_obj)

        try:

            res = requests.request(method=method, url=url,  headers=header,timeout=10,files=file_objs, **parametric)#files=file,
            response = res.json()


        except Exception as e:
            Logger.error('请求发送失败：%s'%((e)))
            response={'response':str(e)}
            #raise '请求发送失败：%s'%((e))


        Logger.info('返回响应：%s' % response)

        with allure.step('响应数据：'):
            allure.attach(
                json.dumps(response, ensure_ascii=False, indent=4),
                "附件内容",
                allure.attachment_type.JSON,
            )


        return response


#
if __name__ == '__main__':
    Api_Request=Api_Request()
    method = 'post'  #get,post,put,delete,head,options,patch
    url = "http://47.105.60.25/emergency/AuthApi/oauth/token"
    header = {
        'Authorization': 'Basic R0FTOmhueU5CQDcwMg=='
    }
    """
    1. params：类似这种：url?参数名=参数值&参数名1=参数值1
    2. data：请求头content-type是from表单类型。
    3. json：请求头content-type：application/json。
    """
    parametric_key="params"#  params,data,json三种类型
    data = {
        "grant_type": "hnymima",
        "username": "admin",
        "password": "system@702"
    }
    #data ={}
    file=''  #上传文件路径
    a = Api_Request.api_request(url,method,parametric_key,header,data,file)
    print(a)


