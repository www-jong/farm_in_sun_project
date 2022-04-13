from flask import Flask,render_template,request,jsonify,redirect,url_for,Blueprint
from ml import predict_lang,trans_lang
from flask import session
import db
from datetime import timedelta
from werkzeug.utils import secure_filename
bp = Blueprint('user', __name__, url_prefix='/user')

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
            print(result[0])
            return render_template('user/myplant.html',userName=session['userid'],plants=result)
        else: # 사진등록시,
            print('등록 post 모드')
            kind=request.form['kind']
            plantname=request.form['plantname']
            memo=request.form['memo']
            f=request.files['img']
            print(f)
            f.save('static/userimages/' + secure_filename(f.filename))
            result=db.create_myplant(session['username'],session['userid'],plantname,memo)
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
