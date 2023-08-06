

class DatappResponse:

    def __init__(self):
        self.code = 10404
        self.error = 'not found'
        self.text = '资源不存在'

    def ret(self):
        return {
            "code": self.code,
            "error": self.error,
            "text": self.text,
        }

    def success(self):
        self.code = 10000
        self.error = ''
        self.text = ''
        return self.ret()

    def normal_error(self, code, error, text=''):
        self.code = code
        self.error = error
        self.text = text
        return self.ret()

    def miss_args(self):
        self.code = 10420
        self.error = 'miss_args'
        self.text = '缺少参数'
        return self.ret()

    def error_args(self, argv=''):
        self.code = 10421
        self.error = 'error_args, %s' % argv
        self.text = '%s参数不正确' % argv
        return self.ret()

    def error_need_login(self):
        self.code = 10401
        self.error = 'not login'
        self.text = '未登录'
        return self.ret()

    def error_need_relogin(self):
        self.code = 10401
        self.error = 'error_need_login'
        self.text = '需要重新登录'
        return self.ret()

    def page_not_found(self, resource='', code=10404):
        self.code = code
        self.error = 'resource not found'
        self.text = '%s 资源不存在' % resource
        return self.ret()

    def not_know_error(self, error):
        self.code = 10999
        self.error = 'not know error, but have %s' % error
        self.text = '未知的错误'
        return self.ret()

    def no_permission_for_etl(self):
        self.code = 10403
        self.error = 'no_permission_for_etl'
        self.text = '暂无权限进行相关操作'
        return self.ret()

    def server_error(self):
        self.code = 10500
        self.error = 'platform server is error'
        self.text = '平台服务出错'
        return self.ret()
