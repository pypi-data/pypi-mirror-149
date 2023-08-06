from datappkit.services.base_request import BaseRequest, GET_LABEL_TYPE_URI, GET_LABEL_TASK


class LabelService:

    def get_label_type(self):
        res, data = BaseRequest('GET', GET_LABEL_TYPE_URI, {}).request()
        type_list = []
        if res['code'] == 10000:
            for item in data['items']:
                if item['key'] == "task_type_id":
                    for label_type in item['options']:
                        if label_type['value']:
                            type_list.append({"id": label_type['value'], "name": label_type['text']})
        return res, type_list

    def get_label_task(self, batch_id):
        uri = GET_LABEL_TASK.format(batchId=batch_id)
        res, data = BaseRequest('GET', uri, {}).request()
        redata = {}
        if res['code'] == 10000:
            redata = {
                "task_id": data['data']['id'],
                "state": data['data']['task_info']['state'],
                "state_desc": data['data']['task_info']['state_desc'],
            }
        return res, redata
