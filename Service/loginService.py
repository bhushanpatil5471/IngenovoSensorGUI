from Constants import users
import rsa

publicKey, privateKey = rsa.newkeys(512)


def encryptPassword(password):
    encPassword = rsa.encrypt(password.encode(),publicKey)
    # print(password)
    # print(encPassword)
    return encPassword


def decryptPassword(encPassword):

    decPassword = rsa.decrypt(encPassword, privateKey).decode()

    return decPassword


def loginAuth(userName, password):
    userEncPass = users.userDetails.get(userName)
    # encpass=encryptPassword(password.zfill(16))
    encpass=encryptPassword(password)
    decpass=decryptPassword(encpass)

    # print(password)
    # print(encpass)
    # print(decpass)
    if password == decpass:
        return {'status': 200, 'message': 'Login Successful'}

    else:
        return {'status': 500, 'message': 'Login Failure'}

