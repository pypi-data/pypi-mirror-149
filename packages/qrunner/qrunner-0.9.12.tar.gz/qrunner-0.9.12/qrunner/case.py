import sys
import jmespath
from qrunner.core.api.request import HttpRequest, ResponseResult
from qrunner.core.android.driver import AndroidDriver
from qrunner.core.android.element import AndroidElement
from qrunner.core.ios.driver import IosDriver
from qrunner.core.ios.element import IosElement
from qrunner.core.browser.driver import BrowserDriver
from qrunner.core.browser.element import WebElement
from qrunner.utils.log import logger
from qrunner.utils.config import conf


class TestCase(HttpRequest):
    """
    测试用例基类，所有测试用例需要继承该类
    """
    def start_class(self):
        """
        Hook method for setup_class fixture
        :return:
        """
        pass

    def end_class(self):
        """
        Hook method for teardown_class fixture
        :return:
        """
        pass

    @classmethod
    def setup_class(cls):
        # 从配置文件中获取浏览器相关配置（为了支持并发执行）
        platform = conf.get_name('common', 'platform')
        serial_no = conf.get_name('app', 'serial_no')
        pkg_name = conf.get_name('app', 'pkg_name')
        browser_name = conf.get_name('web', 'browser_name')

        # 初始化driver
        if platform == 'android':
            logger.info('初始化 安卓 driver')
            if serial_no:
                cls.driver = AndroidDriver(serial_no, pkg_name)
            else:
                logger.info('serial_no为空')
                sys.exit()
        elif platform == 'ios':
            logger.info('初始化 IOS driver')
            if serial_no:
                cls.driver = IosDriver(serial_no, pkg_name)
            else:
                logger.info('serial_no为空')
                sys.exit()
        elif platform == 'browser':
            logger.info('初始化 Selenium driver')
            cls.driver = BrowserDriver(browser_name)
        elif platform == 'api':
            pass
        else:
            logger.info(f'不支持的平台: {platform}')
            sys.exit()
        cls().start_class()

    @classmethod
    def teardown_class(cls):
        # 关闭浏览器
        if isinstance(cls().driver, BrowserDriver):
            cls().driver.quit()
        cls().end_class()

    def start(self):
        """
        Hook method for setup_method fixture
        :return:
        """
        pass

    def end(self):
        """
        Hook method for teardown_method fixture
        :return:
        """
        pass

    def setup_method(self):
        # 启动应用
        if isinstance(self.driver, AndroidDriver) or isinstance(self.driver, IosDriver):
            self.driver.force_start_app()
        self.start()

    def teardown_method(self):
        self.end()
        # 退出应用
        if isinstance(self.driver, AndroidDriver) or isinstance(self.driver, IosDriver):
            self.driver.stop_app()

    def e(self, **kwargs):
        """
        根据
        :param kwargs: 元素定位方式
        :return: 根据平台返回对应的元素
        """
        if isinstance(self.driver, AndroidDriver):
            element = AndroidElement(self.driver, **kwargs)
        elif isinstance(self.driver, IosDriver):
            element = IosElement(self.driver, **kwargs)
        elif isinstance(self.driver, BrowserDriver):
            element = WebElement(self.driver, **kwargs)
        else:
            platform = conf.get('common', 'platform')
            logger.info(f'不支持的平台: {platform}，暂时只支持android、ios、browser')
            sys.exit()
        return element

    def assertStatusCode(self, status_code):
        """
        Asserts the HTTP status code
        """
        assert ResponseResult.status_code == status_code, \
            f'status_code {ResponseResult} != {status_code}'

    def assertPath(self, path, value):
        """
        Assert path data
        doc: https://jmespath.org/
        """
        search_value = jmespath.search(path, ResponseResult.response)
        assert search_value == value, f'{search_value} != {value}'

    def assertLocalPath(self, path, value, json_obj):
        """
        同assertPath，只是源数据不是请求响应，而是传入的json_ojb
        @param path:
        @param value:
        @param json_obj:
        @return:
        """
        search_value = jmespath.search(path, json_obj)
        assert search_value == value, f'{search_value} != {value}'

    def assertLenEq(self, path, value):
        """
        断言列表长度等于多少
        doc: https://jmespath.org/
        """
        search_value = jmespath.search(path, ResponseResult.response)
        assert len(search_value) == value, f"{search_value} 的长度不等于 {value}"

    def assertLenGt(self, path, value):
        """
        断言列表长度大于多少
        doc: https://jmespath.org/
        """
        search_value = jmespath.search(path, ResponseResult.response)
        assert len(search_value) > value, f"{search_value} 的长度不大于 {value}"

    def assertGt(self, path, value):
        """
        值大于多少
        :param path:
        :param value:
        :return:
        """
        search_value = jmespath.search(path, ResponseResult.response)
        if isinstance(search_value, str):
            search_value = int(search_value)
        assert search_value > value, f"{search_value} 不大于 {value}"

    def assertGe(self, path, value):
        """
        值大于等于
        :param path:
        :param value:
        :return:
        """
        search_value = jmespath.search(path, ResponseResult.response)
        if isinstance(search_value, str):
            search_value = int(search_value)
        assert search_value >= value, f"{search_value} 小于 {value}"

    def assertNotEq(self, path, value):
        """值不等于"""
        search_value = jmespath.search(path, ResponseResult.response)
        assert search_value != value, f"{search_value} 等于 {value}"

    def assertIn(self, path, value_list: list):
        """
        断言匹配结果被value_list包含
        @param path:
        @param value_list:
        @return:
        """
        search_value = jmespath.search(path, ResponseResult.response)
        assert search_value in value_list, f"{value_list} 不包含 {search_value}"

    def assertContains(self, path, value):
        """
        断言匹配结果包含value
        @param path:
        @param value:
        @return:
        """
        search_value = jmespath.search(path, ResponseResult.response)
        assert value in search_value, f"{search_value} 不包含 {value}"

    def assertType(self, path, value_type):
        if not isinstance(value_type, type):
            if value_type == 'int':
                value_type = int
            elif value_type == 'str':
                value_type = str
            elif value_type == 'list':
                value_type = list
            elif value_type == 'dict':
                value_type = dict
            else:
                value_type = str

        search_value = jmespath.search(path, ResponseResult.response)
        assert isinstance(search_value, value_type), f'{search_value} 不是 {value_type} 类型'

    def assertCode(self, code):
        """
        断言返回json中的code
        @param code: 0
        @return:
        """
        self.assertPath('code', code)


class Page:
    """
    测试页面基类，所有页面需要继承该类
    """
    def __init__(self, driver):
        """
        :param driver: 驱动句柄
        """
        self.driver = driver

    def e(self, **kwargs):
        """
        根据
        :param kwargs: 元素定位方式
        :return: 根据平台返回对应的元素
        """
        if isinstance(self.driver, AndroidDriver):
            element = AndroidElement(self.driver, **kwargs)
        elif isinstance(self.driver, IosDriver):
            element = IosElement(self.driver, **kwargs)
        elif isinstance(self.driver, BrowserDriver):
            element = WebElement(self.driver, **kwargs)
        else:
            platform = conf.get('common', 'platform')
            logger.info(f'不支持的平台: {platform}，暂时只支持android、ios、browser')
            sys.exit()
        return element
