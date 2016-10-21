from flask import *
import extensions
import hashlib
import uuid
import re

main = Blueprint('main', __name__, template_folder='templates', static_folder ='static')

@main.route('/')
def main_route():
    if 'username' in session:
        username=session['username']
        conn = extensions.connect_to_database()
        cursor = conn.cursor()
        sql3='select username from AlbumAccess' 
        cursor.execute(sql3)
        rows=cursor.fetchall()
        flag=0
        for row in rows:
            for ro in row:
                if ro==username:
                    flag=flag+1
        albumid=[]
        if flag>0:
            sql='select albumid from AlbumAccess where username="%s"' %username
            cursor.execute(sql)
            rows=cursor.fetchall()
            for ro in rows:
                for r in ro:
                    albumid.append(r)
        sql1='select albumid from Album where username="%s"' %username
        cursor.execute(sql1)
        rows=cursor.fetchall()
        for ro in rows:
            for r in ro:
                albumid.append(r)
        sql3='select albumid from Album where username!="%s" and access="public"' %username
        cursor.execute(sql3)
        rows=cursor.fetchall()
        for ro in rows:
            for r in ro:
                albumid.append(r) 
        title=[]
        for i in albumid: 
            sql2='select title from Album where albumid="%s"' %i
            cursor.execute(sql2)
            x=cursor.fetchone()
            for j in x:
                title.append(j)
        sql2='select firstname, lastname, username from User'
        cursor.execute(sql2)
        rows=cursor.fetchall()
        firstname=[]
        lastname=[]
        user=[]
        for row in rows:
            firstname.append(row[0])
            lastname.append(row[1])
            user.append(row[2])
        cursor.close()
        conn.close()
        return render_template("index.html", zips=zip(firstname,lastname,user),link=zip(albumid,title))
    else:       
        conn = extensions.connect_to_database()
        cursor = conn.cursor()
        cursor.execute('select username, title, albumid from Album where access="public"')
        rows = cursor.fetchall()
        albumid=[]
        username=[]
        title=[]
        for row in rows:
                albumid.append(row[2])
                username.append(row[0])
                title.append(row[1])   
        cursor.close()
        conn.close()
        return render_template("index.html", links=zip(albumid,username,title))

@main.app_errorhandler(404)
def page_not_found(error):
    return render_template( "page_not_found.html" ), 404

@main.route('/login', methods=['GET', 'POST'])
def main_login():
    if request.method == 'GET':
        if 'username' in session:
            return redirect(url_for('main.main_route'))
        else:
            return render_template("login.html", error=[0,0,0,0])
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']
        err = [0,0,0,0]
        correct = [0,0,0,0]
        if not username:
            err[0] = 1
        if not password:
            err[1] = 1
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
            err[2] = 1
        if err != correct:
            return render_template("login.html", error=err)
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
            return redirect(url_for('main.main_route'))
        else:
            err[3] = 1
            return render_template("login.html", error=err)


@main.route('/user')
def main_user():
    correct=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    if 'username' in session:
        return redirect(url_for('main.main_user_edit'))
    else:
        return render_template("user.html")
    

@main.route('/user/edit',methods=['POST','GET'])
def main_user_edit():
    if not 'username' in session:
        return redirect(url_for('main.main_login'))
        
    conn = extensions.connect_to_database()
    cursor = conn.cursor()
    sql2='select firstname, lastname, username from User'
    cursor.execute(sql2)
    rows=cursor.fetchall()
    firstname=[]
    lastname=[]
    user=[]
    for row in rows:
        firstname.append(row[0])
        lastname.append(row[1])
        user.append(row[2])
    cursor.close()
    conn.close()
    
    if request.method == 'GET':
        if 'username' in session:
            return render_template("user_edit.html", zips=zip(firstname,lastname,user),error=[0,0])
        else:
            return redirect(url_for('main.main_login'))
    if request.method == 'POST':
        err=[0,0,0,0,0,0,0,0]
        correct=[0,0,0,0,0,0,0,0]
        username=session['username']
        conn = extensions.connect_to_database()
        cursor = conn.cursor()
        
        if 'firstname' in request.form:
            firstname=request.form['firstname']
            
            if len(firstname)>20:
               err[0]=1
            else:
                err[0]=0
                sql='update User set firstname="%s" where username="%s"' %(firstname,username)
                cursor.execute(sql)
        elif 'lastname' in request.form:
            lastname=request.form['lastname']
            if len(lastname)>20:
                err[1]=1
            else:
                err[1]=0
                sql='update User set lastname="%s" where username="%s"' %(lastname,username)
                cursor.execute(sql)
            
        elif 'email' in request.form:
            email=request.form['email']
            if not re.match(r"[^@]+@[^@]+\.[^@]+",email):
                err[6]=1
            else:
                err[6]=0
            if len(email)>40:
                err[7]=1
            else:
                err[7]=0
            if err[6]==0 and err[7]==0:  
                sql='update User set email="%s" where username="%s"' %(email,username)
                cursor.execute(sql)
        elif 'password1' in request.form and 'password2' in request.form:
            password=request.form['password1']
            pw_verify=request.form['password2']
            if len(password)<8:
                err[2]=1
            else:
                err[2]=0
            if re.search(r'[a-zA-Z]+',password) and re.search(r'[0-9]+',password):
                err[3]=0
            else:
                err[3]=1
            if re.match('^[a-zA-Z_0-9]+$',password):
                err[4]=0
            else:
                err[4]=1
            if password==pw_verify:
                err[5]=0
            else:
                err[5]=1
                    
            if err[2]==0 and err[3]==0 and err[4]==0 and err[5]==0: 
                algorithm='sha512'
                salt=uuid.uuid4().hex
                m=hashlib.new(algorithm)
                m.update(salt+password)
                password_hash=m.hexdigest()
                new_hash="$".join([algorithm,salt,password_hash])
                sql='update User set password="%s" where username="%s"' %(new_hash,username)
                cursor.execute(sql)
                
        sql2='select firstname, lastname, username from User'
        cursor.execute(sql2)
        rows=cursor.fetchall()
        firstname=[]
        lastname=[]
        user=[]
        for row in rows:
            firstname.append(row[0])
            lastname.append(row[1])
            user.append(row[2])   
        cursor.close()
        conn.close()
        if err!=correct:
            return render_template("user_edit.html", zips=zip(firstname,lastname,user),error=err)
        else:
            return render_template("user_edit.html", zips=zip(firstname,lastname,user),error=correct)
        
    else:
        return render_template("user_edit.html", zips=zip(firstname,lastname,user),error=correct)

@main.route('/logout',methods=['POST'])
def main_logout():
    if request.method == 'POST':
        session.pop('username', None)
        return redirect(url_for('main.main_route'))
    else:
        abort(404)
        
@main.app_errorhandler(403)
def page_not_found(error):
    return render_template( "forbidden.html" ), 403
