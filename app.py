from flask import Flask, render_template, request, redirect, url_for, flash, session
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from email.message import EmailMessage
from smtplib import SMTP
from config import settings
from models import empresaModel
from models import emailCheck
from models import updatePassword
#from models import emailConfirm
from models import  encryptPassword
from config.database import  db

app = Flask(__name__)
app.secret_key = 'fjifjidfjied5df45df485h48@ht34'
var=URLSafeTimedSerializer('Thisisasecret')
#---------ruta principal------
@app.get("/")
def index():
    return render_template("home.html")
#---------ruta menu------
@app.route('/empresas/empresaPagina/menu')
def menu():
  productos = empresaModel.obtenerProductos(session['id'])
  return render_template("menu.html",  usuario_id=session['id'], productos=productos )

@app.route('/productos_empresas/<string:usuario_id>')
def carta(usuario_id):

    productos = empresaModel.obtenerProductos(usuario_id)
    return render_template('menu.html', productos=productos)

#------ruta de crud productos-------

@app.route('/crud', methods=["GET", "POST"])
def inicio():
  print(session['id'])
  productos = empresaModel.obtenerProductos(session['id'])
  return render_template("index.html",  usuario_id=session['id'], productos=productos )

#------ruta agregar producto-------
@app.route("/agregar_producto", methods=['POST'])
def agregarProducto():
  if request.method=='POST':
    nombre=request.form['nombre']
    precio=request.form['precio']
    imagen = request.files['imagen']
        #------Guardando imagen-------------
    imagen_ = imagen.filename
    imagen.save('./static/img/' + imagen_)
    empresaModel.insertProduct(nombre=nombre, precio=precio, imagen='/static/img/' + imagen_, usuario_id=session['id'])
    flash("Producto agregado satisfactoriamente")
    return redirect(url_for("inicio"))


#------ruta editar producto------
@app.route("/editar_producto/<id>")
def get_Producto(id):
  cursor=db.cursor()
  cursor.execute("SELECT * FROM productos WHERE id=%s", (id,))
  datos=cursor.fetchall()
  print(datos[0])
  return render_template("editarProducto.html", producto=datos[0])

#------ruta actualizar producto------
@app.route("/actualizar_producto/<string:id>", methods=['POST'])
def actualizarProducto(id):
  if request.method=='POST':
    nombre=request.form['nombre']
    precio=request.form['precio']
    cursor=db.cursor()
    cursor.execute("""
    UPDATE productos
    SET nombre=%s,
    precio=%s
    WHERE id=%s
    """, (nombre, precio, id))
    flash("Producto actualizado satisfactoriamente")
    return redirect(url_for("inicio"))


#------ruta eliminar producto------
@app.route("/eliminar_producto/<string:id>")
def eliminarProducto(id):
  cursor=db.cursor()
  cursor.execute("DELETE FROM productos WHERE id = {0}".format(id))
  flash("Producto removido satisfactoriamente")
  return redirect(url_for("inicio"))




#------ruta de reistro de empresa-------
@app.route('/register', methods=["GET", "POST"])
def register():
  if request.method == 'GET':
    return render_template("register.html")
  else:

    m1=""
    m2=""
    m3=""
    m4=""
    m5=""
    m6=""

    a1=""
    a2=""
    a3=""
    a4=""
    a5=""
    #----almacenado los datos del formulario registro en variables----------
    name = request.form['name']
    description = request.form['description']
    image = request.files['image']
    phone = request.form['phone']
    address = request.form['address']
    email = request.form['email']
    password = request.form['password']
    #-------validando que los campos del formulario no estes vacíos----------
    is_valid = True

    if name == "":
        m1="El nombre es requerido. "
        is_valid = False

    if description == "":
        m2="La descripcion es requerida. "
        is_valid = False

    if phone == "":
        m3="El teléfono es requerido. "
        is_valid = False

    if address == "":
        m4="La dirección es requerida. "
        is_valid = False

    if email == "":
        m5="El email es requerido. "
        is_valid = False

    if password == "":
        m6="La contraseña es requerida. "
        is_valid = False

    if is_valid == False:
        flash(m1+m2+m3+m4+m5+m6)
        return render_template("register.html",
                name=name,
                description=description,
                image=image,
                phone=phone,
                address=address,
                email=email,
                password=password,
        )
    #----------obteniedo el email de la empresa---------
    email_ = emailCheck.getEmail_1(email)
    #----------validando que el correo no se repita --------
    is_valid = True

    if(len(email_) > 0):
         flash("Ya existe una empresa con este correo.")
         is_valid = False

    if is_valid == False:
         return render_template('register.html',
                name=name,
                description=description,
                image=image,
                phone=phone,
                address=address,
                email=email,
                password=password,
         )
    #----validando que la contraseña cumpla con las politicas-----------
    SpecialSym =['$', '@', '#', '%']

    is_valid = True

    if len(password) < 8:
        a1="La longitud debe ser de al menos 8. "
        is_valid = False

    if not any(char.isdigit() for char in password):
        a2="La contraseña debe tener al menos un número. "
        is_valid = False

    if not any(char.isupper() for char in password):
        a3="La contraseña debe tener al menos una letra mayúscula. "
        is_valid = False

    if not any(char.islower() for char in password):
        a4="La contraseña debe tener al menos una letra minúscula. "
        is_valid = False

    if not any(char in SpecialSym for char in password):
        a5="La contraseña debe tener al menos un caracter especial $@#%. "
        is_valid = False

    if  is_valid == False:
        flash("Contraseña inválida. "+a1+a2+a3+a4+a5)
        return render_template('register.html',
                name=name,
                description=description,
                image=image,
                phone=phone,
                address=address,
                email=email,
                password=password,
        )

    #------Guardando imagen-------------
    image_ = image.filename
    image.save('./static/img/' + image_)
    #-------Encriptando contraseña-------
    password = encryptPassword.encryptPassword(password)
    #-------Insertando datos en la base de datos--------
    empresaModel.insertCompany(name=name, description=description, image='/static/img/' + image_, phone=phone, address=address, email=email, password=password )

    #session['name'] = request.form['name']
    #session['email'] = request.form['email']
    #-------Enviando email de Bienvenida--------------------

    token=var.dumps(email, salt='email-confirm')
    link= url_for('emailConfirm_', token=token, _external=True)

    #emailConfirm.messageConfirm(email,link)

    message = EmailMessage()

    message['Subject'] = '¡Bienvenido(a)!'
    message['From'] = 'edisonchicunque2020@itp.edu.co'
    message['To'] = email
    message.set_content(
                        "Gracias por registrarte. Abre este link para terminar el proceso de confirmacion: {}".format(link)
                        )

    username = settings.SMPT_USERNAME
    password = settings.SMPT_PASSWORD

    server = SMTP(settings.SMPT_HOSTNAME)
    server.starttls()
    server.login(username, password)
    server.send_message(message)
    server.quit()
    

    flash("Registro exitoso. Revisa tu correo, te hemos enviado un mensaje para que actives tu cuenta.")

    return render_template("register.html")
#--------ruta, confirmacion de cuenta---------
@app.route("/login/emailConfirm_/<token>")
def emailConfirm_(token):
    try:
        email=var.loads(token, salt='email-confirm', max_age=120)
        cursor = db.cursor()
        cursor.execute("UPDATE users SET status='1' WHERE email='"+email+"'")
        cursor.close()
    except SignatureExpired:
        cursor = db.cursor()
        cursor.execute("DELETE FROM users WHERE email='"+email+"' AND status='0'")
        cursor.close()
        return "<h1>Los sentimos, el tiempo para confirmar tu cuenta ha expirado.</h1>"
    flash("¡Confirmacion exitosa, inicia sesión cuando quieras")    
    return redirect(url_for('login'))    

#----------ruta  inicio de sesion----------
@app.route('/login', methods=["GET", "POST"])
def login():
  if request.method == 'POST':
    m1=""
    m2=""
    e1=""
    e2=""

    email = request.form['email']
    password = request.form['password']

    email_2 = emailCheck.getEmail_2(email)
    email_3 = emailCheck.getEmail_3(email)
    #---------validando que los campos no esten vacios---------
    is_valid = True
    
    if email == "":
      m1="El email es requerido. "
      is_valid = False

    if password == "":
      m2="La contraseña es requerida. "
      is_valid = False

    if is_valid == False:
      flash(m1+m2)
      return render_template("login.html",
                email=email,
                password=password,
        )

    #-------validando que que la cuenta este confirmada---------
    is_valid2=True

    if email_2 is None:
        e1="Este correo no esta registrado. "
        is_valid2=False

    if email_3 is None:
        e2="Cuenta no confirmada."
        is_valid2=False

    if is_valid2 == False:
      flash(e1+e2)
      return render_template("login.html",
                email=email,
                password=password,
        )
    #-------encripdando contraseña--------
    password = encryptPassword.encryptPassword(password)
    #--------validando que el usuario y la contraseña coindan----
    cursor = db.cursor(dictionary=True)
    cursor.execute('select * from users where email = %s', (email,))
    user =cursor.fetchone()
    cursor.close()

    if len(user) > 0:
        if (user['password']==password):
                session['id'] = user['id']
                session['name'] = user['name']
                session['email'] = user['email']
                return redirect(url_for('miCuenta'))

        else:
          flash("Error de contraseña y correo electrónico no coinciden")
          return render_template("login.html",
                email=email,
                )
    else:
       flash("Error de usuario no encontrado")
       return render_template("login.html",
                email=email,
                )
  else:
    return render_template("login.html")
#_____________ruta de
@app.route('/login/miCuenta', methods=['GET','POST'])
def miCuenta():
        return render_template('miCuenta.html')

#----------ruta, recuperacion de contraseña----------------
@app.route('/login/recoverPassword', methods=["GET", "POST"])
def recoverPasswordForm1():
  if request.method == 'POST':
          email = request.form['email_form']
          email_3 = emailCheck.getEmail_3(email)
    #--validaciones del formulario  recoverPassword.html-------
          is_valid = True
          
          
          if email =='':
                  flash("Se requiere un email")
                  is_valid = False

          if  is_valid==False:
              return render_template("recoverPassword.html", email=email)
          else:

              if email_3 is None:
                  flash("Este correo no esta registrado en nuestra base de datos.")
                  return render_template("recoverPassword.html", email=email)
              else:
                #-------Enviando email  con instrucciones para recuperar la contraseña--------------------

                token=var.dumps(email, salt='newPassword')
                link= url_for('recoverPassword_', token=token, _external=True)

                message = EmailMessage()

                message['Subject'] = 'Solicitud de restablecimiento de contraseña.'
                message['From'] = 'edisonchicunque2020@itp.edu.co'
                message['To'] = email
                message.set_content(
                              
                                      "Usted solicitó un restablecimiento de contraseña para su cuenta."
                                      "Para confirmar esta petición, y establecer una nueva contraseña para su cuenta, por favor vaya a la siguiente dirección de Internet:  {}".format(link)

                              )

                username = settings.SMPT_USERNAME
                password = settings.SMPT_PASSWORD

                server = SMTP(settings.SMPT_HOSTNAME)
                server.starttls()
                server.login(username, password)
                server.send_message(message)
                server.quit()
                
                return render_template("recoverPassword_.html")


  else:
    return render_template("recoverPassword.html")

#----------ruta, recuperacion de contraseña dos----------------
@app.route('/login/recoverPasswordd/<token>')
def recoverPassword_(token):
    try:
        email=var.loads(token, salt='newPassword', max_age=600)
    except SignatureExpired:
        flash("Los sentimos, pero este link ha expirado.")
        return render_template('recoverPassword.html')

    flash("¡Confirmacion exitosa, ahora puedes restablcer tu contraseña.")
    return redirect(url_for('recoverPasswordForm2', email=email, _external=True))    


#-----------ruta, formulario recuperar password-------
@app.route('/login/recoverPassword/new/<email>', methods=["GET", "POST"])
def recoverPasswordForm2(email):
      if request.method == 'POST':
            password1 = request.form['password1']
            password2 = request.form['password2']

            is_valid = True

            if password1=='':
                flash("Se requiere una contraseña.")
                is_valid = False
            
            if password2=='':
                flash("Se requiere una contraseña.")
                is_valid = False

            if  is_valid==False:
                return render_template("recoverPasswordForm.html", password1=password1, password2=password2, )
            else:
                    #----validando que la contraseña cumpla con las politicas-----------
                SpecialSym =['$', '@', '#', '%']

                a1=""
                a2=""
                a3=""
                a4=""
                a5=""

                is_valid2 = True

                if len(password1) < 8:
                    a1="La longitud debe ser de al menos 8. "
                    is_valid2 = False

                if not any(char.isdigit() for char in password1):
                    a2="La contraseña debe tener al menos un número. "
                    is_valid2 = False

                if not any(char.isupper() for char in password1):
                    a3="La contraseña debe tener al menos una letra mayúscula. "
                    is_valid2 = False

                if not any(char.islower() for char in password1):
                    a4="La contraseña debe tener al menos una letra minúscula. "
                    is_valid2 = False

                if not any(char in SpecialSym for char in password1):
                    a5="La contraseña debe tener al menos un caracter especial $@#%. "
                    is_valid2 = False

                if  is_valid2 == False:
                    flash("Contraseña inválida. "+a1+a2+a3+a4+a5)
                    return render_template('recoverPasswordForm.html',
                            password1=password1,
                            password2=password2,)
                else:    
                            if password1==password2:

                            #-------Encriptando contraseña-------
                              passwordn = encryptPassword.encryptPassword(password2)
                              updatePassword.updatePassword_(email=email, passwordn=passwordn)
                              flash("Actualizacion de contraseña existosa!")
                              return render_template('login.html')
                            else:
                               flash("Las contraseñas no coinciden")
                               return render_template('recoverPasswordForm.html',
                               password1=password1,
                               password2=password2,)


      else:
        return render_template("recoverPasswordForm.html")

@app.route('/editarRegistro/<int:id>')
def editarRegistro(id):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s",(id,))
    item = cursor.fetchall()
    print(item)
    cursor.close()
    return render_template('updateRegister.html', usuario=item[0])

@app.route('/editarRegistro/<int:id>', methods=['POST'])
def actualizarRegistro(id):
    if request.method == 'POST':
        name = request.form['name']
        description= request.form['description']
        image = request.files['image']
        phone = request.form['phone']
        address = request.form['address']
        email = request.form['email']
        password = request.form['password']

    #------Guardando imagen-------------
        image_ = image.filename
        image.save('./static/img/' + image_)

        empresaModel.actualizarRegistro(name=name, description=description, image='/static/img/' + image_, phone=phone, address=address, email=email, password=password, id=id )

        return redirect(url_for('miCuenta'))

#--------ruta, cerrar sesion------------
@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for('login'))


#if __name__ == '__main__':
#  app.run(port = 5000, debug=True)





