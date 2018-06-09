
# ajax 请求
class AjaxResponse:
    success =False;
    msg = None;
    result = None;
    response = None;
    request = None;

    def toDict(self):
        dict = {};
        dict['success'] = self.success
        dict['msg'] = self.msg
        dict['result'] = self.result
        return dict;

class CommonMethodResult:
    success = False;
    msg = None;
    result = None;

    def toDict(self):
        dict = {};
        dict['success'] = self.success
        dict['msg'] = self.msg
        dict['result'] = self.result
        return dict;

