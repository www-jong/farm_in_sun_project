from flask import Flask,render_template,request,jsonify,redirect,url_for,Blueprint
from ml import predict_lang,trans_lang
from flask import session
import db,os
from email.policy import default
import queue,math
from unittest import result
from datetime import timedelta,datetime
from flask_paginate import Pagination, get_page_parameter
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

@bp.route('/tip')
def tip():
  return render_template('/public/tip.html', userName="사용자명")

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
 
row_page=5
# 커뮤니티 리스트
@bp.route('/community',methods=['GET','POST'])
def community():
  if "userid" in session:
    if request.method=='GET':   
      page=request.args.get('page',default=1,type=int) # 페이지
      result=db.rend_communuty()
      limit=5 # 한페이지에 보일 게시글수
      c_list=db.rend_community_paging(limit,page-1)
      looks_page=5 # 최대 표시할 페이지수
      total_cnt=len(result) # 총 게시글수
      print("총 게시글수 %d"%(len(result)))
      #pagination=rPagination(page=page,total=total_cnt,search="True",recode_name="community_list")
      print('총 페이지수 %d'%(math.ceil(len(result)//5)))
      return render_template('/public/community.html', userName=session['userid'],lp=looks_page//2 ,community_list=c_list,c_list=c_list,page=page,maxpage=math.ceil(1+len(result)//5))
    else:
      pass
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
      print(result)
      nickname=db.getnickname(idx)# 해당 게시글의 닉네임을 얻어오는 로직
      print(nickname)
      comments=db.getcomment(idx)
      print(comments)
      likes=db.get_likes(idx)['num']
      return render_template('/public/community_view.html', userName=session['userid'],
                                                         article=result,nickname=nickname,comments=comments,likes=likes,page=page)
    else: # 댓글 등록시, 
      a_idx=request.form['articlenum']
      id=session['userid']
      username=session['username']
      content=request.form['comment']
      result=db.comment_write(a_idx,id,username,content)
      if result:
        return render_template('alert/add_success.html')
      else:
        return render_template('alert/add_fail.html')
  else:
    return redirect(url_for('login'))

# 게시글 작성
@bp.route('/community_write', methods=['GET','POST'])
def community_write():
  if "userid" in session:
    if request.method=='GET':
      return render_template('/public/community_write.html', userName=session['userid'])
    else:# 게시글 등록 시,
        title=request.form['title']
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
          return render_template('/public/community.html', userName=session['userid'], community_list=result)
  else:
    return redirect(url_for('login'))

# 게시글 수정
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
