import sys
sys.path.append("/Users/garry/PycharmProjects/data-service-sdk")

from datappkit.common import config
from datappkit.datapp import Datapp


def create():
    """
    test 创建需求
    """
    body = {
        "name": "sdk_test_0410a",
        "researcher_id": "100793",
        "researcher_department_id": "S461",
        "security_level": 3,
        "label_type_id": 1000,
        "estimated_count": 50,
        "description": "",
        "start_time": 1649174400,
        "end_time": 1683648000,
        "data_type_id": 0,
        "payer_list": [
            {
                "employee_id": "100793",
                "rate": 30,
                "payer_department_id": "S461",
            },
            {
                "employee_id": "101608",
                "rate": 70,
                "payer_department_id": "S461",
            }
        ],
    }
    res, data = datapp.create_requirement(body)
    print(res, data)


def patch():
    """
    test 修改需求
    """
    body = {
        "id": 1079,
        "name": "sdk_test_0406b_update1",
        "payer_list": [
            {
                "employee_id": "100793",
                "rate": 30,
                "payer_department_id": "S461",
            },
            {
                "employee_id": "101608",
                "rate": 70,
                "payer_department_id": "S461",
            }
        ],
    }
    res, data = datapp.update_requirement(body)
    print(res, data)


if __name__ == '__main__':
    datapp = Datapp()
    # test jwt
    # config.set_authorization('JWT eyJ0eXBlIjoiSldUIiwiYWxnIjoiUlMyNTYifQ.eyJ1c2VyX2lkIjozNywiaWF0IjoxNjQ5MjE1MjU0LCJleHBpcmVfYXQiOjE2NjczNTkyNTQsImRvbWFpbiI6Im1lZ3l1ZXlpbmcuY29tIiwicGxhdGZvcm1faWQiOjIxfQ.fQXfDbwvpg4N8U_2xoZaLKasi_zmH6uMvSILsEyhhz32tj5mxtlsJvueHZ5fYWbKT5OozLDEe-lHUEUsde8U8iE6nfL1XBFM4HvCbjDskFJt-G6yC2AgV6XEYZAMsOne9ni9kVlKwIG9_mqm1oiv0wE-LLhm732ySYfTf7s9DiDLEV-TLOjLPIkGYKHUN-Oi1XiLOf_gkNlGy4DVWLCh4CRsLZngD5ysz9ZkHj1cE8hqvk1IphwJ4D9a7H_nharumisS2SI4nVpQDr8Za_goIZmJ6KED3oS9WlX3cQPweQ0oX5oSFIyIEd7VVDcusoMp0ykFZYUjH9R_GbLQKaSYoA')
    # datapp.login("13333330003", "test123")

    # 创建需求
    # create()

    # 获取需求详情
    # res, data = datapp.get_requirement(1079)
    # print(res, data)

    # 修改需求
    # patch()

    # 获取需求list
    res, data = datapp.get_requirements(1, 1)
    print(res, data)
