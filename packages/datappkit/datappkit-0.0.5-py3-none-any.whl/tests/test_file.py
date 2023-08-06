import sys
sys.path.append("/Users/baojiarui/PycharmProjects/data-service-sdk")

from datappkit.datapp import Datapp


if __name__ == '__main__':
    datapp = Datapp()

    file_path = datapp.download_cli(1, "/Users/baojiarui/Downloads")
    print(file_path)

