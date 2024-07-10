import os,sys
import pytest,shutil,subprocess
from common import all_path

# 选择环境
env = sys.argv[1]

def run(env):
    try:
        # 删除allure历史数据
        shutil.rmtree(all_path.targetPath)
        os.makedirs(all_path.targetPath)
        os.makedirs(all_path.allure_results)
    except:
        pass
    # --reruns = 3  失败重试
    # --env=dev     执行环境 会存储到提取参数池里面,dev 对应config.yaml 中的server.dev
    # pytest测试框架主程序运行
    pytest.main([os.path.join(all_path.base_path, "test_cases"), '-vs', '-W','ignore:Module already imported:pytest.PytestWarning', "--env={}".format(env),"--reruns=3", "--alluredir", all_path.allure_results])



    # 拷贝 环境配置文件
    # copy(all_path.environmentPath, os.path.join(all_path.allure_results, 'environment.properties'))

    # 生成allure的html报告
    allure_html = 'allure generate {} -o {} --clean'.format(all_path.allure_results, all_path.reportsPath)
    subprocess.call(allure_html, shell=True)





if __name__ == '__main__':
    run(env)
