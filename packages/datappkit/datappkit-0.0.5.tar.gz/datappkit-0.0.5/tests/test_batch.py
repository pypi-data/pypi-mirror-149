import sys
sys.path.append("/Users/garry/PycharmProjects/data-service-sdk")

from datappkit.common import config
from datappkit.datapp import Datapp

def create_configs_data():
    return {
        'batch_ids': [1421, 1420],
        'task_config': {
            'attr_config': [
                {
                    "defaultValue": "2",
                    "tmpDefaultValue": ["2"],
                    "icon": "glyphicon-record",
                    "require": True,
                    "type": "radio-v1",
                    "version": "",
                    "hide": False,
                    "readonly": False,
                    "defaultIndex": "config_3",
                    "tmpDefaultIndex": ["config_3"],
                    "isNumber": False,
                    "name": "单选框",
                    "options": [{
                        "color": "#409EFF",
                        "name": "选项名1",
                        "$idx": "config_2",
                        "tip": "",
                        "value": "1"
                    }, {
                        "color": "#67C23A",
                        "name": "选项名2",
                        "$idx": "config_3",
                        "tip": "",
                        "value": "2"
                    }, {
                        "color": "#EB9E05",
                        "name": "选项名3",
                        "$idx": "config_4",
                        "tip": "",
                        "value": "3"
                    }, {
                        "color": "#FA5555",
                        "$idx": "config_5",
                        "name": "选项名43",
                        "value": "43"
                    }]
                }
            ],
            'tool_config': {
                "rect": {
                    "maxnum": 300,
                    "enabled": True,
                    "minnum": 0
                },
                "expanded": True,
                "ruler_config": {
                    "valid": False,
                    "width": 32,
                    "height": 32,
                    "ratio": "fixed"
                },
                "mask": {
                    "maxnum": 300,
                    "enabled": True,
                    "minnum": 0
                }
            },
            "version": "0.1"
        },
        'user_id': '18',
        'platform': 21
    }


if __name__ == '__main__':
    datapp = Datapp()
    # test jwt
    # config.set_authorization('JWT eyJ0eXBlIjoiSldUIiwiYWxnIjoiUlMyNTYifQ.eyJ1c2VyX2lkIjozNywiaWF0IjoxNjQ5MjE1MjU0LCJleHBpcmVfYXQiOjE2NjczNTkyNTQsImRvbWFpbiI6Im1lZ3l1ZXlpbmcuY29tIiwicGxhdGZvcm1faWQiOjIxfQ.fQXfDbwvpg4N8U_2xoZaLKasi_zmH6uMvSILsEyhhz32tj5mxtlsJvueHZ5fYWbKT5OozLDEe-lHUEUsde8U8iE6nfL1XBFM4HvCbjDskFJt-G6yC2AgV6XEYZAMsOne9ni9kVlKwIG9_mqm1oiv0wE-LLhm732ySYfTf7s9DiDLEV-TLOjLPIkGYKHUN-Oi1XiLOf_gkNlGy4DVWLCh4CRsLZngD5ysz9ZkHj1cE8hqvk1IphwJ4D9a7H_nharumisS2SI4nVpQDr8Za_goIZmJ6KED3oS9WlX3cQPweQ0oX5oSFIyIEd7VVDcusoMp0ykFZYUjH9R_GbLQKaSYoA')
    # config.set_authorization('JWT eyJhbGciOiJSUzI1NiIsInR5cGUiOiJKV1QifQ.eyJ1c2VyX2lkIjoxOCwiaWF0IjoxNjQ5NDE2MjQ4LCJleHBpcmVfYXQiOjE2Njc1NjAyNDgsImRvbWFpbiI6Im1lZ3l1ZXlpbmcuY29tIiwicGxhdGZvcm1faWQiOjIxfQ.uUnPaEO4OLg83GxKSP3kJYyN-pmp_WGsd7lCA5RBo9N7rsB1tnrtoiC5fTfuAp2lrhT6DtYBZxuAfdDheUK6UOACZSXhENDosGhATGd-Su82xWG8bBBi0xjlIRJDaXtL_0TiTUuwwl9VGTz9hLm16t_WDexvFv2rWmwG-9NHWWvUANBGEl4nBVMfkI0APvhyD7kHemOh9rvb7IWFgRcevBF9CoS9qqahmuN7JELmgBMB8KLHo_LFz40Fnl8BnzNvFu_eM5aRPVRVKu9Nhzk7irQd2xsQQglZwYxKFrBbXsQnmOIaNqW39ddknW8x-pqJskfDuzVl6jnMj0Ar-JXvbw')

    # 根据id获取批次
    # res, data = datapp.get_batch(1420)

    # 获取批次
    # res, data = datapp.get_batches("1337")

    # 获取批次配置
    # res, data = datapp.get_batches_config(1369)

    # 发布批次
    # res, data = datapp.publish_batches([1337])

    # 修改批次配置
    res, data = datapp.configs_batches(create_configs_data())

    print(res, data)
