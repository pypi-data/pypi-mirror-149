# @Time    : 2022/2/22 11:32
# @Author  : kang.yang@qizhidao.com
# @File    : run.py
import time
import requests
import qrunner


def get_fingerprint():
    timestamp = time.time()
    app_host = 'https://app-pre.qizhidao.com'
    url = f'{app_host}/confuse/css/font/{timestamp}.css'
    requests.get(url, verify=False)
    return timestamp


if __name__ == '__main__':
    headers = {
        'accessToken': 'eyJhbGciOiJIUzUxMiJ9.ZXlKNmFYQWlPaUpFUlVZaUxDSmhiR2NpT2lKa2FYSWlMQ0psYm1NaU9pSkJNVEk0UTBKRExVaFRNalUySW4wLi5RR05oQWhaWnlwVTBJSVBkMDVpWHpBLlZIeF8wOEhFWVNVZE1pYU5nYnh3dmdBNW1hMTRfa3EzOHNoVlFyR2dOZTJQT1JROXFVcEN5TkswZDBudFlTOWxtSzVWcXFfUDEtYVhhSHRvaFJKckN2RUFXeVA4b0dXXzN5NjB1TmRyeHUyTGtfTmMwY2RGdy1PQWo5b2M5aVQzRnpUcGlBOGxfRENwZnpUa3ZtRUUwb0QzRVFkaUpmM0VnQzU1UHZtWWI5NzlEN2s2R1Q5M0Itc1NHdTZjNVg5Z1ByeGRSTUktQXpaTFllOHFiVi05WXptbDkxenJ5cXJmb1lDOVMwdUNrVmcuS2FUT2RQTnQ2RXdCek5OWUdjb3RyQQ.398_WGQsyrxsqb97EMeTrVIS3B1KEznZmDiVZcdtTUVMcML3FC4KnrmcQLtGxiOSYnv6CvkrF-u2-vas64jc0A',
        'signature': '72ff197401b1ec859a5618bcb0e90a34.1wqJG3H3A6',
        'User-Agent': 'Mozilla/5.0 (iOS; OS/14.6) QZDVName/3.0.2 Device/iPhone XR AppleWebKit/537.36 (KHTML, like Gecko)  Safari/537.36 X/0.29c0c3b080053f818d737a9e8c18822d',
        'Content-Type': 'application/json;charset=UTF-8',
        'Qzd-Fingerprint': get_fingerprint()
    }
    qrunner.main(
        case_path='test_demo.py',
        platform='api',
        base_url='https://app-pre.qizhidao.com',
        headers=headers
    )
