from venv import create
from flask import Flask,render_template,request,jsonify,redirect,url_for,Blueprint
from ml import predict_lang,trans_lang
from flask import session
import db,os
from datetime import timedelta
bp = Blueprint('sign', __name__, url_prefix='/sign')
def createDirectory(directory): 
    try: 
        if not os.path.exists(directory): 
            os.makedirs(directory) 
    except OSError: 
        print("Error: Failed to create the directory.")



@bp.route('/logingo')
def logingo():
    return render_template('sign/login.html')


@bp.route('/login',methods=['GET','POST']) # 초기화면
def login():
    session.clear()
    if request.method=='GET':
        #임시 자동로그인
        """
        session['userid']='test'
        session['username']='name'
        
        return redirect(url_for('user.home'))
        """
        stat=""
        if request.args.get('join_status'):
            return render_template('sign/login2.html',stat="true")
        else:
            return render_template('sign/login2.html')
    else:
        check=int(request.form['check'])
        print(check)
        if check==1: # 로그인이면 
            id=request.form['id']
            pwd=request.form['pwd']
            # 디비 로그인 체크
            result=db.select_login(id,pwd)
            if result:
                session['userid']=result['id']
                session['username']=result['username']
                session['userimage']=result['userimage']
                session['userstatus']=result['status']
                session['joindate']=result['joindate']
                print(session['userid'])
                return redirect(url_for('user.home'))
            else:
                # 회원아니면#회원아님처리
                    return render_template('alert/alert.html')
        else: # 회원가입이면?
            username=request.form['username']
            id=request.form['id']
            pwd=request.form['pwd']
            if pwd=="" or username=="" or id=="":
                return render_template('/alert/join_error.html')
            # 디비 로그인 체크
            result=db.create_join(username,id,pwd)
            if result:
                #print(session['userid'])
                # 만약, url이 변경되더라도, 변경되는 지점 이외에는 다른 부분은 수정할 필요가 없다.
                return redirect(url_for('sign.login',join_status='true'))
            else:
                # 회원가입 에러 띄우기
                    return render_template('/alert/join_error.html')



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
        if pwd=="" or username=="" or id=="":
            return render_template('/alert/join_error.html')
        # 디비 로그인 체크
        result=db.create_join(username,id,pwd)
        if result:
            #print(session['userid'])
            createDirectory(os.getcwd()+"/static/imgdb/user/"+id)
            # 만약, url이 변경되더라도, 변경되는 지점 이외에는 다른 부분은 수정할 필요가 없다.
            return redirect(url_for('sign.login',join_status='true'))
        else:
            # 회원가입 에러 띄우기
                return render_template('/alert/join_error.html')


@bp.route('/logout')
def logout():
    session.clear()#세션초기화
    return redirect(url_for('login'))