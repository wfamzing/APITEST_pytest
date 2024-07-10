from common.exchange_data import ExchangeData
from common.logger import Logger
import jsonpath,allure,json


class AssertApi():
    re_sql_data={}

    def assert_api(self,response,case,get_db=None):
        self.assert_sql(case,get_db)

        expectlist=case[-1] #断言内容提取
        result_all=[]#多个断言结果列表 True False
        result_dic_list=[]
        if type(response) != dict:
            response={"response":response}

        self.re_sql_data.update(response)
        Logger.info(self.re_sql_data)

        #后置提取参数
        extra = case[-3]  # 后置提取参数到参数池中
        ExchangeData.allure_step_text('提取参数路径：',extra)#显示提取参数路径
        ExchangeData.Extract(self.re_sql_data,extra)
        ExchangeData.extra_pool_allure()  # 显示参数池数
        Logger.info('提取参数路径：%s' % extra)
        Logger.info('参数池：%s' % ExchangeData.extra_pool)
        Logger.info('断言内容：%s' % expectlist)
        if expectlist != "" and expectlist != "{}":
            n = 1
            expectlist_change = ExchangeData.rep_expr(expectlist, return_type='dict')
            # try:
            if expectlist.find("],[") != -1:
                expectlist = expectlist.replace("[[", "[").replace("]]", "]")
            expectlist = eval(expectlist)
            # except:
            #     expectlist=expectlist.split("],[")
            Logger.info('变量引用后的断言内容：%s' % str(expectlist))
            for expect_group in expectlist:
                expected_value, assert_type, jsonpath_str, data_type = expect_group
                msg = ''
                loc = locals()
                # 提取实际值
                try:
                    actual_value = ExchangeData.Extract_noe(self.re_sql_data, jsonpath_str)
                except Exception as e:
                    Logger.error(f"无法从 {jsonpath_str} 提取实际值：{e}")
                    msg="[%s]"%e
                try:
                    if data_type=='str':
                        try:
                            Logger.info(f'asser_results = "{expected_value}" {assert_type} "{actual_value}"')
                            exec(f'asser_results = "{expected_value}" {assert_type} "{actual_value}"')
                        except:
                            Logger.info(f"asser_results = '{expected_value}' {assert_type} '{actual_value}'")
                            exec(f"asser_results = '{expected_value}' {assert_type} '{actual_value}'")

                    elif data_type=='int':
                        Logger.info(f"asser_results = {expected_value} {assert_type} {actual_value}")
                        exec(f"asser_results = {expected_value} {assert_type} {actual_value}")

                    else:
                        raise "没有定义，这样{}的数据类型，当前定义了[str,int]".format(assert_type)
                    result=(loc['asser_results'])
                except Exception as e:
                    Logger.error("断言异常：%s（请检查数据类型……）"%e)
                    result = False
                    msg="[%s]"%e
                try:
                    expect_jsonpath_str = jsonpath_str.replace("[[", "").replace("]]", "")
                except:
                    expect_jsonpath_str = str(jsonpath_str)

                Logger.info(expect_jsonpath_str)
                result_dic={
                        "提取路径": expect_jsonpath_str,
                        "预期结果": expected_value,
                        "断言类型": assert_type,
                        "实际结果": actual_value,
                        "测试结果": '%s %s'%(result,msg)
                        }
                result_all.append(result)
                result_dic_list.append(result_dic)

                n += 1
        else:
            Logger.warning('没有写断言……')
            result_all = [False]
            result_dic_list.append({"result":"没有添加断言,无断言用例标记失败，请添加断言判断用例",})

        with allure.step('断言：%s'%(False not in result_all)):
            Logger.info(self.re_sql_data)
            allure.attach(
                json.dumps(self.re_sql_data, ensure_ascii=False, indent=4),
                're_sql_data',
                allure.attachment_type.JSON,
            )
            for result_dic in result_dic_list:
                allure.attach(
                    json.dumps(result_dic, ensure_ascii=False, indent=4).replace("\\",''),
                    "断言：%s：" % (result_dic.get('测试结果',False)),
                    allure.attachment_type.JSON,
                )

        Logger.info(result_all)
        self.re_sql_data.clear()
        return False not in result_all

    # 和数据库中的数据对比
    def assert_sql(self, case,get_db=None):
        if get_db!=None:
            sql_srt=case[-2]
            if sql_srt!="":
                sql_srt = ExchangeData.rep_expr(sql_srt, return_type='srt')

                with allure.step('执行sql：'):
                    for n,sql in enumerate(sql_srt.split(";")):
                        Logger.info([n,sql])
                        try:
                            data_sql_dic = get_db.execute_sql(sql)
                        except Exception as e:
                            Logger.error(f'数据库查询失败！（{e}）')
                            data_sql_dic = {'message': "数据库查询失败！","error":f"{e}"}
                        Logger.info(data_sql_dic)
                        Logger.info(type(data_sql_dic))
                        #ExchangeData.extra_pool.update({"sql_%s_data"%n:data_sql_dic})
                        self.re_sql_data.update({"sql_%s_data"%n:data_sql_dic})
                        #Logger.info(ExchangeData.extra_pool)

                        try:
                            allure_data=json.dumps({"sql_%s_data"%n:data_sql_dic}, ensure_ascii=False, indent=4)
                        except Exception as e:
                            allure_data = json.dumps("sql_%s_data:'%s'"%(n,data_sql_dic), ensure_ascii=False, indent=4)
                            Logger.warning('sql查询数据转换插入allure报告数据，出现异常！！（%s）'%e)

                        allure.attach( allure_data,sql, allure.attachment_type.JSON,)


if __name__ == '__main__':
    AssertApi=AssertApi()









