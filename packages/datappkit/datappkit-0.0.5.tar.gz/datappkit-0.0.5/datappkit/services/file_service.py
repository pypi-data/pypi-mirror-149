import os
import time

import requests


class FileService:

    def download_cli(self, cli_type, target_path):
        if cli_type == 1:
            url = "https://data-galaxy-public.oss-cn-beijing.aliyuncs.com/download/label-cli"
            filename = "zzcrowd-cli"
        elif cli_type == 2:
            url = "https://data-galaxy-public.oss-cn-beijing.aliyuncs.com/download/label-cli"
            filename = "label-cli"
        elif cli_type == 3:
            url = "https://data-galaxy-public.oss-cn-beijing.aliyuncs.com/download/label-cli-mac"
            filename = "label-cli-mac"
        else:
            return "not supported"
        file_path = self._download(url, target_path, filename)
        return {"file_path": file_path}

    def _download(self, url, path, filename):
        if not os.path.exists(path):
            os.mkdir(path)
        start = time.time()
        response = requests.get(url, stream=True)
        size = 0
        chunk_size = 1024
        content_size = int(response.headers['content-length'])
        filepath = path + '/' + filename
        try:
            if response.status_code == 200:
                print('Start download,[File size]:{size:.2f} MB'.format(size=content_size / chunk_size / 1024))
                with open(filepath, 'wb') as file:
                    for data in response.iter_content(chunk_size=chunk_size):
                        file.write(data)
                        size += len(data)
                        print('\r' + '[下载进度]:%s%.2f%%' % ('>' * int(size * 50 / content_size), float(size / content_size * 100)), end=' ')
            end = time.time()
            print('Download completed!,times: %.2f秒' % (end - start))
        except Exception as e:
            print('Error!', e)
        return filepath
