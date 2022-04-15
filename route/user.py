from flask import Flask,render_template,request,jsonify,redirect,url_for,Blueprint
from ml import predict_lang,trans_lang
from flask import session
import db,os
from datetime import timedelta
from werkzeug.utils import secure_filename
from datetime import datetime
def createDirectory(directory): 
    try: 
        if not os.path.exists(directory): 
            os.makedirs(directory) 
    except OSError: 
        print("Error: Failed to create the directory.")
now=datetime.now()
nowDatetime = now.strftime('%Y%m%d%H%M%S')


bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/profiledit',methods=['GET','POST'])
def profiledit():
    if "userid" in session:
        if request.method=='GET':
            return render_template('/user/profile_edit.html', userName="사용자명")
        else: #수정시
            result=""
            username=request.form['username']
            bpwd=request.form['bpwd']
            c1pwd=request.form['c1pwd']
            c2pwd=request.form['c2pwd']
            f=request.files['img']
            imgurl="_"
            if c1pwd!=c2pwd:
                return render_template('alert/profiledit_notpasswd.html') # 새 비밀번호 불일치
            elif db.select_login(session['userid'],bpwd) is None:
                return render_template('alert/profiledit_notpasswd2.html')# 기존비밀번호 불일치
            else: # 저장하기
                print("***&*&*"*10)
                print(session['userimage'])
                print(f.filename)
                imgpath='static/userprofileimg/' +session['userid']+"/"+f.filename
                if session['userimage'] is None or session['userimage']=="_": #기존이미지가 없을경우
                    print('기존 유저이미지가 없을 경우')
                    createDirectory(os.getcwd()+"/static/userprofileimg/"+session['userid'])
                    print(imgpath)
                    if imgpath[-1]!="/":# 바꿀이미지가 있을경우
                        f.save(imgpath) # 바꿀이미지 저장
                        imgurl=f.filename #바꿀이미지 등록
                        session['userimage']=imgurl #세션에 등록
                    result=db.modify_userprofile(session['userid'],username,c1pwd,imgurl)
                else: #기존이미지가 있을경우
                    imgpath='static/userprofileimg/' +session['userid']+"/"+f.filename
                    if imgpath[-1]!="/": # 바꿀이미지가 있을경우
                        print("기존이미지 삭제, 이미지 교체")
                        f.save(imgpath) # 바꿀이미지 저장
                        imgurl=f.filename # 바꿀이미지이름 등록
                        os.remove(os.getcwd()+"/static/userprofileimg/"+session['userid']+"/"+session['userimage'])
                        session['userimage']=imgurl # 세션에 등록
                    else: # 바꿀이미지는 없고 기존이미지만 있을경우
                        imgurl=session['userimage']
                    result=db.modify_userprofile(session['userid'],username,c1pwd,imgurl)
                if result:
                    return redirect(url_for('user.profiledit'))
                
    else:
        return redirect(url_for('login'))

# 로그인 후 이동하는 페이지
@bp.route('/home')
def home():
    if "userid" in session:
        #SSR수행시 값을 전달하는 방법
        return render_template('user/index.html',userName=session['userid'])
    else:#세션정보 없을시, 
        return redirect(url_for('login'))

# 나의식물 페이지로 이동
@bp.route('/myplant',methods=['GET','POST'])
def myplant():
    print('ddd')
    if "userid" in session:
        if request.method=='GET':
            result=db.rend_myplant(session['userid'])
            return render_template('user/myplant.html',userName=session['userid'],plants=result)
        else: # 사진등록시,
            print('등록 post 모드')
            kind=request.form['kind']
            plantname=request.form['plantname']
            memo=request.form['memo']
            f=request.files['img']
            imgpath='static/imgdb/' +session['userid']+"/"+nowDatetime+"_"+f.filename
            createDirectory(os.getcwd()+"/static/imgdb/"+session['userid'])
            f.save(imgpath)
            result=db.create_myplant(session['username'],session['userid'],plantname,nowDatetime+"_"+f.filename,memo)
            if result=="성공":
                return render_template('alert/add_success.html')
            else:
                return render_template('alert/add_fail.html')
    else:#세션정보 없을시, 
        return redirect(url_for('login'))





# 나의식물 등록페이지로 이동
@bp.route('/myplantadd')
def myplantadd():
    if "userid" in session:
        #SSR수행시 값을 전달하는 방법
        return render_template('user/myplant_add.html',userName=session['userid'])
    else:#세션정보 없을시, 
        return redirect(url_for('login'))
