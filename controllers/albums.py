from flask import *
import os
import os.path
import extensions

albums = Blueprint('albums', __name__, template_folder='templates', static_folder = 'static/images')

rootdir="static/images"

@albums.route('/albums/edit',methods =['POST','GET'])
def albums_edit_route():
	options = {
		"edit": True
	}
	if request.method == 'POST':
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
                                username=r
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
                return render_template("albums.html", name=username,album=albumid,title=title,**options)

@albums.route('/albums',methods=['GET'])
def albums_route():
	options = {
		"edit": False
	}
	conn = extensions.connect_to_database()
        cursor = conn.cursor()
	if 'username' in session:
                username=session['username']
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
        else:
                username = request.args.get('username')
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
                sql = 'select * from Album where username="%s" and access="public"' % username
                cursor.execute(sql)
                rows = cursor.fetchall()
                albumid=[]
                title=[]
                cursor.close()
                conn.close()
                for row in rows:
                    albumid.append(int(row[0]))
                    title.append(row[1])	
        return render_template("albums.html", name=username,album=albumid,title=title,**options)
