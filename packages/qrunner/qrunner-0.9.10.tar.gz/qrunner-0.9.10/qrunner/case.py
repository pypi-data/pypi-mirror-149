import sys
import typing
import allure
from qrunner.utils.log import logger
from qrunner.utils.config import conf
from qrunner.core.android.driver import AndroidDriver
from qrunner.core.android.element import AndroidElement
from qrunner.core.ios.driver import IosDriver
from qrunner.core.ios.element import IosElement
from qrunner.core.browser.driver import BrowserDriver
from qrunner.core.browser.element import WebElement
from qrunner.core.api.request import HttpRequest, ResponseResult
import jmespath
# from jsonschema import validate
# from jsonschema.exceptions import ValidationError


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
        # 初始化driver
        logger.info('初始化driver')
        # 从配置文件中获取浏览器相关配置（为了支持并发执行）
        platform = conf.get_name('common', 'platform')
        serial_no = conf.get_name('app', 'serial_no')
        browser_name = conf.get_name('web', 'browser_name')

        cls.driver: typing.Union[AndroidDriver, IosDriver, BrowserDriver] = None
        if platform == 'android':
            if serial_no:
                cls.driver = AndroidDriver(serial_no)
            else:
                logger.info('serial_no为空')
                sys.exit()
        elif platform == 'ios':
            if serial_no:
                cls.driver = IosDriver(serial_no)
            else:
                logger.info('serial_no为空')
                sys.exit()
        elif platform == 'browser':
            cls.driver = BrowserDriver(browser_name)
        elif platform == 'api':
            pass
        else:
            logger.info(f'不支持的平台: {platform}')
            sys.exit()
        cls().start_class()

    @classmethod
    def teardown_class(cls):
        logger.info('teardown_class')
        platform = conf.get_name('common', 'platform')
        logger.info(platform)
        if platform == 'browser':
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
        self.platform = conf.get_name('common', 'platform')
        if self.platform in ['android', 'ios']:
            self.driver.force_start_app()
        self.start()

    def teardown_method(self):
        self.end()
        if self.platform in ['android', 'ios']:
            self.driver.stop_app()
        # if self.platform == 'api':
        #     method = ResponseResult.method
        #     path: str = ResponseResult.path
        #     allure.dynamic.title(f'[{method}]{path}')  # 设置用例标题

    # @staticmethod
    # def set_title(text):
    #     """
    #     设置allure报表中对应用例的标题
    #     @param text: 测试用例标题
    #     @return:
    #     """
    #     allure.dynamic.title(text)

    def el(self, **kwargs):
        """
        :param kwargs: 元素定位方式
        :return: 根据平台返回对应的元素
        """
        if self.platform == 'android':
            element = AndroidElement(**kwargs)
        elif self.platform == 'ios':
            element = IosElement(**kwargs)
        elif self.platform == 'browser':
            element = WebElement(self.driver, **kwargs)
        else:
            logger.info(f'不支持的平台: {self.platform}，暂时只支持android、ios、browser')
            sys.exit()
        return element

    def click(self, **kwargs):
        self.el(**kwargs).click()

    def assertExist(self, **kwargs):
        assert self.el(**kwargs).exists(timeout=3)

    def open(self, url, cookies: list = None):
        """
        访问链接为url的页码
        :param url: 页面链接
        :param cookies: 登录相关的cookie，如[
            {'name': 'xxx', 'value': 'xxxx'}
        ]
        :return:
        """
        self.driver.open_url(url)
        if cookies:
            self.driver.add_cookies(cookies)
            self.driver.refresh()

    def screenshot(self, file_name: str):
        """
        截图并存为文件
        :param file_name: 如test.png
        :return:
        """
        if not file_name.endswith('.png'):
            file_name = file_name + '.png'
        self.driver.screenshot(file_name)

    def assertStatusCode(self, status_code):
        """
        Asserts the HTTP status code
        """
        assert ResponseResult.status_code == status_code, \
            f'status_code {ResponseResult} != {status_code}'

    # def assertSchema(self, schema):
    #     """
    #     Assert JSON Schema
    #     doc: https://json-schema.org/
    #     """
    #     try:
    #         validate(instance=ResponseResult.response, schema=schema)
    #     except ValidationError as msg:
    #         assert "Response data" == "Schema data", msg
    #     else:
    #         assert True

    # def assertJSON(self, assert_json):
    #     """
    #     Assert JSON data
    #     """
    #     AssertInfo.data = []
    #     diff_json(ResponseResult.response, assert_json)
    #     if len(AssertInfo.data) == 0:
    #         self.assertTrue(True)
    #     else:
    #         self.assertEqual("Response data", "Assert data", msg=AssertInfo.data)

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
    def __init__(self, driver, url=None):
        """
        :param driver: 驱动句柄
        :param url: 页面链接
        :param cookies: 登录态相关cookies: [
            {'name': 'xxx', 'value': 'xxxx'},
            {'name': 'xxx', 'value': 'xxxx'},
        ]
        """
        self.platform = conf.get_name('common', 'platform')
        self.driver = driver
        if url is not None:
            self.url = url
            self.open(self.url)

    def el(self, **kwargs):
        """
        :param args: 暂时无用
        :param kwargs: 元素定位方式
        :return: 根据平台返回对应的元素
        """
        element: typing.Union[AndroidElement, IosElement, WebElement] = None
        if self.platform == 'android':
            element = AndroidElement(**kwargs)
        elif self.platform == 'ios':
            element = IosElement(**kwargs)
        elif self.platform == 'browser':
            element = WebElement(self.driver, **kwargs)
        else:
            logger.info(f'不支持的平台: {self.platform}，暂时只支持android、ios、browser')
            sys.exit()
        return element

    def open(self, url, cookies: str = None):
        """
        访问链接为url的页码
        :param url: 页面链接
        :@param cookies: 登录相关的cookie，如[
            {'name': 'xxx', 'value': 'xxx'}
        ]
        :return:
        """
        self.driver.open_url(url)
        if cookies:
            self.driver.add_cookies(cookies)
            self.driver.refresh()

    def screenshot(self, file_name):
        """
        截图并存为文件
        :param file_name: 如test.png
        :return:
        """
        if not file_name.endswith('.png'):
            file_name = file_name + '.png'
        self.driver.screenshot(file_name)

    # def allure_shot(self, file_name):
    #     """
    #     截图并上传至allure
    #     :param file_name: 如首页截图
    #     :return:
    #     """
    #     self.driver.upload_pic(file_name)


class H5Page:
    """
    测试页面基类，所有页面需要继承该类
    """
    def __init__(self, driver):
        """
        :param driver: 驱动句柄
        :param url: 页面链接
        :param cookies: 登录态相关cookies: [
            {'name': 'xxx', 'value': 'xxxx'},
            {'name': 'xxx', 'value': 'xxxx'},
        ]
        """
        self.driver = driver

    def el(self, **kwargs):
        """
        :param args: 暂时无用
        :param kwargs: 元素定位方式
        :return: 根据平台返回对应的元素
        """
        element: WebElement = WebElement(self.driver, **kwargs)
        return element

    def open(self, url, cookies: str = None):
        """
        访问链接为url的页码
        :param url: 页面链接
        :@param cookies: 登录相关的cookie，如[
            {'name': 'xxx', 'value': 'xxx'}
        ]
        :return:
        """
        self.driver.open_url(url)
        if cookies:
            self.driver.add_cookies(cookies)
            self.driver.refresh()

    def screenshot(self, file_name):
        """
        截图并存为文件
        :param file_name: 如test.png
        :return:
        """
        if not file_name.endswith('.png'):
            file_name = file_name + '.png'
        self.driver.screenshot(file_name)

    def allure_shot(self, file_name):
        """
        截图并上传至allure
        :param file_name: 如首页截图
        :return:
        """
        self.driver.upload_pic(file_name)
