import sys
sys.path.append("/Users/garry/PycharmProjects/data-service-sdk")

from datappkit.common import config
from datappkit.datapp import Datapp


if __name__ == '__main__':
    datapp = Datapp()
    # test jwt
    # config.set_authorization('JWT eyJ0eXBlIjoiSldUIiwiYWxnIjoiUlMyNTYifQ.eyJ1c2VyX2lkIjozNywiaWF0IjoxNjQ5MjE1MjU0LCJleHBpcmVfYXQiOjE2NjczNTkyNTQsImRvbWFpbiI6Im1lZ3l1ZXlpbmcuY29tIiwicGxhdGZvcm1faWQiOjIxfQ.fQXfDbwvpg4N8U_2xoZaLKasi_zmH6uMvSILsEyhhz32tj5mxtlsJvueHZ5fYWbKT5OozLDEe-lHUEUsde8U8iE6nfL1XBFM4HvCbjDskFJt-G6yC2AgV6XEYZAMsOne9ni9kVlKwIG9_mqm1oiv0wE-LLhm732ySYfTf7s9DiDLEV-TLOjLPIkGYKHUN-Oi1XiLOf_gkNlGy4DVWLCh4CRsLZngD5ysz9ZkHj1cE8hqvk1IphwJ4D9a7H_nharumisS2SI4nVpQDr8Za_goIZmJ6KED3oS9WlX3cQPweQ0oX5oSFIyIEd7VVDcusoMp0ykFZYUjH9R_GbLQKaSYoA')
    # config.set_authorization('JWT eyJhbGciOiJSUzI1NiIsInR5cGUiOiJKV1QifQ.eyJ1c2VyX2lkIjoxOCwiaWF0IjoxNjQ5NDE2MjQ4LCJleHBpcmVfYXQiOjE2Njc1NjAyNDgsImRvbWFpbiI6Im1lZ3l1ZXlpbmcuY29tIiwicGxhdGZvcm1faWQiOjIxfQ.uUnPaEO4OLg83GxKSP3kJYyN-pmp_WGsd7lCA5RBo9N7rsB1tnrtoiC5fTfuAp2lrhT6DtYBZxuAfdDheUK6UOACZSXhENDosGhATGd-Su82xWG8bBBi0xjlIRJDaXtL_0TiTUuwwl9VGTz9hLm16t_WDexvFv2rWmwG-9NHWWvUANBGEl4nBVMfkI0APvhyD7kHemOh9rvb7IWFgRcevBF9CoS9qqahmuN7JELmgBMB8KLHo_LFz40Fnl8BnzNvFu_eM5aRPVRVKu9Nhzk7irQd2xsQQglZwYxKFrBbXsQnmOIaNqW39ddknW8x-pqJskfDuzVl6jnMj0Ar-JXvbw')

    # 获取标注类型
    # res, data = datapp.get_label_type()
    # print(res, data)

    # 获取任务信息
    res, data = datapp.get_label_task(1363)
    print(res, data)
