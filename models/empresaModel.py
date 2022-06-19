from config.database import db

def insertCompany(name, description, image, phone, address, email, password):
    cursor= db.cursor()
    cursor.execute("INSERT INTO users (name, description, image, phone, address, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s)", (name, description, image, phone, address, email, password,))
    cursor.close()

def insertProduct(nombre, precio, imagen, usuario_id):
    cursor= db.cursor()
    cursor.execute("INSERT INTO productos (nombre, precio, imagen, usuario_id) VALUES (%s, %s, %s,%s)", (nombre, precio, imagen, usuario_id,))
    cursor.close()


def obtenerProductos(usuario_id):
    cursor = db.cursor(dictionary = True)
    cursor.execute("select * from productos where usuario_id =%s ",(usuario_id,))
    productos = cursor.fetchall() 
    print(productos)
    cursor.close()
    return productos

def actualizarRegistro(name, description, image, phone, address, email, password, id):
    cursor = db.cursor()
    cursor.execute("UPDATE users SET  name = %s, description = %s,   image =%s, phone = %s, address = %s, email = %s,  password = %s WHERE id = %s", 
        (name, 
        description,
        image,
        phone,
        address,
        email,
        password,
        id,
        )) 
    
    cursor.close()


def mostrarRegistro():
    cursor = db.cursor(dictionary = True)
    cursor.execute("select * from users")
    usuarios = cursor.fetchall()
    print(usuarios)
    cursor.close()
    return usuarios
