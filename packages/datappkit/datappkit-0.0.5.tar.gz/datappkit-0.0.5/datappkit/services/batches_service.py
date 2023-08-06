from datappkit.services.base_request import BaseRequest, GET_BATCHES, POST_BATCHES_PUBLISH, GET_BATCHES_CONFIG, \
    GET_BATCH, POST_BATCHES_CONFIGS


class BatchesService:

    def get_batch(self, batch_id):
        uri = GET_BATCH.format(batchId=batch_id)
        res, data = BaseRequest('GET', uri, {}).request()
        re_data = {}
        if res['code'] == 10000:
            re_data = {
                'id': data['id'],
                'name': data['name'],
                'state': data['state'],
                'state_desc': data['state_desc'],
                'label_type_id': data['task_type_id'],
            }
        return res, re_data

    def get_batches(self, search, page, per_page):
        params = {
            "page": page,
            "per_page": per_page
        }
        if search:
            params['search'] = search
        res, data = BaseRequest('GET', GET_BATCHES, params).request()
        re_list = []
        if res['code'] == 10000:
            for item in data['items']:
                re_list.append({
                    'id': item['id'],
                    'name': item['name'],
                    'state': item['state'],
                    'state_desc': item['state_desc'],
                    'label_type_id': item['task_type_id'],
                })
        return res, {'pagination': data['pagination'], 'items': re_list}

    def get_batches_config(self, batch_id):
        uri = GET_BATCHES_CONFIG.format(batchId=batch_id)
        return BaseRequest('GET', uri, {}).request()

    def publish_batches(self, batch_ids):
        body = {
            "batch_ids": batch_ids
        }
        return BaseRequest('POST', POST_BATCHES_PUBLISH, {}, body=body).request()

    def configs_batches(self, config):
        return BaseRequest('POST', POST_BATCHES_CONFIGS, {}, body=config).request()
