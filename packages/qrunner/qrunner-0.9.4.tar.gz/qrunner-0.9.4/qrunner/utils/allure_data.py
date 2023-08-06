import inspect
import os.path
import sys

from qrunner import logger


class AllureData:

    @staticmethod
    def get_basic_info(report_name):
        stack_t = inspect.stack()
        ins = inspect.getframeinfo(stack_t[1][0])
        root_dir = os.path.dirname(os.path.abspath(ins.filename))
        parent_dir = os.path.dirname(root_dir)
        parent_parent_dir = os.path.dirname(parent_dir)
        dir_list = [root_dir, parent_dir, parent_parent_dir]
        report_dir = None
        for dir_item in dir_list:
            report_like_dir = os.path.join(dir_item, report_name)
            if os.path.exists(report_like_dir):
                report_dir = report_like_dir
                break

        if report_dir is not None:
            logger.debug(f'找到报告目录: {report_dir}')
        else:
            logger.debug('未找到报告目录')
            sys.exit()

        prometheus_data_path = os.path.join(report_dir, 'export', 'prometheusData.txt')
        with open(prometheus_data_path, 'r') as f:
            lines = f.readlines()
        passed = int(lines[2].strip('\n').split(' ')[1])
        total = int(lines[10].strip('\n').split(' ')[1])
        fail = total - passed
        rate = int((passed / total) * 100)
        return {"total": total, "passed": passed, "rate": rate, "fail": fail}


if __name__ == '__main__':
    print(AllureData.get_basic_info('report'))
