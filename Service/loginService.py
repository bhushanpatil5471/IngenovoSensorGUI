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
    # print(encPassword)
    # print(decPassword)
    return decPassword


def loginAuth(userName, password):
    userDetails = users.userDetails.get(userName)
    # encpass=encryptPassword(password.zfill(16))
    encpass=encryptPassword(password)
    decpass=decryptPassword(encpass)

    if (userDetails == password):
        return {'status': 200, 'message': 'Login Successful'}

    else:
        return {'status': 500, 'message': 'Login Failure'}

