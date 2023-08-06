import json
from collections import OrderedDict
from typing import Any, Dict, Optional, Tuple

import requests
from requests import Response
from requests.models import RequestEncodingMixin
import datappkit.common.config as config
from datappkit.common.datapp_response import DatappResponse

YUEYING_HOST_DEV = "https://galaxy-api-test.megyueying.com"
YUEYING_HOST_PROD = "https://api.megyueying.com"

# 登录
YUEYING_LOGIN_URI = "/guc/v1/login?type=1&platform_id=20"
# 获取当前用户信息
CURRENT_YUEYING_USER_URI = "/guc/v1/user/current"
# 创建需求
POST_REQUIREMENT_URI = "/requirement/v1/requirements"
# 修改需求
PATCH_REQUIREMENT_URI = "/requirement/v1/requirements/{}"
# 获取需求详情
GET_REQUIREMENT_DETAIL_URI = "/requirement/v1/requirements/{}/detail"
# 获取需求list
GET_REQUIREMENT_URI = "/requirement/v1/requirements?"
# 获取标注类型
GET_LABEL_TYPE_URI = "/requirement/v1/filters?keys=task_type"
# 搜索研究员、费用接口人
SEARCH_EMPLOYEE = "/info/v1/employees/galaxy/query"
# 搜索DPM、需求方成员
SEARCH_GUC_COMPANY_USER = "/guc/v1/company/users"
# 搜索项目经理
SEARCH_PROJECT_USER = "/guc/v1/users"
# 搜索负责人、执行人员
SEARCH_COMPANY_USER = "/company/v1/search_username"
# 根据id获取批次
GET_BATCH = "/requirement/v1/batches/{batchId}"
# 获取批次
GET_BATCHES = "/requirement/v1/batches?"
# 获取批次配置
GET_BATCHES_CONFIG = "/requirement/v1/batches/{batchId}/tool-config"
# 批量修改批次配置
POST_BATCHES_CONFIGS = "/requirement/v1/batches/tool-configs"
# 发布批次
POST_BATCHES_PUBLISH = "/requirement/v1/batches/publish"
# 获取任务信息
GET_LABEL_TASK = "/requirement/v1/batches/{batchId}/preview"

ParamsVar = Dict[str, Any]
BodyVar = Optional[Dict[str, Any]]


class DatappAPIClientException(Exception):
    pass


class DatappAPIServicesException(Exception):
    pass


class DatappAPIUnknownException(Exception):
    pass


class BaseRequest(RequestEncodingMixin):  # noqa: WPS338
    def __init__(self, method: str, uri: str, params: ParamsVar, body: BodyVar = None):  # noqa: WPS110
        self._method = method.upper()
        self._uri = uri
        self.url = self.host() + uri.format(**params)
        self.params = OrderedDict(params)
        self.body = body if body else {}
        self.content = json.dumps(self.body) if self.body else ''

    @property
    def _headers(self):
        headers = {
            'Content-type': 'application/json',
            'Charset': 'utf-8',
        }
        jwt = config.authorization()
        if jwt and "login" not in self._uri:
            headers['Authorization'] = jwt
        return headers

    def host(self):
        host = YUEYING_HOST_DEV if config.debug() else YUEYING_HOST_PROD
        return host

    def request(self) -> Tuple[Any, dict]:
        if not config.authorization() and "login" not in self._uri:
            return DatappResponse().error_need_login(), {}
        res = self._request()
        # if config.debug():
        # if True:
        #     print(f'Base Request | {res.request.method} {res.request.url}')
        #     print(f'Base Request | Headers: {res.request.headers}')
        #     if res.request.body:
        #         print(f'Base Request | Request Body: {json.dumps(json.loads(res.request.body), indent=1)}')  # noqa: WPS221
        #
        #     print(f'Base Request | Response Code: {res.status_code}')
        #     print(f'Base Request | Response Body: {res.text}')

        if res.status_code // 100 == 2:
            if res.status_code == 204:  # noqa: WPS432
                return DatappResponse().success(), {}
            return DatappResponse().success(), res.json()
        try:
            error_msg = res.json()['message']
        except (ValueError, KeyError):
            error_msg = res.text
        code = res.status_code + 10000
        return DatappResponse().normal_error(code, error_msg), {}

    def _request(self) -> Response:
        if self._method in {'GET', 'DELETE', 'HEAD', 'OPTIONS'}:
            return requests.request(self._method, self.url, headers=self._headers, params=self.params)
        elif self._method in {'POST', 'PUT', 'PATCH'}:
            return requests.request(
                self._method,
                self.url,
                headers=self._headers,
                params=self.params,
                data=self.content,
            )

        raise TypeError(f'Not support {self._method} method request.')
