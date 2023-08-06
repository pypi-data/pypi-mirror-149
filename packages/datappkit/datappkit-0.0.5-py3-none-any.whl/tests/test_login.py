import sys
sys.path.append("/Users/garry/PycharmProjects/data-service-sdk")

from datappkit.datapp import Datapp


if __name__ == '__main__':
    datapp = Datapp()
    # test account
    # res, data = datapp.login("13333330003", "test123")
    res, data = datapp.login("17610188166", "test123")

    # res, data = datapp.login("18610928883", "21151091321197")
    # res, data = datapp.login("15185055472", "megviiHEXIN02000000")
    print(res, data)