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

def imagesaver(path,file,beforefilename="X",customfilename="X"):
  #path경로는 ~~~/~~~ 형식으로 끝에 /가 오면 안된다.
  save_path='static/imgdb/'+path
  createDirectory(os.getcwd()+"/static/imgdb/"+path)
  # 커뮤니티 사진저장소 : /static/communitydb/일자(20220417)/게시물번호
  if file.filename is None or file.filename=="":# 저장할 사진이 없다면
    if beforefilename=="X":#기존 사진이 없다면
      print("저장할사진x 기존사진x")
      pass
    else: # 기존사진이 있다면
      print("저장할사진x 기존사진o")
      pass 
  else: # 저장할 사진이 있다면
    if beforefilename=="X" or beforefilename is None or beforefilename=="None":#기존 사진이 없다면
      print("저장할사진o 기존사진x")
      if customfilename!="X":
        file.save(os.path.join(save_path,customfilename))
      else:
        file.save(os.path.join(save_path,file.filename))
      pass
    else: # 기존사진이 있다면
      print("저장할사진o 기존사진o")
      os.remove(os.getcwd()+"/"+save_path+"/"+beforefilename)
      if customfilename!="X":
        file.save(os.path.join(save_path,customfilename))
      else:
        file.save(os.path.join(save_path,file.filename))
      pass 


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
                print(session['userimage'])
                print(f.filename)
                imgpath='static/userprofileimg/' +session['userid']+"/"+f.filename
                imagesaver("user/"+session['userid'],f,session['userimage'])
                if f.filename is None or f.filename=="": # 새 이미지가 없는경우
                    print("넣을 이미지가 비어있다!")
                    print(session['userid'])
                    print(username)
                    print(c1pwd)
                    print(session['userimage'])
                    result=db.modify_userprofile(session['userid'],username,c1pwd,session['userimage'])
                    session['username']=username
                else:# 새 이미지가 있는경우
                    session['userimage']=f.filename
                    result=db.modify_userprofile(session['userid'],username,c1pwd,f.filename)
                    session['username']=username
                '''
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
                    '''
                if result:
                    return redirect(url_for('user.profiledit'))
                
    else:
        return redirect(url_for('login'))

# 로그인 후 이동하는 페이지
@bp.route('/home')
def home():
    if "userid" in session:
        #SSR수행시 값을 전달하는 방법
        data_list=db.most_like_community()
        print(data_list)
        return render_template('user/index.html',userName=session['userid'],data_list=data_list)
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
        else: # 식물등록시,
            print('등록 post 모드')
            kind=request.form['kind']
            print(session['userid'])
            print(kind)
            plantname=request.form['plantname']
            print('plantname:',plantname)
            memo=request.form['memo']
            print("memo:",memo)
            f=request.files['img']
            print('filename',f.filename)
            if f.filename=="None" or f.filename=="":
                return render_template('alert/plantfile_empty.html')
            elif kind is None or kind=="":
                return render_template('alert/plantkind_empty.html')
            elif plantname is None or plantname=="":
                return render_template('alert/plantname_empty.html')
            
            imagesaver("user/"+session['userid']+"/"+plantname,f,customfilename="1_"+f.filename)
            #createDirectory(os.getcwd()+"/static/imgdb/"+session['userid'])
            result=db.create_myplant(session['userid'],plantname,"1_"+f.filename,memo,kind)
            if result:
                result2=db.create_myplant_log(str(result['plant_no']),session['userid'],"start","1_"+f.filename)
                if result2:
                    return render_template('alert/add_success.html')
                else:
                    print('등록실패')
                    return render_template('alert/add_fail.html')
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
    else:#세션정보 있을시, 
        return redirect(url_for('login'))
    
    
#인기글
@bp.route('/best', methods=['GET'])
def best():
    if "userid" in session:
        data_list=db.most_like_community()
        return render_template('user/index.html', data_list=data_list)
    else:#세션정보 있을시, 
        return redirect(url_for('login'))