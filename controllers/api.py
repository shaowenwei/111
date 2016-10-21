from flask import *
import extensions
import hashlib
import uuid
import re

api = Blueprint('api', __name__, template_folder='templates', static_folder ='static')

@api.route('/api/v1/user', methods=['GET','POST'])
def query():
    correct=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    if request.method == "GET":
        username=request.args.get("username")
        password=request.args.get("password")
        ret_data={
            "username": username,
            "firstname": firstname,
            "lastname": lastname,
            "email": email
            }
        if 'username' in session:
            return jsonify(ret_data=ret_data)
        
    if request.method == 'POST':
        username=request.form['username']
        firstname=request.form['firstname']
        lastname=request.form['lastname']
        password=request.form['password1']
        pw_verify=request.form['password2']
        email=request.form['email']
        err=[]
        error=[]
        if username=="":
            err.append(1)
            error.append("Username may not be left blank")
        else:
            err.append(0)
        if firstname=="":
            err.append(1)
            error.append("Firstname may not be left blank")
        else:
            err.append(0)
        if lastname=="":
            err.append(1)
            error.append("Lastname may not be left blank")
        else:
            err.append(0)
        if password=="":
            err.append(1)
            error.append("Password1 may not be left blank")
        else:
            err.append(0)
        if email=="":
            err.append(1)
            error.append("Email may not be left blank")
        else:
            err.append(0)
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
            err.append(1)
            error.append("This username is taken")
        else:
            err.append(0)
        if len(username) <3:
            err.append(1)
            error.append("Usernames must be at least 3 characters long")
        else:
            err.append(0)
        if len(username)>20:
            err.append(1)
            error.append("Username must be no longer than 20 characters")
        else:
            err.append(0)
        if re.match('^[a-zA-Z_0-9]+$',username):
            err.append(0)
        else:
            err.append(1)
            error.append("Usernames may only contain letters, digits, and underscores")
        if len(firstname)>20:
            err.append(1)
            error.append("Firstname must be no longer than 20 characters")
        else:
            err.append(0)

        if len(lastname)>20:
            err.append(1)
            error.append("Lastname must be no longer than 20 characters")
        else:
            err.append(0)
            
        if len(password)<8:
            err.append(1)
            error.append("Passwords must be at least 8 characters long")
        else:
            err.append(0)
            
        if (re.search(r'[a-zA-Z]+',password) and re.search(r'[0-9]+',password)):
            err.append(0)
        else:
            err.append(1)
            error.append("Passwords must contain at least one letter and one number")
            
        if re.match('^[a-zA-Z_0-9]+$',password):
            err.append(0)
        else:
            err.append(1)
            error.append("Passwords may only contain letters, digits, and underscores")
            
        if password==pw_verify:
            err.append(0)
        else:
            err.append(1)
            error.append("Passwords do not match")
            
        if (not re.match(r"[^@]+@[^@]+\.[^@]+",email)):
            err.append(1)
            error.append("Email address must be valid")
        else:
            err.append(0)
            
        if len(email)>40:
            err.append(1)
            error.append("Email must be no longer than 40 characters")
        else:
            err.append(0)

        if err!=correct:
            ret_data={
                "username": username,
                "firstname": firstname,
                "lastname": lastname,
                "email": email,
                "error": error
                }
            return jsonify(ret_data=ret_data), 201
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
    
