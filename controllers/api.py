from flask import *
import extensions
import hashlib
import uuid
import re

api = Blueprint('api', __name__, template_folder='templates', static_folder ='static')

@api.route('/api/v1/user', methods=['GET','POST','PUT'])
def query():
    if request.method == "GET":
        if 'username' in session:
            username=session['username']
            conn=extensions.connect_to_database()
            cursor=conn.cursor
            sql1='select firstname, lastname, email from User where username="%s"' %username
            cursor.execute(sql1)
            rows=cursor.fetchall()
            firstname=[]
            lastname=[]
            email=[]
            for row in rows:
                firstname.append(row[0])
                lastname.append(row[1])
                email.append(row[2])
            ret_data={
                "username": username,
                "firstname": firstname,
                "lastname": lastname,
                "email": email
                }
            return jsonify(ret_data=ret_data)
        
    if request.method == 'POST':
        content=request.json
        if (content['username']!="") and (content['firstname']!="") and (content['lastname']!="") and (content['password1']!="") and (content['password2']!="") and (content['email']!=""):
            username=content['username']
            firstname=content['firstname']
            lastname=content['lastname']
            password=content['password1']
            pw_verify=content['password2']
            email=content['email']
        else:
            error_data={   
                "errors": [
                    {
                        "message":"You did not provide the necessary fields"
                    }
                ]
            }
            return jsonify(error=error_data), 422

        error=[]
        conn = extensions.connect_to_database()
        cursor = conn.cursor()
        sql2='select username from User'
        cursor.execute(sql2)
        rows=cursor.fetchall()
        flag=0
        for row in rows:
            for ro in row:
                if username==ro:
                    flag=flag+1
        if flag >=1:
            message={"message":"This username is taken"}
            error.append(message)
            
        if len(username) <3:
            message={"message":"Usernames must be at least 3 characters long"}
            error.append(message)

        if len(username)>20:
            message={"message":"Username must be no longer than 20 characters"}
            error.append(message)

        if not re.match('^[a-zA-Z_0-9]+$',username):
            message={"message":"Usernames may only contain letters, digits, and underscores"}
            error.append(message)
            
        if len(firstname)>20:
            message={"message":"Firstname must be no longer than 20 characters"}
            error.append(message)

        if len(lastname)>20:
            message={"message":"Lastname must be no longer than 20 characters"}
            error.append(message)
            
        if len(password)<8:
            message={"message":"Passwords must be at least 8 characters long"}
            error.append(message)
            
        if not ((re.search(r'[a-zA-Z]+',password) and re.search(r'[0-9]+',password))):
            message={"message":"Passwords must contain at least one letter and one number"}
            error.append(message)
            
        if not re.match('^[a-zA-Z_0-9]+$',password):
            message={"message":"Passwords may only contain letters, digits, and underscores"}
            error.append(message)
            
        if password != pw_verify:
            message={"message":"Passwords do not match"}
            error.append(message)
            
        if (not re.match(r"[^@]+@[^@]+\.[^@]+",email)):
            message={"message":"Email address must be valid"}
            error.append(message)
            
        if len(email)>40:
            message={"message":"Email must be no longer than 40 characters"}
            error.append(message)

        if error!=[]:
            error_data={
                "errors": error
                }
            return jsonify(error=error_data), 422
        else:
            conn = extensions.connect_to_database()
            cursor = conn.cursor()
            algorithm='sha512'
            salt=uuid.uuid4().hex
            m=hashlib.new(algorithm)
            m.update(salt+password)
            password_hash=m.hexdigest()
            new_hash="$".join([algorithm,salt,password_hash])
            sql1='insert into User(username,firstname,lastname,password,email) values("%s","%s","%s","%s","%s")' %(username,firstname,lastname,new_hash,email)
            cursor.execute(sql1)
            cursor.close()
            conn.close()

            ret_data={
                "username": username,
                "firstname": firstname,
                "lastname": lastname,
                "email": email
                }
            return jsonify(ret_data=ret_data), 201
        
    if request.method == "PUT":
        if 'username' in session:
            error=[]
            username=session['username']
            conn = extensions.connect_to_database()
            cursor = conn.cursor()
            content=request.json
            firstname=content['firstname']
            lastname=content['lastname']
            password=content['password1']
            pw_verify=content['password2']
            email=content['email']
            
            if firstname != "":
                if len(firstname)>20:
                    message={"message":"Firstname must be no longer than 20 characters"}
                    error.append(message)
                else:
                    sql='update User set firstname="%s" where username="%s"' %(firstname,username)
                    cursor.execute(sql)
                
            if lastname !="":
                if len(lastname)>20:
                    message={"message":"Lastname must be no longer than 20 characters"}
                    error.append(message)
                else:
                    sql='update User set lastname="%s" where username="%s"' %(lastname,username)
                    cursor.execute(sql)
                
            if email != "":
                err=[0,0]
                if not re.match(r"[^@]+@[^@]+\.[^@]+",email):
                    message={"message":"Email address must be valid"}
                    error.append(message)
                else:
                    err[0]=0
                if len(email)>40:
                    message={"message":"Email must be no longer than 40 characters"}
                    error.append(message)
                else:
                    err[1]=0
                if err[0]==0 and err[1]==0:  
                    sql='update User set email="%s" where username="%s"' %(email,username)
                    cursor.execute(sql)
                    
            if password != "" and pw_verify != "":
                err=[0,0,0,0]
                if len(password)<8:
                    message={"message":"Passwords must be at least 8 characters long"}
                    error.append(message)
                else:
                    err[0]=0
                if re.search(r'[a-zA-Z]+',password) and re.search(r'[0-9]+',password):
                    err[1]=0
                else:
                    message={"message":"Passwords must contain at least one letter and one number"}
                    error.append(message)
                if re.match('^[a-zA-Z_0-9]+$',password):
                    err[2]=0
                else:
                    message={"message":"Passwords may only contain letters, digits, and underscores"}
                    error.append(message)
                if password==pw_verify:
                    err[3]=0
                else:
                    message={"message":"Passwords do not match"}
                    error.append(message)
                        
                if err[0]==0 and err[1]==0 and err[2]==0 and err[3]==0: 
                    algorithm='sha512'
                    salt=uuid.uuid4().hex
                    m=hashlib.new(algorithm)
                    m.update(salt+password)
                    password_hash=m.hexdigest()
                    new_hash="$".join([algorithm,salt,password_hash])
                    sql='update User set password="%s" where username="%s"' %(new_hash,username)
                    cursor.execute(sql)
            if error!=[]:
                error_data={
                    "errors": error
                    }
                return jsonify(error=error_data), 422
            else:
                return "", 201
        else:
            error_data={
                "errors":[
                    {
                        "message":"You do not have the necessary credentials for the resource"
                    }
                ]
            }
            return jsonify(error=error_data), 401
            
        
       
@api.route('/api/v1/login', methods=['POST'])
def login():
        
    if request.method == 'POST':
        content=request.json
        username=""
        password=""
        if 'username' in content and 'password' in content:           
            username=content['username']
            password=content['password']
        else:
            error={
                "errors":[
                    {
                        "message":"You did not provide the necessary fields"
                    }
                ]
            }
            return jsonify(error=error),422

        conn = extensions.connect_to_database()
        cursor=conn.cursor()
        sql1='select username from User'
        cursor.execute(sql1)
        row=cursor.fetchall()
        flag=0
        for ro in row:
            for r in ro:
                if r == username:
                    flag=1
        if flag == 0:
            error={
                    "errors":[
                        {
                            "message":"Username does not exist"
                        }
                    ]
            }
            return jsonify(error=error),404
        sql='select password from User where username="%s"' %username
        cursor.execute(sql)
        row=cursor.fetchall()
        cursor.close()
        conn.close()
        passdb=''
        algorithm='sha512'
        for ro in row:
            for r in ro:
                passdb=r
        j=0
        loc=[]
        for i in passdb:
            if i=='$':
                loc.append(j)
            j=j+1
        salt=passdb[((loc[0])+1):((loc[1]))]
        m=hashlib.new(algorithm)
        m.update(salt+password)
        password_hash=m.hexdigest()
        new_hash="$".join([algorithm,salt,password_hash])
        if new_hash==passdb:
            session['username']=username
            return jsonify(user={"username":username})
        else:
            error={
                    "errors":[
                        {
                            "message":"Password is incorrect for the specified username"
                        }
                    ]
            }
            return jsonify(error=error),422
   
@api.route('/api/v1/logout', methods=['POST'])
def logout():
    if request.method == 'POST':
        if 'username' in session:           
            session.pop('username', None)
            return '',204
        else:
            error={
                    "errors":[
                        {
                            "message":"You do not have the necessary credentials for the resource"
                        }
                    ]
            }
            return jsonify(error=error),401
    else:
        abort(404)
    
