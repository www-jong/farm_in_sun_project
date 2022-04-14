from flask import Flask,render_template,request,jsonify,redirect,url_for,Blueprint
from ml import predict_lang,trans_lang
from flask import session
import db,os
from email.policy import default
import queue,math
from unittest import result
from datetime import timedelta,datetime
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


# 커뮤니티 리스트
@bp.route('/community')
def community():
  if "userid" in session:
    result=db.rend_communuty()

    # # 페이지 값 (디폴트값 = 1)
    # page = request.args.get("page",1,type=int)
    # # 한 페이지 당 몇개의 게시물 출력
    # limit = 10

    # # 컬렉션 모두 가져옴
    # datas = result.find({}).skip((page -1) * limit).limit(limit)

    # # 게시물 총 개수 세기
    # tot_count = result.find({}).count()
    # # 마지막 페이지의 수 구하기
    # last_page_num = math.ceil(tot_count / limit) # 반올림

    # # 페이지 블럭 5개씩 표기
    # block_size = 5
    # # 현재 블럭의 위치 (첫 번째 블럭이라면, block_num = 0)
    # block_num = int((page - 1) / block_size)
    # # 현재 블럭의 맨 처음 페이지 넘버 (첫 번째 블럭이라면, block_start = 1, 두 번째 블럭이라면, block_start = 6)
    # block_start = (block_size * block_num) + 1
    # # 현재 블럭의 맨 끝 페이지 넘버 (첫 번째 블럭이라면, block_end = 5)
    # block_end = block_start + (block_size - 1)
    # return render_template(
    #     "/public/community.html",
    #     datas=datas,
    #     limit=limit,
    #     page=page,
    #     block_start=block_start,
    #     block_end=block_end,
    #     last_page_num=last_page_num,
    #     userName=session['userid'],
    #     community_list=result)
    return render_template('/public/community.html', userName=session['userid'], community_list=result)

  else:
    return redirect(url_for('login'))

# 게시글 리스트 글 보기  
@bp.route('/community_view',methods=['GET','POST'])
def community_view():
  if "userid" in session:
    if request.method=='GET':  # 해당게시글 클릭시,  
      idx = request.args.get('idx', type = str)
      print(idx)
      result=db.rend_communuty(idx)
      print(result)
      nickname=db.getnickname(idx)# 해당 게시글의 닉네임을 얻어오는 로직
      print(nickname)
      comments=db.getcomment(idx)
      print(comments)
      likes=db.get_likes(idx)['num']
      return render_template('/public/community_view.html', userName=session['userid'],
                                                         article=result,nickname=nickname,comments=comments,likes=likes)
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
      title=request.form['title']
      content=request.form['content']
      f=request.files['img']
      beforefile=request.form['beforefilename']
      imgpath='static/communitydb/' +nowDatetime2+"/"+nowDatetime+"_"+session['userid']+"_"+f.filename
      createDirectory(os.getcwd()+"/static/communitydb/"+nowDatetime2)
      f.save(imgpath)        
      result=db.modify_community(session['userid'],title,content,nowDatetime2+'/'+nowDatetime+"_"+session['userid']+"_"+f.filename)
      if beforefile: # 이전에 이미 사진이 등록되어있었다면, 사진삭제
        os.remove(os.getcwd()+"/static/communitydb/"+beforefile)
      return "dd"
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
