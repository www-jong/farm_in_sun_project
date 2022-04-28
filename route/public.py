from email.policy import default
import queue
from socket import AI_PASSIVE
from unittest import result
from flask import Flask,render_template,request,jsonify,redirect,url_for,Blueprint
from ml import predict_lang,trans_lang
from flask import session
import db,os,math
from email.policy import default
import queue,math
from unittest import result
from datetime import timedelta,datetime

import smtplib
from email.mime.text import MIMEText

bp = Blueprint('public', __name__, url_prefix='/public')
def createDirectory(directory):
    try: 
        if not os.path.exists(directory): 
            os.makedirs(directory) 
    except OSError: 
        print("Error: Failed to create the directory.")
now=datetime.now()
nowDatetime = now.strftime('%Y%m%d%H%M%S')
nowDatetime2 = now.strftime('%Y%m%d')

def imagesaver(path,file,beforefilename="X"):
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
      file.save(os.path.join(save_path,nowDatetime+"_"+session['userid']+"_"+file.filename))
      pass
    else: # 기존사진이 있다면
      print("저장할사진o 기존사진o")
      os.remove(os.getcwd()+"/"+save_path+"/"+beforefilename)
      file.save(os.path.join(save_path,nowDatetime+"_"+session['userid']+"_"+file.filename))
      pass 


# @bp.route('/tip')
# def tip():
#   return render_template('/public/tip.html', userName="사용자명")

@bp.route('/tip_ver2')
def tip2():
  return render_template('/public/tip-ver2.html', userName="사용자명")

@bp.route('/sang')
def sang():
  return render_template('/public/sang.html', userName="사용자명")

@bp.route('/chung')
def chung():
  return render_template('/public/chung.html', userName="사용자명")


@bp.route('/ggae')
def ggae():
  return render_template('/public/ggae.html', userName="사용자명")  
 
@bp.route('/back')
def back():
  return render_template('/alert/back.html', userName="사용자명")  


limit=5 # 한페이지에 보일 게시글수
looks_page=7 # 최대 표시할 페이지수
# 커뮤니티 리스트
@bp.route('/community',methods=['GET','POST'])
def community():
  if "userid" in session:
    if request.method=='GET':   

      keyword=request.args.get('keyword',default=None,type=str)
      lk=request.args.get('lk',default=1,type=str)
      page=request.args.get('page',default=1,type=int) # 페이지
      result=db.count_communuty(keyword=keyword,look_type=lk)
      c_list=db.rend_community_paging(limit=limit,page=page-1,keyword=keyword,look_type=lk)
      noti_list=db.rend_notice_community(3)
      print('maxpage : ',int(math.ceil(result['count']/limit)))
      print(result['count'])
      return render_template('/public/community.html',userstatus=session['userstatus'],noti_list=noti_list,lk=lk,keyword=keyword, userName=session['userid'],lp=looks_page//2 ,community_list=c_list,c_list=c_list,page=page,maxpage=int(math.ceil(result['count']/limit)))
    else: #게시글 검색기능, 작성기능
      type=int(request.form['type'])
      if type==1: # 작성기능일경우
        title=request.form['title']
        if title=="": # 제목이 비어있을 경우 다시쓰기
          return render_template('alert/community_write_nonetitle.html')
        content=request.form['content']
        f=request.files['img']
        result=db.create_community(session['userid'],title,content,nowDatetime+"_"+session['userid']+"_"+f.filename)
        print('*(*&(^')
        print(result)
        print(f.filename)
        if f.filename=="None":
          print("None 1번")
        elif f.filename is None:
          print("None 2번")
        elif f.filename =="":
          print("None 3번")
        elif f.filename:
          print("None 4번")
        
        # 이미지등록함수 경로, 새로올릴파일, 기존파일이름
        imagesaver('community/'+nowDatetime2+"/"+str(result['idx']),f)
        if result:
          result=db.rend_communuty()
          return redirect(url_for('public.community'))
      elif type==2:
        print("검색기능 작동")
        keyword=request.form['keyword']
        lk=request.form['look_type']
        #sc=request.form['searchcheck']
        if request.form['searchcheck']:
          page=1
        else:
          page=request.args.get('page',default=1,type=int) # 페이지
        result=db.count_communuty(keyword=keyword,look_type=lk)
        print("^^"*20)
        print('페이지 :',page)
        print('검색유형 :',lk)
        print('검색 키워드 :',keyword)
        print('검색된 게시물 수 :',result)
        c_list=db.rend_community_paging(limit=limit,page=page-1,keyword=keyword,look_type=lk)
        noti_list=db.rend_notice_community(3)
        print(keyword)
        print(c_list)
        return render_template('/public/community.html',userstatus=session['userstatus'],noti_list=noti_list,lk=lk,keyword=keyword, userName=session['userid'],lp=looks_page//2 ,community_list=c_list,c_list=c_list,page=page,maxpage=int(math.ceil(result['count']/limit)))
  else:
    return redirect(url_for('login'))

# 게시글 리스트 글 보기  
@bp.route('/community_view',methods=['GET','POST'])
def community_view():
  if "userid" in session:
    if request.method=='GET':  # 해당게시글 클릭시,  
      idx = request.args.get('idx', type = str)
      page = request.args.get('page', type = int)
      print(idx)
      result=db.rend_communuty(idx)
      artiuserprof=db.getuserprofile(result['id'])
      print('***')
      print(artiuserprof['userimage'])
      print(result)
      nickname=db.getnickname(idx)# 해당 게시글의 닉네임을 얻어오는 로직
      print(nickname)
      comments=db.getcomment(idx)
      print(comments)
      article_status=0
      if db.getarticle_status(idx):
        article_status=1
      likes=db.get_likes(idx)['num']
      return render_template('/public/community_view.html',article_status=article_status, userName=session['userid'],userstatus=session['userstatus'],
                                                         article=result,nickname=nickname,comments=comments,likes=likes,page=page,artipro=artiuserprof['userimage'])
    else: # 댓글 등록시, 
      type=int(request.form['type'])
      if type==1: # 게시글 수정부분
        idx=request.form['idx']
        title=request.form['title']
        content=request.form['content']
        f=request.files['img']
        beforefile=request.form['beforefilename']
        beforedate=request.form['beforedate']
        imagesaver('community/'+beforedate+"/"+idx,f,beforefile)
        if beforefile: # 기존파일이 있을때,
          if f.filename=="": # 등록할 파일이 없다면
            result=db.modify_community(idx,title,content,beforefile)
          else: # 등록할 파일이 있다면
            result=db.modify_community(idx,title,content,nowDatetime+"_"+session['userid']+"_"+f.filename)
        else:
          result=db.modify_community(idx,title,content,nowDatetime+"_"+session['userid']+"_"+f.filename)
        return redirect(url_for('public.community_view',idx=idx)) 
      elif type==2: # 댓글 작성기능
        a_idx=request.form['articlenum']
        id=session['userid']
        username=session['username']
        content=request.form['comment']
        result=db.comment_write(a_idx,id,username,content)
        if result:
          return render_template('alert/add_success.html')
        else:
          return render_template('alert/add_fail.html')
      elif type==3: # 공지등록
        idx=request.form['idx']
        result=db.insert_notice(idx)
        if result:
          return render_template('alert/add_notice.html')
      elif type==4:# 공지삭제
        idx=request.form['idx']
        result=db.delete_notice(idx)
        if result:
          return render_template('alert/delete_notice.html')
  else:
    return redirect(url_for('login'))

# 게시글 작성 -> 모달로 이동됨
'''
@bp.route('/community_write', methods=['GET','POST'])
def community_write():
  if "userid" in session:
    if request.method=='GET':
      return render_template('/public/community_write.html', userName=session['userid'])
    else:# 게시글 등록 시,
        title=request.form['title']
        if title=="": # 제목이 비어있을 경우 다시쓰기
          return render_template('alert/community_write_nonetitle.html')
        content=request.form['content']
        f=request.files['img']
        imgpath='static/communitydb/' +nowDatetime2+"/"+nowDatetime+"_"+session['userid']+"_"+f.filename
        createDirectory(os.getcwd()+"/static/communitydb/"+nowDatetime2)
        if imgpath[-1]!="_":
          print("^"*20)
          print(imgpath)
          f.save(imgpath)
        result=db.create_community(session['userid'],title,content,nowDatetime2+'/'+nowDatetime+"_"+session['userid']+"_"+f.filename)
        if result:
          result=db.rend_communuty()
          return redirect(url_for('public.community'))
  else:
    return redirect(url_for('login'))
'''

# 게시글 수정 -> 모달로 이동됨
'''
@bp.route('/community_modify',methods=['GET','POST'])
def community_modify():
  if "userid" in session:
    if request.method=='GET': # 수정창으로 이동
      idx = request.args.get('idx', type = str)
      result=db.rend_communuty(idx)
      print("*"*25)
      print(result)
      #result=db.modify_community(session['userid'])
      return render_template('/public/community_modify.html', userName=session['userid'],result=result)
    else: # 수정적용시,
      idx=request.form['idx']
      title=request.form['title']
      content=request.form['content']
      f=request.files['img']
      beforefile=request.form['beforefilename']
      imgpath='static/communitydb/' +nowDatetime2+"/"+nowDatetime+"_"+session['userid']+"_"+f.filename
      createDirectory(os.getcwd()+"/static/communitydb/"+nowDatetime2)
      f.save(imgpath)        
      result=db.modify_community(idx,title,content,nowDatetime2+'/'+nowDatetime+"_"+session['userid']+"_"+f.filename)
      print("-"*20)
      print(beforefile)
      if beforefile!="None": # 이전에 이미 사진이 등록되어있었다면, 사진삭제
          os.remove(os.getcwd()+"/static/communitydb/"+beforefile)
      return redirect(url_for('public.community_view',idx=idx)) 
  else:
    return redirect(url_for('login')) 
'''

# 게시글 삭제
@bp.route('/community_delete')
def community_delete():
  if "userid" in session:
    idx = request.args.get('idx', type = str)
    result=db.delete_community(idx)
    print("*삭제"*25)
    print(result)
    return redirect(url_for('public.community',res="삭제성공"))
  else:
    return redirect(url_for('login')) 

# 게시글 댓글 삭제
@bp.route('/reply_delete')
def reply_delete():
  if "userid" in session:
    idx = request.args.get('idx', type = str)
    result=db.delete_reply(idx)
    print(result)
    if result:
      return render_template('alert/reply_delete.html')
  else:
    return redirect(url_for('login')) 

# 좋아요!
@bp.route('/likey')
def likey():
  if "userid" in session:
    idx = request.args.get('idx', type = str)
    result=db.likey(session['userid'],idx)
    print("@@@@@@@@@@@@@@@@@@@@@@@@")
    print(result)
    if result=="on":
      return render_template('alert/likey_on.html')
    else:
      return render_template('alert/likey_off.html')
  else:
    return redirect(url_for('login')) 

# contact us
@bp.route('/contactus',methods=['GET','POST'])
def contactus():
  if request.method=='GET':  # 해당게시글 클릭시, 
   return render_template('/public/contactus.html', userName="사용자명")
  else:
    email=request.form['email']# 메일계정아이디,비밀번호와 동일한 이메일주솔르 적어야함
    subject=request.form['subject']
    content=request.form['content']
    s=smtplib.SMTP('smtp.naver.com',587)
    sender_id='test' # 메일계정아이디
    sender_pw='testpasswd' # 메일계정비밀번호
    smtp_info = {
    "smtp_server": 'smtp.naver.com',  # SMTP 서버 주소
    "smtp_user_id": sender_id,
    "smtp_user_pw": sender_pw,
    "smtp_port": 587 # SMTP 서버 포트
    }
    msg=MIMEText(content,_charset="utf8")
    msg['subject']=subject 
    msg['From']=email
    msg['To']='weon1009@gmail.com'
    smtp = smtplib.SMTP(smtp_info['smtp_server'], smtp_info['smtp_port'])
    smtp.ehlo
  smtp.starttls()  # TLS 보안 처리
  smtp.login(sender_id , sender_pw)  # 로그인
  smtp.sendmail(msg['From'], msg['To'].split(','), msg.as_string())
  smtp.quit()
  return render_template('alert/email_success.html')