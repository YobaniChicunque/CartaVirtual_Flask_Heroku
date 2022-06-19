from config.database import db

def updatePassword_(email, passwordn):
    cursor = db.cursor()
    cursor.execute("UPDATE users SET password='"+passwordn+"' where email='"+email+"'")
    cursor.close()
