from lib2to3.pgen2 import token
import jwt
from cryptography.hazmat.primitives import serialization
from datetime import datetime, timedelta
import jwt

JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_HOURS = 24
payload_data = {
    "id":17102 ,
    "name": "Abhishek Yadav",
    "email": "Abhi15@gamil.com"
}
# payload = {
#         'user_id': user.id,
#         'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
#     }
# jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
# return json_response({'token': jwt_token.decode('utf-8')})


token = jwt.encode(payload=payload_data,key="secret")
print(token)

data = jwt.decode(token,key="secret", algorithms=['HS256'])
print(data)
