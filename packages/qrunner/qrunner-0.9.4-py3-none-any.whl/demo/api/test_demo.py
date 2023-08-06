# @Time    : 2022/2/22 11:32
# @Author  : kang.yang@qizhidao.com
# @File    : test_demo.py
import qrunner


@qrunner.module('查企业-详情')
class TestIndex(qrunner.TestCase):

    @qrunner.title('分页查询行政许可[size={size}]')
    @qrunner.data('size', [10, 20])
    def test_pageQueryAdminLicense(self, size):
        """分页查询行政许可"""
        path = '/qzd-bff-enterprise/qzd/v4/es/law/app/pageQueryAdminLicense'
        pay_load = {
            'source': 'app',
            'current': 1,
            'pageSize': size,
            'eid': 'f202501d-1254-4832-98dd-5162a669b8f2'
        }
        self.post(path, json=pay_load)

        self.assertStatusCode(200)
        self.assertPath('code', 0)
