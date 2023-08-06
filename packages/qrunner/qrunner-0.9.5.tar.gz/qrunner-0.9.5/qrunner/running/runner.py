# coding=utf-8
import json
import os
import sys
import pytest
from qrunner.utils.log import logger
from qrunner.utils.config import conf


class TestMain(object):
    """
    Support for app and web
    """
    def __init__(self,
                 platform='api',
                 serial_no=None,
                 pkg_name=None,
                 browser_name='chrome',
                 case_path='test_dir',
                 rerun='0',
                 concurrent=False,
                 base_url=None,
                 headers=None,
                 timeout=30,
                 report_path='report'
                 ):
        """
        :param platform: 平台，如browser、android、ios、api
        :param serial_no: 设备id，如UJK0220521066836、00008020-00086434116A002E
        :param pkg_name: 应用包名，如com.qizhidao.clientapp、com.qizhidao.company
        :param browser_name: 浏览器类型，如chrome、其他暂不支持
        :param case_path: 用例路径
        :param rerun: 失败重试次数
        :param concurrent: 是否需要并发执行，只支持platform为browser的情况
        :@param base_url: 接口host
        "@param headers: 额外的请求头，{
            "accessToken": "xxxx",
            "signature": "xxxx"
        }
        :@param timeout: 接口请求超时时间
        :@param report_path: 报告生成目录
        """

        self.platform = platform
        self.serial_no = serial_no
        self.pkg_name = pkg_name
        self.browser_name = browser_name
        self.case_path = case_path
        if isinstance(rerun, int):
            self.rerun = str(rerun)
        self.rerun = rerun
        self.concurrent = concurrent
        self.base_url = base_url
        self.headers = headers
        self.timeout = timeout
        self.report_path = report_path

        # 将数据写入全局变量
        if self.platform is not None:
            conf.set_name('common', 'platform', self.platform)
        if self.serial_no is not None:
            conf.set_name('app', 'serial_no', self.serial_no)
        if self.pkg_name is not None:
            conf.set_name('app', 'pkg_name', self.pkg_name)
        if self.browser_name is not None:
            conf.set_name('web', 'browser_name', self.browser_name)
        if self.base_url is not None:
            conf.set_name('common', 'base_url', self.base_url)
        else:
            if self.platform == 'api' or self.platform == 'browser':
                print('base_url未配置，请配置后重新执行~')
                sys.exit()
        if self.headers is not None:
            conf.set_name('api', 'headers', json.dumps(self.headers))
        if self.timeout is not None:
            conf.set_name('common', 'timeout', self.timeout)
        conf.set('common', 'report_path', self.report_path)

        # 执行用例
        logger.info('执行用例')
        logger.info(f'平台: {self.platform}')
        cmd_list = [
            '-sv',
            '--reruns', self.rerun,
            '--alluredir', 'allure-results', '--clean-alluredir'
        ]
        if self.case_path:
            cmd_list.insert(0, self.case_path)
        if self.concurrent:
            if self.platform == 'browser' or self.platform == 'api':
                cmd_list.insert(1, '-n')
                cmd_list.insert(2, 'auto')
                cmd_list.insert(3, '--dist=loadscope')
            else:
                logger.info(f'{self.platform}平台不支持并发执行')
                sys.exit()
        logger.info(cmd_list)
        pytest.main(cmd_list)

        # 用例完成后操作
        conf.set_name('api', 'headers', json.dumps({}))  # 清除登录态
        os.system(f'allure generate allure-results -o {self.report_path} --clean')  # 生成报告


main = TestMain


if __name__ == '__main__':
    main()

