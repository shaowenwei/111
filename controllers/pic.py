from flask import *
import extensions
import os
import os.path
from datetime import datetime


pic = Blueprint('pic', __name__, template_folder='templates', static_folder = 'static/images')

rootdir="static/images"

@pic.route('/pic',methods=['GET','POST'])
def pic_route():
        if request.method == 'GET':
                flag_prev=0;
                flag_next=0;
                picid=request.args.get('picid')
                if picid is None:
                        abort(404)
                if len(picid) ==0:
                        abort(404)
                conn = extensions.connect_to_database()
                cursor = conn.cursor()
                sql='select caption from Contain where picid= "%s" ' %picid
                cursor.execute(sql)
                row=cursor.fetchone()
                for ro in row:
                        caption=ro
                sql1='select albumid from Contain where picid= "%s" ' %picid
                cursor.execute(sql1)
                aid=cursor.fetchone()[0]
                sql2='select access from Album where albumid=%d' % aid
                cursor.execute(sql2)
                acc = cursor.fetchone()[0]
                if acc == 'private':
                    if 'username' in session:
                        username=session['username']
                        hasacc = 0
                        sql7 = 'select username from Album where albumid=%d' %aid
                        cursor.execute(sql7)
                        uname = cursor.fetchone()[0]
                        if uname == username:
                            hasacc = 1
                            isowner = 1
                        sql6 = 'select username from AlbumAccess where albumid=%d' %aid
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
                if acc == 'public':
                    sql7 = 'select username from Album where albumid=%d' %aid
                    cursor.execute(sql7)
                    uname = cursor.fetchone()[0]
                    if uname == username:
                        isowner = 1 
                        
                file=''
                picid=str(picid)
                suc=0;
                for parent, dirname, filenames in os.walk(rootdir):
                        for filename in filenames:
                                files = filename.rsplit('.', 1)[0]
                                if picid == files:
                                        file=filename
                                        suc=suc+1
                if suc==0:
                        abort(404)
                sql2='select picid from Contain where albumid= %d order by sequencenum ASC' %aid
                cursor.execute(sql2)
                rows = cursor.fetchall()
                a=0
                piclist=[]
                for row in rows:
                    for r in row:
                        piclist.append(r)
                        a=a+1
                i=0
                for row in rows:
                        i=i+1
                        if row[0] == picid:
                                break
                if i==a:
                        flag_next=1
                if i==1:
                        flag_prev=1
                cursor.close()
                conn.close()
                return render_template("pic.html",caption=caption,flag_prev=flag_prev,flag_next=flag_next,file=file,piclist=piclist,num=i-1,albumid=aid, capedit=isowner)
        if request.method == 'POST':
                now=datetime.now()
                op=request.form['op']
                if op == 'caption':
                        caption=request.form['caption']
                        picid=request.form['picid']
                        conn = extensions.connect_to_database()
                        cursor = conn.cursor()
                        sql='update Contain set caption="%s" where picid="%s"'%(caption,picid)
                        cursor.execute(sql)
                        flag_prev=0
                        flag_next=0
                        sql1='select albumid from Contain where picid= "%s" ' %picid
                        cursor.execute(sql1)
                        rows=cursor.fetchall()
                        for row in rows:
                                for ro in row:
                                        aid=ro
                        aid=int(aid)
                        file=''
                        suc=0
                        for parent, dirname, filenames in os.walk(rootdir):
                                for filename in filenames:
                                        files = filename.rsplit('.', 1)[0]
                                        if picid == files:
                                                file=filename
                                                suc=suc+1
                        if suc==0:
                                abort(404)
                        sql2='select picid from Contain where albumid= %d order by sequencenum ASC' %aid
                        cursor.execute(sql2)
                        rows = cursor.fetchall()
                        a=0
                        piclist=[]
                        for row in rows:
                                piclist.append(row)
                                a=a+1
                        i=0
                        for row in rows:
                                i=i+1
                                if row[0] == picid:
                                        break
                        if i==a:
                                flag_next=1
                        if i==1:
                                flag_prev=1
                        sql3 = 'update Album set lastupdated="%s" where albumid=%d' %(now.strftime('%Y-%m-%d %H:%M:%S'), aid)
                        cursor.execute(sql3)                                
                        cursor.close()
                        conn.close()
                        return render_template("pic.html",caption=caption,flag_prev=flag_prev,flag_next=flag_next,file=file,piclist=piclist,num=i-1,albumid=aid)                      

@pic.route('/pic/prev',methods=['GET'])
def pic_prev():
        picid = request.args.get('picid')
        return redirect(url_for('pic.pic_route',picid=picid))
        

@pic.route('/pic/next',methods=['GET'])
def pic_next():
        picid = request.args.get('picid')
        return redirect(url_for('pic.pic_route',picid=picid))


        



        
