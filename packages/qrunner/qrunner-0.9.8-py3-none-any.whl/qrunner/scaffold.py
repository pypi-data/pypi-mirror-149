import os.path
import sys

api_run_content = """
import qrunner


if __name__ == '__main__':
    base_url = 'https://www.qizhidao.com'
    qrunner.main(
        case_path='test_dir',
        platform='api',
        base_url=base_url,
    )
"""

android_run_content = """
import qrunner


if __name__ == '__main__':
    qrunner.main(
        case_path = 'test_dir',
        platform='android',
        serial_no='UJK0220521066836',
        pkg_name='com.qizhidao.clientapp'
    )
"""

ios_run_content = """
import qrunner


if __name__ == '__main__':
    qrunner.main(
        case_path = 'test_dir',
        platform='ios',
        serial_no='00008101-000E646A3C29003A',
        pkg_name='com.qizhidao.company'
    )
"""

browser_run_content = """
import qrunner


if __name__ == '__main__':
    qrunner.main(
        case_path = 'test_dir',
        platform='browser',
        browser_name='chrome'
    )
"""

case_content_not_api = """
from qrunner import TestCase


class TestUiSample(TestCase):
    def test_go_my(self):
        self.click(resourceId='id/bottom_btn')
        self.click(resourceId='id/bottom_view', index=3)
        self.assertExist(text='我的订单')
        self.screenshot('test.png')
"""

case_content_api = """
from qrunner import TestCase, file_data


class TestApiSample(TestCase):

    @file_data('card_type', 'data.json')
    def test_getToolCardListForPc(self, card_type):
        path = '/api/qzd-bff-app/qzd/v1/home/getToolCardListForPc'
        pay_load = {"type": card_type}
        self.post(path, json=pay_load)
        self.assertCode(0)
"""

require_content = """qrunner
"""

ignore_content = "\n".join(
    ["__pycache__/*", "*.pyc", ".idea/*", ".DS_Store", "allure-results"]
)

data_content = """
{
  "card_type": [0, 1, 2]
}
"""


def init_scaffold_project(subparsers):
    parser = subparsers.add_parser("create", help="Create a new project with template structure.")
    parser.add_argument('-n', '--name', dest='name', type=str, default='my_pro', help='Specify new project name.')
    parser.add_argument('-t', '--platform', dest='platform', type=str, default='api', help='测试平台: api、android、ios、browser')
    return parser


def create_scaffold(project_name, platform):
    """ create scaffold with specified project name.
    """

    def create_folder(path):
        os.makedirs(path)
        msg = f"created folder: {path}"
        print(msg)

    def create_file(path, file_content=""):
        with open(path, "w", encoding="utf-8") as f:
            f.write(file_content)
        msg = f"created file: {path}"
        print(msg)

    create_folder(project_name)
    create_file(
        os.path.join(project_name, ".gitignore"),
        ignore_content,
    )
    create_file(
        os.path.join(project_name, "requirements.txt"),
        require_content,
    )
    create_folder(os.path.join(project_name, 'test_dir'))
    create_file(
        os.path.join(project_name, 'test_dir', "__init__.py"),
        '',
    )
    if platform == 'api':
        create_file(
            os.path.join(project_name, "run.py"),
            api_run_content,
        )
        create_file(
            os.path.join(project_name, 'test_dir', "test_api_sample.py"),
            case_content_api,
        )
    elif platform == 'android':
        create_file(
            os.path.join(project_name, "run.py"),
            android_run_content,
        )
        create_file(
            os.path.join(project_name, 'test_dir', "test_api_sample.py"),
            case_content_not_api,
        )
    elif platform == 'ios':
        create_file(
            os.path.join(project_name, "run.py"),
            ios_run_content,
        )
        create_file(
            os.path.join(project_name, 'test_dir', "test_api_sample.py"),
            case_content_not_api,
        )
    elif platform == 'browser':
        create_file(
            os.path.join(project_name, "run.py"),
            browser_run_content,
        )
        create_file(
            os.path.join(project_name, 'test_dir', "test_api_sample.py"),
            case_content_not_api,
        )
    else:
        print(f'不支持的平台: {platform}')
        sys.exit()
    create_folder(os.path.join(project_name, 'test_data'))
    create_file(
        os.path.join(project_name, 'test_data', "data.json"),
        data_content,
    )
    create_folder(os.path.join(project_name, 'report'))
    return 0


def main_scaffold_project(args):
    sys.exit(create_scaffold(args.name, args.platform))

