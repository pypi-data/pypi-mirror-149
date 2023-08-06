from datappkit.services.label_service import LabelService


class LabelController:

    def __init__(self):
        self.service = LabelService()

    def get_label_type(self):
        return self.service.get_label_type()

    def get_label_task(self, batch_id):
        return self.service.get_label_task(batch_id)
