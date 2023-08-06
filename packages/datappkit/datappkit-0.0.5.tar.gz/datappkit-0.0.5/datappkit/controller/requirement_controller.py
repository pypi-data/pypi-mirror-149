from datappkit.services.requirement_service import RequirementService


class RequirementController:

    def __init__(self):
        self.service = RequirementService()

    def create(self, data):
        return self.service.create(data)

    def patch(self, data):
        return self.service.patch(data)

    def get_detail(self, requirement_id):
        return self.service.get(requirement_id)

    def get_list(self, page, per_page):
        return self.service.get_list(page, per_page)
