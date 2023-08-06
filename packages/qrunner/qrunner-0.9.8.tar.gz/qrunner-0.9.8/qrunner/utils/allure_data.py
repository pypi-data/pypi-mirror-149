import os.path


class AllureData:

    def __init__(self, report_path):
        self.report_path = report_path

    def get_basic_info(self):
        prometheus_data_path = os.path.join(self.report_path, 'export', 'prometheusData.txt')
        with open(prometheus_data_path, 'r') as f:
            lines = f.readlines()
        passed = int(lines[2].strip('\n').split(' ')[1])
        total = int(lines[10].strip('\n').split(' ')[1])
        fail = total - passed
        rate = int((passed / total) * 100)
        return {"total": total, "passed": passed, "rate": rate, "fail": fail}

