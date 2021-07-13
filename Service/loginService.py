from Constants import users,Current_token

import rsa
from Utils import NewAccessToken as accessTkn


publicKey, privateKey = rsa.newkeys(512)


def encryptPassword(password):
    encPassword = rsa.encrypt(password.encode(), publicKey)
    # print(password)
    # print(encPassword)
    return encPassword


def decryptPassword(encPassword):
    decPassword = rsa.decrypt(encPassword, privateKey).decode()

    return decPassword


def loginAuth(userName, password):
    userEncPass = users.userDetails.get(userName)
    # encpass=encryptPassword(password.zfill(16))
    encpass = encryptPassword(password)
    decpass = decryptPassword(encpass)

    # print(password)
    # print(encpass)
    # print(decpass)
    if password == decpass:
        access_token = accessTkn.get_access_token()
        Current_token.curtoken.clear()
        Current_token.curtoken={'token':access_token}

        return {'status': 200, 'message': 'Login Successful', 'access_token': access_token}

    else:
        return {'status': 500, 'message': 'Login Failure'}
