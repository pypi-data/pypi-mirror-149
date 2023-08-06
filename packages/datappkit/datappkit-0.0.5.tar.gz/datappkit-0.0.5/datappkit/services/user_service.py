from datappkit.common import config
from datappkit.common.datapp_response import DatappResponse
from datappkit.services.base_request import BaseRequest, CURRENT_YUEYING_USER_URI, YUEYING_LOGIN_URI, SEARCH_EMPLOYEE, \
    SEARCH_GUC_COMPANY_USER, SEARCH_PROJECT_USER, SEARCH_COMPANY_USER


class UserService:

    def login(self, account, password):
        body = {'account': account, 'password': password}
        res, data = BaseRequest('POST', YUEYING_LOGIN_URI, {}, body=body).request()
        if res['code'] == 10000:
            config.set_authorization("JWT {}".format(data['jwt']))
        return res, data

    def search_user(self, search, role):
        # 1研究员、2DPM、3费用接口人、4需求方成员、5项目经理、6执行人员
        users = []
        if role in (0, 1, 3):
            params = {
                "origin": 2,
                "name": search
            }
            res, data = BaseRequest('GET', SEARCH_EMPLOYEE, params).request()
            if res['code'] == 10000:
                for item in data:
                    users.append({
                        "user_id": item['employeeId'],
                        "user_name": item['name'],
                        "user_account": item['username'],
                        "department_id": item['departmentId']
                    })
        elif role in (2, 4):
            params = {
                "search": search,
                "platforms": "21,20",
                "per_page": 100,
            }
            res, data = BaseRequest('GET', SEARCH_GUC_COMPANY_USER, params).request()
            users = self._dpmuser_request(res, data)
        elif role == 5:
            params = {
                "search": search,
                "per_page": 100,
            }
            res, data = BaseRequest('GET', SEARCH_PROJECT_USER, params).request()
            users = self._dpmuser_request(res, data)
        else:
            res = DatappResponse().error_args("role")
        return res, users

    def current_user(self):
        return BaseRequest('GET', CURRENT_YUEYING_USER_URI, {}).request()

    def _dpmuser_request(self, res, data):
        users = []
        if res['code'] == 10000:
            for item in data['items']:
                users.append({
                    "user_id": item['user_id'],
                    "user_name": item['username'],
                    "user_account": item['username'],
                    "department_id": 0
                })
        return users
