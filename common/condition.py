#存放条件方法在Excel中调用执行
from common.logger import Logger
import pytest
from common.exchange_data import ExchangeData
from _pytest.outcomes import Skipped


class Condition():
    def skip_if(self,case):

        skips=case[6]
        print("current skips is {}".format(skips))
        if skips != "" or skips != True:
            if skips == False:
                Logger.warning('跳过跳过条件：%s' % str(skips))
                pytest.skip('跳过跳过条件：%s'%str(skips))

            else:
                result_list=[]
                for skip in skips.split(';'):
                    skips_srt=ExchangeData.rep_expr(skip,return_type='srt')
                    loc = locals()
                    # exec("sum()")
                    try:
                        Logger.info(skips_srt)
                        exec(f"result = %s" % skips_srt)
                        Logger.info(f"result = %s" % skips_srt)
                        Logger.info(loc['result'])
                        result_list.append(loc['result'])
                    except:
                        result_list.append(True)

                if False in result_list:
                    Logger.warning('跳过跳过条件：%s' % str(skips))
                    pytest.skip('跳过跳过条件：%s' % skips)
        else:
            Logger.info('未发现跳过条件')






