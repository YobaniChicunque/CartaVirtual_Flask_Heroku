from hashlib import md5

def encryptPassword(password):
  return md5(password.encode("utf-8")).hexdigest()

