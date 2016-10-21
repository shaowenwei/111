from flask import *
import os
import os.path
import extensions
import main


albums = Blueprint('albums', __name__, template_folder='templates', static_folder = 'static')

rootdir="static/images"

@albums.route('/albums/edit',methods =['POST','GET'])
def albums_edit_route():
	options = {
		"edit": True
	}
	conn = extensions.connect_to_database()
	cursor = conn.cursor()
	sql2='select firstname, lastname, username from User'
	cursor.execute(sql2)
	rows=cursor.fetchall()
	firstname=[]
	lastname=[]
	user1=[]
	cursor.close()
	conn.close()
	for row in rows:
                firstname.append(row[0])
                lastname.append(row[1])
                user1.append(row[2])
	if request.args.get('username'):
                if not 'username' in session:
                        return redirect(url_for('main.main_login'))
                else:
                        username=session['username']
                        user=request.args.get('username')
                        if user==username:
                                username=session['username']
                                conn = extensions.connect_to_database()
                                cursor = conn.cursor()
                                sql1 = 'select username from User'
                                cursor.execute(sql1)
                                rows=cursor.fetchall()
                                log=0;
                                for row in rows:
                                        for r in row:
                                                if username==r:
                                                        log=log+1
                                if log==0:
                                        abort(404)
                                sql = 'select * from Album where username="%s"' % username
                                cursor.execute(sql)
                                rows = cursor.fetchall()
                                albumid=[]
                                title=[]
                                cursor.close()
                                conn.close()
                                for row in rows:
                                    albumid.append(int(row[0]))
                                    title.append(row[1])
                                return render_template("albums.html", zips=zip(firstname,lastname,user1), name=username,album=albumid,title=title,**options)
                        else:
                                abort(403)
        if request.method == 'POST':
                if not 'username' in session:
                        return redirect(url_for('main.main_login'))
                else:
                        op=request.form['op']
                        if op =='delete':
                                albumid=request.form['albumid']
                                albumid=int(albumid)
                                conn = extensions.connect_to_database()
                                cursor=conn.cursor()
                                sql6='select username from Album where albumid=%d' %albumid
                                cursor.execute(sql6)
                                row=cursor.fetchall()
                                for r in row: 
                                        username=r[0]
                                if username!=session['username']:
                                        abort(403)
                                sql1='select picid from Contain where albumid=%d' %albumid
                                cursor.execute(sql1)
                                rows=cursor.fetchall()
                                for row in rows:
                                        for r in row:
                                                for parent, dirname, filenames in os.walk(rootdir):
                                                        for filename in filenames:
                                                                if r in filename:
                                                                       file='static/images/%s' %filename
                                                                       os.remove(file)
                                sql7='delete from AlbumAccess where albumid=%d' %albumid
                                cursor.execute(sql7)
                                sql2='delete from Contain where albumid=%d' %albumid
                                cursor.execute(sql2)
                                for row in rows:
                                        sql='delete from Photo where picid="%s"' %row
                                        cursor.execute(sql)
                                sql3='delete from Album where albumid=%d' %albumid
                                cursor.execute(sql3)
                                sql4 = 'select * from Album where username="%s"' % username
                                cursor.execute(sql4)
                                rowss = cursor.fetchall()
                                albumid=[]
                                title=[]
                                for rows in rowss:
                                    albumid.append(int(rows[0]))
                                    title.append(rows[1])
                                cursor.close()
                                conn.close()
                                return redirect(url_for('albums.albums_edit_route'))
                        if op =='add':
                                username=request.form['username']
                                if username!=session['username']:
                                        abort(403)
                                title=request.form['title']
                                conn = extensions.connect_to_database()
                                cursor=conn.cursor()
                                sql1='insert into Album(title,username,access) values("%s","%s","private")' %(title,username)
                                cursor.execute(sql1)
                                sql2='select * from Album where username="%s"' %username
                                cursor.execute(sql2)
                                rows=cursor.fetchall()
                                albumid=[]
                                titles=[]
                                for row in rows:
                                        albumid.append(row[0])
                                        titles.append(row[1])
                                cursor.close()
                                conn.close()
                                return redirect(url_for('albums.albums_edit_route'))
        elif 'username' in session:
                username=session['username']
                conn = extensions.connect_to_database()
                cursor = conn.cursor()
                sql1 = 'select username from User'
                cursor.execute(sql1)
                rows=cursor.fetchall()
                log=0;
                for row in rows:
                        for r in row:
                                if username==r:
                                        log=log+1
                if log==0:
                        abort(404)
                sql = 'select * from Album where username="%s"' % username
                cursor.execute(sql)
                rows = cursor.fetchall()
                albumid=[]
                title=[]
                cursor.close()
                conn.close()
                for row in rows:
                    albumid.append(int(row[0]))
                    title.append(row[1])
                return render_template("albums.html", zips=zip(firstname,lastname,user1), name=username,album=albumid,title=title,**options)
        else:
                return redirect(url_for('main.main_login'))
                
@albums.route('/albums',methods=['GET'])
def albums_route():
	options = {
		"edit": False
	}
	conn = extensions.connect_to_database()
        cursor = conn.cursor()
        if request.method == 'GET':
        	if 'username' in session:
                        username=session['username']
                elif request.args.get('username'):
                        username = request.args.get('username')
                else:
                        return redirect(url_for('main.main_login'))
                conn = extensions.connect_to_database()
                cursor = conn.cursor()
                sql1 = 'select username from User'
                cursor.execute(sql1)
                rows=cursor.fetchall()
                log=0;
                for row in rows:
                        for r in row:
                                if username==r:
                                        log=log+1
                if log==0:
                        abort(404)
                if request.args.get('username'):
                        sql = 'select * from Album where username="%s" and access="public"' % username
                elif 'username' in session:
                        sql = 'select * from Album where username="%s"' % username
                cursor.execute(sql)
                result = cursor.fetchall()
                albumid=[]
                title=[]
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
                for row in result:
                    albumid.append(int(row[0]))
                    title.append(row[1])
                return render_template("albums.html", zips=zip(firstname,lastname,user), name=username,album=albumid,title=title,**options)

