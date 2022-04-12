from flask import Flask,render_template,request,jsonify,redirect,url_for,Blueprint
from ml import predict_lang,trans_lang
from flask import session
import db
from datetime import timedelta
bp = Blueprint('sign', __name__, url_prefix='/sign')

@bp.route('/login',methods=['GET','POST']) # 초기화면
def login():
    session.clear()
    if request.method=='GET':
        id= request.args.get('id')
        return render_template('sign/login.html')
    else:
        #get이 아니면 모두 post 
        id=request.form['id']
        pwd=request.form['pwd']
        # 디비 로그인 체크
        result=db.select_login(id,pwd)
        if result:
            session['userid']=result['id']
            print(session['userid'])
            # 만약, url이 변경되더라도, 변경되는 지점 이외에는 다른 부분은 수정할 필요가 없다.
            return redirect(url_for('user.home'))
        else:
            # 회원아니면
                #회원아님처리
                return render_template('alert/alert.html')



@bp.route('/join', methods=['GET','POST'])
def join():

    if request.method=='GET':
        id= request.args.get('id')
        print("회원가입시도")
        return render_template('sign/join.html')
    else:
        #get이 아니면 모두 post 
        username=request.form['username']
        id=request.form['id']
        pwd=request.form['pwd']
        print("%s : %s : %s"%(username,id,pwd))
        # 디비 로그인 체크
        result=db.create_join(username,id,pwd)
        if result:
            #print(session['userid'])
            print("패스")
            # 만약, url이 변경되더라도, 변경되는 지점 이외에는 다른 부분은 수정할 필요가 없다.
            return render_template('index.html')
        else:
            # 회원가입 에러 띄우기
                return render_template('/ejs/join_error.ejs')


@bp.route('/logout')
def logout():
    session.clear()#세션초기화
    return redirect(url_for('login'))