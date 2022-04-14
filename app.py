from flask import Flask,render_template,request,jsonify,redirect,url_for
from ml import predict_lang,trans_lang
from flask import session
import db
from datetime import timedelta

from route import public
from route import sign
from route import user


app=Flask(__name__)
app.secret_key='너무나도보안적인시크릿키'

@app.before_request
def make_session_permanent(): #세션의 만료시간 설정 : 60분
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=2)


@app.route('/',methods=['GET','POST']) # 초기화면
def login():
    session.clear()

    return render_template('intro.html')


app.register_blueprint(public.bp)
app.register_blueprint(sign.bp)
app.register_blueprint(user.bp)


"""
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
"""

if __name__=='__main__':
    app.run(debug=True)
    #app.run()