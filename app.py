from flask import Flask,render_template,request,jsonify,redirect,url_for
from ml import predict_lang,trans_lang
from flask import session
import db
from datetime import timedelta



app = Flask(__name__)
app.secret_key='너무나도보안적인시크릿키'


@app.before_request
def make_session_permanent(): #세션의 만료시간 설정 : 60분
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=2)


# 첫화면(로그인페이지)
@app.route('/',methods=['GET','POST'])
def login():
    session.clear()
    if request.method=='GET':
        id= request.args.get('id')
        return render_template('login.html')
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
            return redirect(url_for('home'))
        else:
            # 회원아니면
                #회원아님처리
                return render_template('ejs/alert.html')

# 로그인 후 이동하는 페이지
@app.route('/home')
def home():
    if "userid" in session:
        #SSR수행시 값을 전달하는 방법
        return render_template('index.html',userName=session['userid'])
    else:#세션정보 있을시, 
        return redirect(url_for('login'))

@app.route('/join', methods=['GET','POST'])
def join():
    if request.method=='GET':
        id= request.args.get('id')
        print("회원가입시도")
        return render_template('join.html')
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
            return render_template('login.html',info="가입성공")
        else:
            # 회원가입 에러 띄우기
                return render_template('/ejs/join_error.ejs')

@app.route('/logout')
def logout():
    session.clear()#세션초기화
    return redirect(url_for('login'))







@app.route('/service/ml', methods=['GET','POST'])
def ml():    
    if request.method == 'GET':
        return render_template('ml.html', userName="사용자명")
    else:
        # 1. 클라이언트가 보낸 데이터 획득
        msg=request.form.get('msg')
        print(msg)
        # 2. 예측 처리함수에 데이터 넣어서 호출
        # y_pred : ['en']
        y_pred=predict_lang(msg)
        print(y_pred)
        # 3. 결과를 받아서
        res = {
            'code':1,
            'na':y_pred[0] if y_pred else '예측오류'
        }
        return jsonify(res)

@app.route('/service/ml/trans', methods=['POST'])
def trans():
    # 클라이언트가 보낸 데이터 획득
    s_code = request.form.get('s_code')
    msg    = request.form.get('msg')
    # 번역
    data   = trans_lang( msg, s_code )
    return jsonify({
        'code': 1,
        'msg' : data
    })


if __name__=='__main__':
    app.run(debug=True)
    #app.run()