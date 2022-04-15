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

# 로그인 후 이동하는 페이지
@bp.route('/home')
def home():
    if "userid" in session:
        #SSR수행시 값을 전달하는 방법
        return render_template('user/index.html',userName=session['userid'])
<<<<<<< HEAD
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


# 나의식물 페이지 리스트로 이동
@bp.route('/myplantlist')
def myplantlist():
    if "userid" in session:
        #SSR수행시 값을 전달하는 방법
        return render_template('user/myplant_list.html',userName=session['userid'])
    else:#세션정보 없을시, 
        return redirect(url_for('login'))


# 예측 파일 업로드
@bp.route('/aiservice')
def aiservice():
    if "userid" in session:
        return render_template('user/aiservice.html',userName=session['userid'])
    else:
=======
    else:#세션정보 있을시, 
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 46abe462be3abaa8f97f190e4996ddd56f9d8f81
=======
>>>>>>> 08cc06566b0991b1755085bbcfe4ba92371ad307
>>>>>>> 46abe462be3abaa8f97f190e4996ddd56f9d8f81
        return redirect(url_for('login'))
