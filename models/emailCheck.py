from config.database import db
#----------obteniedo el email de la empresa---------
def getEmail_1(email):
    cursor = db.cursor(dictionary=True)
    cursor.execute('select * from users where email = %s', (email,))
    email=cursor.fetchall()
    return email
#-------------------
def getEmail_2(email):
    cursor = db.cursor()
    cursor.execute('select * from users where email = %s', (email,)) 
    email=cursor.fetchone()
    return email
#-------------------
def getEmail_3(email):
    cursor = db.cursor()
    cursor =db.cursor(dictionary=True)
    cursor.execute("select * from users where status = 1 and email = %s", (email,)) 
    email=cursor.fetchone()
    return email

