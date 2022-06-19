'''
import re

p= "aA@45678"

def password_check(password):
  valid_ = 0
  while True:
      if (len(password)<8):
          print("La contraseña debe tener 8 caracteres como mínimo")
          valid_ = 1
          break
      elif not re.search("[a-z]", password):
          print("La contraseña debe tener una letra minúscula como mínimo")
          valid_ = 1
          break
      elif not re.search("[A-Z]", password):
          print("La contraseña debe tener una letra mayúscula como mínimo")
          valid_ = 1
          break
      elif not re.search("[0-9]", password):
          print("La contraseña debe tener un número como mínimo")
          valid_ = 1
          break
      elif not re.search("[@$!%*#?&_-]", password):
          print("La contraseña debe tener un caracter especial como minínimo")
          valid_ = 1
          break
      elif re.search("\s", password):
          print("La contraseña no puede tener espacios")
          valid_ = 1
          break
      else:
          valid_ = 0
          print("Cotraseña válida")
          break

  if valid_ ==1:
      print("Contraseña no válida")

#contraseña_validada=password_check(p)
############################################


a1=""
a2=""
a3=""
a4=""
a5=""
def passwordCheck(passwd): 

    SpecialSym =['$', '@', '#', '%'] 
    val = True
      
    if len(passwd) < 8: 
        a1="length should be at least 6"
        val = False
          
    if not any(char.isdigit() for char in passwd): 
        a2="Password should have at least one numeral"
        val = False
          
    if not any(char.isupper() for char in passwd): 
        a3="Password should have at least one uppercase letter"
        val = False
          
    if not any(char.islower() for char in passwd): 
        a4="Password should have at least one lowercase letter"
        val = False
          
    if not any(char in SpecialSym for char in passwd):
        a5="Password should have at least one of the symbols $@#"
        val = False
    if val:
      
        return val 
#######################
def main(): 
    passwd = 'Geek12@i'
      
    if (password_check(passwd)): 
        print("Password is valid") 
    else: 
        print("Invalid Password !!") 
          
if __name__ == '__main__': 
    main() 


'''
