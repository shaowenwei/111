from flask import *
import extensions
import os
import os.path
from datetime import datetime
from werkzeug.utils import secure_filename
import hashlib


album = Blueprint('album', __name__, template_folder='templates',static_folder = 'static')

rootdir="static/images"

allowed_extensions = set(['png', 'jpg', 'bmp', 'gif'])
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in allowed_extensions

@album.route('/album/edit', methods=['GET', 'POST'])
def album_edit_route():
	options = {
		"edit": True
	}
	now=datetime.now()
	
        if request.method == 'POST':
            op=request.form['op']
            
            conn = extensions.connect_to_database()
            cursor = conn.cursor()
            albumid = int(request.form['albumid'])  
            picid = 0
            
            #P2 adding access, grant, revoke, and checking user
            if 'username' in session:
                username=session['username']
                sql = 'select username from Album where albumid=%d' %albumid
                cursor.execute(sql)
                uname = cursor.fetchone()[0]
                if uname != username:
                    abort(403)
            else:
                abort(403)
	  
            if op == 'access':
                acc = request.form['access']
                sql = "update Album set access='%s' where albumid=%d" %(acc,albumid)
                cursor.execute(sql)
                if acc == 'public':
                    sql1 = 'delete from AlbumAccess where albumid=%d' %albumid
                    cursor.execute(sql1)                    
            if op == 'grant':
                username = request.form['username']
                sql = 'insert into AlbumAccess(albumid, username) values (%d, "%s")' %(albumid, username)
                cursor.execute(sql)
            if op == 'revoke':
                username = request.form['username']
                sql = 'delete from AlbumAccess where albumid=%d AND username="%s"' %(albumid, username)
                cursor.execute(sql)
            
            if op == 'delete':
                picid = request.form['picid']
                sql = 'delete from Contain where picid="%s"' %picid
                cursor.execute(sql)
                sql1 = 'delete from Photo where picid="%s"' %picid
                cursor.execute(sql1)
                for parent, firname, filenames in os.walk(rootdir):
                    for filename in filenames:
                        if picid in filename:
                            file = "static/images/%s" %filename
                            os.remove(file)
            if op == 'add':
                file = request.files['file']
                if file.filename == '':
                    abort(404)
                filehash = ''
                fileformat = ''
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    m = hashlib.md5(str(albumid) + filename)
                    filehash = m.hexdigest()
                    fileformat = filename.rsplit('.', 1)[1]
                    name = filehash + '.' + fileformat
                    file.save(os.path.join(rootdir, name))
                sql = 'select max(sequencenum) from Contain'
                cursor.execute(sql)
                seqnum = cursor.fetchone()
                sequencenum = seqnum[0] + 1
                sql1 = 'insert into Photo(picid, format, date) values("%s", "%s", "%s")' %(filehash, fileformat, now.strftime('%Y-%m-%d %H:%M:%S'))
                cursor.execute(sql1)
                sql2 = 'insert into Contain(sequencenum, albumid, picid, caption) values(%i, %s, "%s", "")' %(sequencenum, albumid, filehash)
                cursor.execute(sql2)
            sql3 = 'update Album set lastupdated="%s" where albumid=%d' %(now.strftime('%Y-%m-%d %H:%M:%S'), albumid)
            cursor.execute(sql3)
            sql='select username from Album where albumid = %d' %albumid
            cursor.execute(sql)
            row=cursor.fetchall()
            for r in row:
                username=r
            sql2= 'select * from Contain where albumid= %s order by sequencenum ASC' % albumid
            cursor.execute(sql2)
            rows=cursor.fetchall()
            picid=[]
            for row in rows:
                    picid.append(str(row[2]))
            files=[]
            for parent, dirname, filenames in os.walk(rootdir):
                    for pid in picid:
                            for filename in filenames:                               
                                    if pid in filename:
                                            files.append(filename)
            sql1= 'select title from Album where albumid= %d' % albumid
            cursor.execute(sql1)
            titles=cursor.fetchone()
            title=titles[0]
            cursor.close()
            conn.close()           
            return redirect(url_for('album.album_edit_route',albumid=albumid))
        if request.method == 'GET':
            albumid = request.args.get('albumid')
            if albumid is None:
                abort(404)
            if albumid.isdigit():
                albumid = int(albumid)
            else:
                abort(404)
            conn = extensions.connect_to_database()
            cursor = conn.cursor()

            sql4='select albumid from Album'
            cursor.execute(sql4)
            rows=cursor.fetchall()
            log=0
            for row in rows:
                for r in row:
                    if r == int(albumid):
                        log=log+1
            if log ==0:
                abort(404)
                
            #P2 adding access, grant, revoke, checking if user is owner
            if 'username' in session:
                username=session['username']
                sql = 'select username from Album where albumid=%d' %albumid
                cursor.execute(sql)
                uname = cursor.fetchone()[0]
                if uname != username:
                    abort(403)
            else:
                abort(403)
            sql2='select firstname, lastname, username from User'
            cursor.execute(sql2)
            rows=cursor.fetchall()
            firstname=[]
            lastname=[]
            user1=[]
            for row in rows:
            	firstname.append(row[0])
            	lastname.append(row[1])
            	user1.append(row[2])   
            sql5='select access from Album where albumid=%d' %albumid
            cursor.execute(sql5)
            acc=cursor.fetchone()[0]
            sql6='select username from AlbumAccess where albumid=%d' %albumid
            cursor.execute(sql6)
            rows = cursor.fetchall()
            names=[]
            for row in rows:
                names.append(str(row[0]))
                    
            #END OF P2
            
            sql1= 'select title from Album where albumid= %d' % albumid
            cursor.execute(sql1)
            titles=cursor.fetchone()
            title=titles[0]
            sql2= 'select * from Contain where albumid= %d order by sequencenum ASC' % albumid
            cursor.execute(sql2)
            rows=cursor.fetchall()
            sql3= 'select username from Album where albumid= %d ' % albumid
            cursor.execute(sql3)
            user=cursor.fetchone()
            cursor.close()
            conn.close()
            picid=[]
            for row in rows:
                    picid.append(str(row[2]))
            files=[]
            for parent, dirname, filenames in os.walk(rootdir):
                    for pid in picid:
                            for filename in filenames:                               
                                    if pid in filename:
                                            files.append(filename)
            return render_template("album.html", zips=zip(firstname,lastname,user1),username=user, title=title, links=zip(files,picid), albumid=albumid, acc=acc, names=names, **options)
            
    
    

@album.route('/album',methods=['GET'])
def album_route():
	options = {
		"edit": False
	}
	albumid = request.args.get('albumid')
        if albumid is None:
            abort(404)
        if albumid.isdigit():
            albumid = int(albumid)
        else:
            abort(404)
	conn = extensions.connect_to_database()
        cursor = conn.cursor()
        sql4='select albumid from Album'
        cursor.execute(sql4)
        rows=cursor.fetchall()
        log=0
        for row in rows:
            for r in row:
                if r == (albumid):
                    log=log+1
        if log == 0:
            abort(404)
            
        # P2 PART: checking if album is public, or if the user has access
        sql5 = 'select access from Album where albumid=%d' % albumid
        cursor.execute(sql5)
        acc = cursor.fetchone()[0]

        if acc == 'private':
            if 'username' in session:
                username=session['username']
                hasacc = 0
                sql7 = 'select username from Album where albumid=%d' %albumid
                cursor.execute(sql7)
                uname = cursor.fetchone()[0]
                if uname == username:
                    hasacc = 1
                sql6 = 'select username from AlbumAccess where albumid=%d' %albumid
                cursor.execute(sql6)
                rows=cursor.fetchall()
                for row in rows:
                    for r in row:
                        if r == username:
                            hasacc = 1       
                if hasacc == 0:
                    abort(403)
            else:
                cursor.close()
                conn.close()
                return redirect(url_for('main.main_login'))
        
        sql1= 'select title from Album where albumid= %d' % albumid
        cursor.execute(sql1)
        titles=cursor.fetchone()
        title=titles[0]
        sql2= 'select * from Contain where albumid= %d order by sequencenum ASC' % albumid
        cursor.execute(sql2)
        rows=cursor.fetchall()
        sql3= 'select username from Album where albumid= %d ' % albumid
        cursor.execute(sql3)
        user=cursor.fetchone()[0] 
        picid=[]
        caption=[]
        date=[]
        for row in rows:
                picid.append(str(row[2]))
                caption.append(str(row[3]))
        files=[]
        for parent, dirname, filenames in os.walk(rootdir):
                for pid in picid:
                        for filename in filenames:                               
                                if pid in filename:
                                        files.append(filename)
        date=[]
        for pid in picid:
            sql='select date from Photo where picid ="%s"' %pid
            cursor.execute(sql)
            rows=cursor.fetchone()
            for row in rows:
                date.append(row.strftime("%B %d, %Y"))
		
	sql2='select firstname, lastname, username from User'
        cursor.execute(sql2)
        rows=cursor.fetchall()
        firstname=[]
        lastname=[]
        user1=[]
        for row in rows:
            	firstname.append(row[0])
            	lastname.append(row[1])
            	user1.append(row[2])
        cursor.close()
        conn.close()
	return render_template("album.html", zips=zip(firstname,lastname,user1),username=user, title=title, links=zip(files,picid,caption,date), albumid=albumid, **options)
