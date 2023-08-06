from datappkit.services.file_service import FileService


class FileController:

    def __init__(self):
        self.service = FileService()

    def download_cli(self, cli_type, target_path):
        return self.service.download_cli(cli_type, target_path)
