import pytest,allure
from common.assert_api import AssertApi
from common.api_request import Api_Request
from common.read_exce_yaml_caes import get_yaml_excle_caes
from common.read_file import ReadFile
from run import env

@allure.epic(ReadFile.read_config("$.project_name"))  # 项目名称

# 调用开发环境用例 记得run.py ---- "--env=dev"
# @pytest.mark.parametrize("case",get_yaml_excle_caes('dev'))

class Test_Dev():

    @pytest.mark.parametrize("case",get_yaml_excle_caes(env))
    @allure.step
    def test_001(self,case,get_db,env_url):

        # 获取接口返回值
        response=(Api_Request.api_data(case,env_url))

        assert AssertApi().assert_api(response,case,get_db)

#调用测试环境用例 记得run.py ---- "--env=test"
# class Test_Test():
#
#     @pytest.mark.parametrize("case",get_yaml_excle_caes('test'))
#     @allure.step
#     def test_001(self,case,get_db,env_url):
#
#         response=(Api_Request.api_data(case,env_url))
#
#         assert AssertApi().assert_api(response,case,get_db)

