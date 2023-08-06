import base64
import pyotp


if __name__ == '__main__':
    topt_secret = 'SMP3WCXJJFUBTB4U'
    secretKey = base64.b32encode(topt_secret.encode(encoding="utf-8"))
    totp = pyotp.TOTP(topt_secret)
    print(totp.now())