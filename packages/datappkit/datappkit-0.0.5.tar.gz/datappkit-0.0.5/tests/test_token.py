import rsa

import base64
import json
from datetime import datetime


def make_jwt():
    header = {'type': 'JWT',
              'alg': 'RS256'
              }

    header = base64.b64encode(json.dumps(header).encode()).decode() # encode  decode 默认使用utf-8
    # print(header)

    # JwtExpiration = int(30 * 7 * 24 * 3600)
    # nowTimeStamp = int(datetime.now().timestamp())
    payload = {
        "user_id": 37, # prod 4792
        "iat": 1649215254,
        "expire_at": 1667359254,
        'domain': "megyueying.com",
        'platform_id': 21
    }
    payload = base64.b64encode(json.dumps(payload).encode()).decode()
    # print(payload)
    signature = genrate_signature(2048, '{header}.{payload}'.format(header=header, payload=payload).encode('utf-8'), 'SHA-256')
    # print(signature)

    return '{header}.{payload}.{signature}'.format(header=header,
                                                      payload=payload,
                                                      signature=signature)


def genrate_signature(nbits, message, hash_method):
    (pubkey, privkey) = rsa.newkeys(nbits)
    # privkey = "s.GXjjIF7rLW0r1GvxIKDmYeKF"
    if not isinstance(message, bytes):
        message = message.encode('utf-8')
    hash = rsa.compute_hash(message, hash_method)
    return base64.b64encode(rsa.sign(hash, privkey, hash_method)).decode()


if __name__ == '__main__':
    print(make_jwt())