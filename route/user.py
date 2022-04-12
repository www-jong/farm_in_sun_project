from flask import Flask,render_template,request,jsonify,redirect,url_for,Blueprint
from ml import predict_lang,trans_lang
from flask import session
import db
from datetime import timedelta
bp = Blueprint('user', __name__, url_prefix='/user')

# 로그인 후 이동하는 페이지
@bp.route('/home')
def home():
    if "userid" in session:
        #SSR수행시 값을 전달하는 방법
        return render_template('user/index.html',userName=session['userid'])
    else:#세션정보 있을시, 
        return redirect(url_for('login'))