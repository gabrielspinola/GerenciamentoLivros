# Arquivo de teste para funcionalidades diversas

#from werkzeug.security import generate_password_hash, check_password_hash

#hashed_password = generate_password_hash("123456")
#print(hashed_password)
#print(check_password_hash(hashed_password, "123456"))
from datetime import date, datetime

print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
print(datetime.strptime('1985-12-15',"%d/%m/%Y"))
