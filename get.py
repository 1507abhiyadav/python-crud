# import ctypes
# from dataclasses import fields
import email
from lib2to3.pgen2 import token
from urllib import response
from wsgiref import headers
import jwt
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import serialization
from array import array
from distutils.log import error
from genericpath import exists
from http import server
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from pickle import TRUE
from types import NoneType
from unicodedata import decimal, name
from gc import collect
from http import client
from xml.dom.minidom import Element
import pymongo
from bson import encode, json_util, ObjectId
try:
	client=pymongo.MongoClient('mongodb://localhost:27017/')
	print("Connected successfully!!!")
except:
	print("Could not connect to MongoDB")

mydb = client['employee']  # database name
collection = mydb['employee']  # collection name
collection_1 = mydb['user'] # collection name
HOST = "127.0.0.1"
PORT = 8000

# employee =[{
#   "id":1,
#   "name":"abhishek"
# },
# { "id":2,
#   "name":"rakesh"
# }]
# print(employee)
expires= datetime.now() + timedelta(minutes=2) -timedelta(hours=5)-timedelta(minutes=30)
expires= datetime.utcnow() + timedelta(minutes=2)

class ServerHTTP(BaseHTTPRequestHandler):
    def _set_headers(self):
      self.send_response(200)
      self.send_header('Content-type','text/json')
      # #reads the length of the Headers
      length = int(self.headers['Content-Length'])
      # #reads the contents of the request
      content = self.rfile.read(length)
      temp = str(content).strip('b\'')
      self.end_headers()
      return temp 

    def error_function(self):
      self.send_response(404)
      self.send_header('Content-type','text/plain')
      self.end_headers()
      self.wfile.write("id not found".encode())

    def error_find(self):
      self.send_response(404)
      self.send_header('Content-type','text/plain')
      self.end_headers()
      self.wfile.write("id  already exist".encode())
      # self.wfile.write(("name already exist").encode())

    def error(self):
      self.send_response(404)
      self.send_header('Content-type','text/plain')
      self.end_headers()
      # self.wfile.write("id  already exist".encode())
      self.wfile.write(("name or password is invalid ").encode())

    
      
   #### login path---->
    def do_GET(self):
        # length = int(self.headers['Content-Length'])
        # # print(length)
        # # # reads the contents of the request
        # content = self.rfile.read(length)
        # temp = str(content).strip('b\'') # data come from postman as string, when the use method post
        # print(temp)       
        try:
            # obj = json.loads(temp) # data convert as object use json.loads
            # print(obj) 
            # all = collection.find_one({'id':obj['id']}) # find the id in the database
            # all = collection.find_one({'name':obj['name'],'password':obj['password']}) # find the name in the database
            all = collection.find()
            # print(all)
            
            var_token= self.headers['Authorization'] # get the token from the header
            # print(var_token)
            token = var_token.split(" ")[1]
            # print(token)
            if all == None:
                self.error()
            if token == None:
              self.send_response(401)
              self.send_header('Content-type','text/plain')
              self.end_headers()
              self.wfile.write(("Invalide token").encode())
            try:
              decode_data = jwt.decode(token,key="secret", algorithms=['HS256'])
              # print(decode_data)
              data = json.loads(json_util.dumps(all))
              for i in data:
                self.send_response(200)
                self.send_header('Content-type','text/json')
                self.end_headers()
                self.wfile.write(json.dumps(i).encode())
              
                # self.send_response(200)
                # self.send_header('Content-type','text/json')
                # self.end_headers()
                # self.wfile.write(json.dumps(data).encode())
            except jwt.ExpiredSignatureError:
              self.send_response(401)
              self.send_header('Content-type','text/plain')
              self.end_headers()
              self.wfile.write(("Token expired").encode())
                
        except Exception as e:
            # print(e)
            self.send_response(400)
            self.send_header('Content-type','text/plain')
            self.end_headers() 
            self.wfile.write(("error massege:"+str(e)).encode())
        except:
            self.send_response(504)
            self.send_header('Content-type','text/plain')
            self.wfile.write(("internal error"+str(e)).encode())
            
####  Sign Up method defination----->

####POST method defination----->
    def do_POST(self):
        if self.path == "/signup":
        # print(self.headers)
        # print("post method is working")
            length = int(self.headers['Content-Length']) 
            # # reads the contents of the request
            content = self.rfile.read(length)
            temp = str(content).strip('b\'') # data come from postman as string, when the use method post
            # print(temp)
            try:
                obj = json.loads(temp)# data convert as object use json.loads
                # print(obj)
                all = collection_1.find_one({'id':obj['id']}) # find the id in the database
                # all = collection.find_one({'name':obj['name'],'password':obj['password']}) # find the name in the database
                # print(all)
                # token = jwt.encode(payload = obj, key = "secret")
                # print(token) 
                if all == None:
                    collection_1.insert_one(obj)
                    self.send_response(200)
                    self.send_header('Content-type','text/plain')
                    self.end_headers()
                    self.wfile.write(("successfully signup").encode())
                    # self.wfile.write((token).encode())
                else:
                    self.error_find()
            
            except Exception as e:
                # print(e)
                self.send_response(400)
                self.send_header('Content-type','text/plain')
                self.end_headers() 
                self.wfile.write(("error massege:"+str(e)).encode())
            except:
                self.send_response(504)
                self.send_header('Content-type','text/plain')
                self.wfile.write(("internal error"+str(e)).encode())

        elif self.path == "/login":
            length = int(self.headers['Content-Length']) 
            # # reads the contents of the request
            content = self.rfile.read(length)
            temp = str(content).strip('b\'') # data come from postman as string, when the use method post
            # print(temp)
            obj = json.loads(temp)
            try:
                # obj = json.loads(temp)# data convert as object use json.loads
                # print(obj)
                # all = collection.find_one({'name':obj['id']}) # find the id in the database
                all = collection_1.find_one({'name':obj['name'],'password':obj['password']}) # find the name in the database
                # print(all)
                data= json.loads(json_util.dumps(all))
                payload={
                    'id':data['id'],
                    'exp':expires
                }
                # dt=datetime.now() + datetime.timedelta(hours=24)
                token = jwt.encode(payload, key = "secret", algorithm = "HS256")
                # print(token)
                # dt = datetime.now() + timedelta(hours=24)
                en_data ={
                    "token":token,
                    "status":200,
                    "message":"successfully login"
                }
                if all != None:
                    # collection.insert_one(obj)
                    self.send_response(200)
                    self.send_header('Content-type','text/plain')
                    self.end_headers()
                    # self.wfile.write(("successfully login").encode())
                    self.wfile.write(json_util.dumps(en_data).encode())
                else:
                    self.error_find()
            
            except Exception as e:
                # print(e)
                self.send_response(400)
                self.send_header('Content-type','text/plain')
                self.end_headers() 
                self.wfile.write(("error massege:name or password not match").encode())
            except:
                self.send_response(504)
                self.send_header('Content-type','text/plain')
                self.wfile.write(("internal error"+str(e)).encode())


        elif self.path == "/post":
        # print(self.headers)
        # print("post method is working")
            # length = int(self.headers['Content-Length']):
            length = int(self.headers['Content-Length']) 
            # # reads the contents of the request
            content = self.rfile.read(length)
            temp = str(content).strip('b\'') # data come from postman as string, when the use method post
            # print(temp)
            
            try:
                obj = json.loads(temp) # data convert as object use json.loads
                # print(obj) 
                all = collection.find_one({'id':obj['id']}) # find the id in the database
                # all = collection.find_one({'name':obj['name'],'password':obj['password']}) # find the name in the database
                # print(all)
                if all == None:
                  var_token= self.headers['Authorization'] # get the token from the header
                  # print(var_token)
                  token = var_token.split(" ")[1]
                  # print(token)
                  if (token == None):
                    self.send_response(404)
                    self.send_header('Content-type','text/plain')
                    self.end_headers()
                    self.wfile.write(("Invalide token").encode())
                  try:
                    var_decode = jwt.decode(token, key = "secret", algorithms = ['HS256'])
                  # print(var_decode)
                    collection.insert_one(obj)
                    self.send_response(200)
                    self.send_header('Content-type','text/plain')
                    self.end_headers()
                    self.wfile.write(("successfully post").encode())
                    
                  except jwt.ExpiredSignatureError:
                      self.send_response(403)
                      self.send_header('Content-type','text/plain')
                      self.end_headers()
                      self.wfile.write(("Token expired").encode())

                  except  Exception as e:
                    self.send_response(401)
                    self.send_header('Content-type','text/json')
                    self.end_headers()
                    self.wfile.write(("unauthentication user").encode())
               
              
            except Exception as e:
                # print(e)
                self.send_response(400)
                self.send_header('Content-type','text/plain')
                self.end_headers() 
                self.wfile.write(("error massege:"+str(e)).encode())
            except:
                self.send_response(504)
                self.send_header('Content-type','text/plain')
                self.wfile.write(("internal error"+str(e)).encode())

### PUT method defination----->

    def do_PUT(self):
    #   print("put method is working")
      
      length = int(self.headers['Content-Length'])
      # reads the contents of the request
      content = self.rfile.read(length)
      temp = str(content).strip('b\'') # # data come from postman as string , when the use method put
      # print(temp)
      try:
        obj = json.loads(temp)  # data convert as object id =4
        data = collection.find_one({'id':obj['id']})
        var_token= self.headers['Authorization'] # get the token from the header
        # print(var_token)
        token = var_token.split(" ")[1]
        if data == None:
          self.error_function()
        if (token == None):
          self.send_response(404)
          self.send_header('Content-type','text/plain')
          self.end_headers()
          self.wfile.write(("Invalide token").encode())

        try:
          var_decode = jwt.decode(token, key = "secret", algorithms = ['HS256'])
          # print(var_decode)
          collection.update_one({'id':obj['id']},{'$set':obj})
          self.send_response(200)
          self.send_header('Content-type','text/plain')
          self.end_headers()
          self.wfile.write(("data successfully update").encode())
        
        except jwt.ExpiredSignatureError:
          self.send_response(403)
          self.send_header('Content-type','text/plain')
          self.end_headers()
          self.wfile.write(("Token expired").encode())
        except Exception as e:
          self.send_response(401)
          self.send_header('Content-type','text/json')
          self.end_headers()
          self.wfile.write(("unauthentication user").encode())

      except Exception as e:
        # print(e)
        self.send_response(400)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write(("error massge:"+str(e)).encode())
      except:
        self.send_response(504)
        self.send_header('Content-type','text/plain')
        self.wfile.write(("internal error"+str(e)).encode())
        
## DELETE method defination----->

    def do_DELETE(self):
      # print("delete method is working")
      length = int(self.headers['Content-Length']) #returns the content length (value of the header) as a string. # <--- Gets the size of data

      # reads the contents of the request
      content = self.rfile.read(length) # <--- Gets the data itself
      temp = str(content).strip('b\'') # data come from postman as string , when the use method delete  
      try:
        obj = json.loads(temp)  # date convert as object 
        all = collection.find_one({'id':obj['id']})
        # print(all)
        var_token= self.headers['Authorization'] # get the token from the header
        # print(var_token)
        token = var_token.split(" ")[1]
        # if all == None:
        #   self.error_function()
        if (token == None):
          self.send_response(401)
          self.send_header('Content-type','text/plain')
          self.end_headers()
          self.wfile.write(("Invalide token").encode())
        try:
          var_decode = jwt.decode(token, key = "secret", algorithms = ['HS256'])
          # print(var_decode)
          collection.delete_one({'id':obj['id']})
          self.send_response(200)
          self.send_header('Content-type','text/plain')
          self.end_headers()
          self.wfile.write(("data successfully delete").encode())
        except jwt.ExpiredSignatureError:
          self.send_response(403)
          self.send_header('Content-type','text/plain')
          self.end_headers()
          self.wfile.write(("Token expired").encode())
        except Exception as e:
          self.send_response(401)
          self.send_header('Content-type','text/json')
          self.end_headers()
          self.wfile.write(("unauthentication user").encode())
       
      except Exception as e:
        # print(e)
        self.send_response(400)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write(("error  massge:"+str(e)).encode())
      except:
        self.send_response(504)
        self.send_header('Content-type','text/plain')
        self.wfile.write(("internal error"+str(e)).encode())

server= HTTPServer((HOST,PORT),ServerHTTP)
print("Server is running on port 8000")
server.serve_forever() 
