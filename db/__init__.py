import pymysql
from . import sign
host='121.175.81.240'
user='dbmanager'
password='1234'
database='farm_in_sun'
def con():
    connection = pymysql.connect(host=host,
                                 user=user,
                                password=password,
                                database=database,
                                cursorclass=pymysql.cursors.DictCursor)
    return connection

def select_login(id,pwd):
    result = None
    try:
        connection = con()
        with connection:
            with connection.cursor() as cursor:
                # 쿼리중 오류가 나더라도, 커넥션은 정상적으로 닫아야 하므로 예외처리 추가
                try:
                    sql = '''
                        select * from userdata where id=%s and pwd=%s;
                    '''
                    cursor.execute(sql,(id,pwd))
                    result = cursor.fetchone()
                    #print(result)
                except Exception as e1:
                    print(e1)
    except Exception as e:
        print(e)
    return result

def create_join(username,id,pwd):
    result = None
    try:
        connection = pymysql.connect(host=host,
                                    user=user,
                                    password=password,
                                    database=database,
                                    cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                # 쿼리중 오류가 나더라도, 커넥션은 정상적으로 닫아야 하므로 예외처리 추가
                try:
                    sql = '''
                        insert into userdata(username,id,pwd) values (%s,%s,%s);
                    '''
                    cursor.execute(sql,(username,id,pwd))
                    connection.commit() # insert, update ,delete후 커밋이 필수
                    result = "성공"
                    #print(result)
                except Exception as e1:
                    print(e1)
                    result=None
    except Exception as e:
        print(e)
        result=None
    return result

def rend_myplant(id):
    result = None
    try:
        connection = con()
        with connection:
            with connection.cursor() as cursor:
                # 쿼리중 오류가 나더라도, 커넥션은 정상적으로 닫아야 하므로 예외처리 추가
                try:
                    sql = '''
                        select * from plantdata where master_id=%s;
                    '''
                    cursor.execute(sql,(id))
                    result = cursor.fetchall()
                except Exception as e1:
                    print(e1)
                    result=None
    except Exception as e:
        print(e)
        result=None
    return result

# 나의식물 등록(미완성)
def create_myplant(master_id,plant_name,imagename,memo,kind):
    result = None
    try:
        connection = con()
        with connection:
            with connection.cursor() as cursor:
                # 쿼리중 오류가 나더라도, 커넥션은 정상적으로 닫아야 하므로 예외처리 추가
                try:
                    sql = '''
                        insert into plantdata(master_id,plant_name,imagename,memo,kind) values (%s,%s,%s,%s,%s);
                    '''

                    cursor.execute(sql,(master_id,plant_name,imagename,memo,kind))
                    connection.commit() # insert, update ,delete후 커밋이 필수
                    sql='''
                        select plant_no from plantdata where master_id=%s and plant_name=%s and kind=%s;
                    '''
                    cursor.execute(sql,(master_id,plant_name,kind))
                    result = cursor.fetchone()
                    #print(result)
                except Exception as e1:
                    print(e1)
                    result=None
    except Exception as e:
        print(e)
        result=None
    return result

# 로그등록
def create_myplant_log(plant_no,master_id,log,imagename):
    result = None
    try:
        connection = con()
        with connection:
            with connection.cursor() as cursor:
                # 쿼리중 오류가 나더라도, 커넥션은 정상적으로 닫아야 하므로 예외처리 추가
                try:
                    sql = '''
                        insert into plantlog(plant_no,master_id,log,imagename) values (%s,%s,%s,%s);
                    '''

                    cursor.execute(sql,(plant_no,master_id,log,imagename))
                    connection.commit() # insert, update ,delete후 커밋이 필수
                    result = "완료"
                    #print(result)
                except Exception as e1:
                    print(e1)
                    result=None
    except Exception as e:
        print(e)
        result=None
    return result


# 페이징을 위한 게시글카운트
def count_communuty(keyword=None,look_type=1):
    result = None
    try:
        connection = con()
        with connection:
            with connection.cursor() as cursor:
                try:
                    if keyword is None:
                        sql = '''
                            select count(*) as count from communitydata;
                        '''
                        cursor.execute(sql)
                        result = cursor.fetchone()
                    else: # 키워드로 카운트가 들어왔다면
                        if look_type==1: # 타이틀검색
                            sql = '''
                                select count(*) as count from communitydata where title LIKE %s; 
                            '''
                        else: # 내용검색
                            sql = '''
                                select count(*) as count from communitydata where content LIKE %s;
                            '''
                        cursor.execute(sql,('%'+keyword+'%'))
                        result = cursor.fetchone()
                    # print("%s %s %s %s %s @@@@"%(idx,id,title,content,filename))
                except Exception as e1:
                    print(e1)
                    result=None
    except Exception as e:
        print(e)
        result=None
    return result


# 페이징 구현
def rend_community_paging(limit,page,keyword=None,look_type=1):
    result = None
    try:
        connection = con()
        with connection:
            with connection.cursor() as cursor:
                # 쿼리중 오류가 나더라도, 커넥션은 정상적으로 닫아야 하므로 예외처리 추가
                try:
                    if keyword is None:
                        sql = '''
                            select *,(select count(*) from commentdata where a_idx=a.idx) as comcount from communitydata a order by uploaddate desc LIMIT %s OFFSET %s;
                        '''
                        cursor.execute(sql,(limit,page*limit))
                        result = cursor.fetchall()
                    else: # 키워드값이 들어왔다면?
                        if int(look_type)==1: # 제목에서찾기
                            print("으아아아")
                            sql = '''
                                select *,(select count(*) from commentdata where a_idx=a.idx) as comcount from communitydata a where title  LIKE %s order by uploaddate desc LIMIT %s OFFSET %s;
                            '''
                        else:
                            sql = '''
                                select *,(select count(*) from commentdata where a_idx=a.idx) as comcount from communitydata a where content  LIKE %s order by uploaddate desc LIMIT %s OFFSET %s;
                            '''
                        cursor.execute(sql,('%'+keyword+'%',limit,page*limit))
                        result = cursor.fetchall()
                except Exception as e1:
                    print(e1)
                    result=None
    except Exception as e:
        print(e)
        result=None
    return result

# 게시판 전체 들고오기
def rend_communuty(idx="None"):
    result = None
    try:
        connection = con()
        with connection:
            with connection.cursor() as cursor:
                # 쿼리중 오류가 나더라도, 커넥션은 정상적으로 닫아야 하므로 예외처리 추가
                try:
                    if idx=="None":
                        sql = '''
                            select *,(select count(*) from commentdata where a_idx=a.idx) as comcount from communitydata a order by uploaddate desc;
                        '''
                        cursor.execute(sql)
                        result = cursor.fetchall()
                    else:
                        sql = '''
                            select * from communitydata where idx=%s;
                        '''
                        cursor.execute(sql,(idx))
                        result = cursor.fetchone()
                        sql = '''
                            update communitydata set looks=looks+1 where idx=%s;
                        '''
                        cursor.execute(sql,(idx))
                        connection.commit()
                    # print("%s %s %s %s %s @@@@"%(idx,id,title,content,filename))
                except Exception as e1:
                    print(e1)
                    result=None
    except Exception as e:
        print(e)
        result=None
    return result

# 게시판 전체 들고오기
def rend_notice_community(num=5):
    result = None
    try:
        connection = con()
        with connection:
            with connection.cursor() as cursor:
                # 쿼리중 오류가 나더라도, 커넥션은 정상적으로 닫아야 하므로 예외처리 추가
                try:
                    sql = '''
                        select c.*,(select count(*) from commentdata where a_idx=c.idx) as comcount from communitydata c join notice n on c.idx=n.comidx limit %s;
                    
                    '''
                    cursor.execute(sql,(num))
                    result = cursor.fetchall()
                    # print("%s %s %s %s %s @@@@"%(idx,id,title,content,filename))
                except Exception as e1:
                    print(e1)
                    result=None
    except Exception as e:
        print(e)
        result=None
    return result


# 게시판 글 작성 BD 연동
def create_community(id,title,content,filename):
    result = None
    try:
        connection = con()
        with connection:
            with connection.cursor() as cursor:
                # 쿼리중 오류가 나더라도, 커넥션은 정상적으로 닫아야 하므로 예외처리 추가
                try:
                    if filename[-1]=="_":
                        sql = '''
                            insert into communitydata(id,title,content) values (%s,%s,%s);
                        '''
                        cursor.execute(sql,(id,title,content))
                    else:
                        sql = '''
                            insert into communitydata(id,title,content,filename) values (%s,%s,%s,%s);
                        '''
                        cursor.execute(sql,(id,title,content,filename))
                    # print("%s %s %s %s %s @@@@"%(idx,id,title,content,filename))
                    connection.commit() # insert, update ,delete후 커밋이 필수
                    sql = '''
                        select idx from communitydata where id=%s and title=%s and content=%s;
                    '''
                    cursor.execute(sql,(id,title,content))
                    result = cursor.fetchone()
                    print('등록작동',result)
                except Exception as e1:
                    print(e1)
                    result=None
    except Exception as e:
        print(e)
        result=None
    return result

# 게시판 글 공지등록
def insert_notice(idx):
    result = None
    try:
        connection = con()
        with connection:
            with connection.cursor() as cursor:
                # 쿼리중 오류가 나더라도, 커넥션은 정상적으로 닫아야 하므로 예외처리 추가
                try:
                    sql = '''
                        insert into notice(comidx) values (%s);
                    '''
                    cursor.execute(sql,(idx))
                    # print("%s %s %s %s %s @@@@"%(idx,id,title,content,filename))
                    connection.commit() # insert, update ,delete후 커밋이 필수
                    result = "성공"
                except Exception as e1:
                    print(e1)
                    result=None
    except Exception as e:
        print(e)
        result=None
    return result

# 게시판 글 공지삭제
def delete_notice(idx):
    result = None
    try:
        connection = con()
        with connection:
            with connection.cursor() as cursor:
                # 쿼리중 오류가 나더라도, 커넥션은 정상적으로 닫아야 하므로 예외처리 추가
                try:
                    sql = '''
                        delete from notice where comidx=%s;
                    '''
                    cursor.execute(sql,(idx))
                    # print("%s %s %s %s %s @@@@"%(idx,id,title,content,filename))
                    connection.commit() # insert, update ,delete후 커밋이 필수
                    result = "성공"
                except Exception as e1:
                    print(e1)
                    result=None
    except Exception as e:
        print(e)
        result=None
    return result

# 게시판 글 작성 BD 연동
def delete_community(idx):
    result = None
    try:
        connection = con()
        with connection:
            with connection.cursor() as cursor:
                # 쿼리중 오류가 나더라도, 커넥션은 정상적으로 닫아야 하므로 예외처리 추가
                try:
                    sql = '''
                        delete from communitydata where idx=%s;
                    '''
                    cursor.execute(sql,(idx))
                    # print("%s %s %s %s %s @@@@"%(idx,id,title,content,filename))
                    connection.commit() # insert, update ,delete후 커밋이 필수
                    result = "성공"
                    print(result)
                except Exception as e1:
                    print(e1)
                    result=None
    except Exception as e:
        print(e)
        result=None
    return result

# 게시글 상태 가져오기
def getarticle_status(idx):
    result = None
    try:
        connection = con()
        with connection:
            with connection.cursor() as cursor:
                # 쿼리중 오류가 나더라도, 커넥션은 정상적으로 닫아야 하므로 예외처리 추가
                try:
                    sql = '''
                        select comidx from notice where comidx=%s;
                    '''
                    cursor.execute(sql,(idx))
                    result = cursor.fetchone()
                    #print(result)
                except Exception as e1:
                    print(e1)
    except Exception as e:
        print(e)
    return result

# 닉네임 가져오기
def getnickname(idx):
    result = None
    try:
        connection = con()
        with connection:
            with connection.cursor() as cursor:
                # 쿼리중 오류가 나더라도, 커넥션은 정상적으로 닫아야 하므로 예외처리 추가
                try:
                    sql = '''
                        select username from userdata where id=(select id from communitydata where idx=%s);
                    '''
                    cursor.execute(sql,(idx))
                    result = cursor.fetchone()
                    #print(result)
                except Exception as e1:
                    print(e1)
    except Exception as e:
        print(e)
    return result

# 코멘트작성
def comment_write(a_idx,id,username,content):
    result = None
    try:
        connection = con()
        with connection:
            with connection.cursor() as cursor:
                # 쿼리중 오류가 나더라도, 커넥션은 정상적으로 닫아야 하므로 예외처리 추가
                try:
                    sql = '''
                        insert into commentdata(a_idx,id,username,content) values (%s,%s,%s,%s);
                    '''

                    cursor.execute(sql,(a_idx,id,username,content))
                    connection.commit() # insert, update ,delete후 커밋이 필수
                    result = "성공"
                    #print(result)
                except Exception as e1:
                    print(e1)
                    result=None
    except Exception as e:
        print(e)
        result=None
    return result

# 코멘트가져오기
def getcomment(idx):
    result = None
    try:
        connection = con()
        with connection:
            with connection.cursor() as cursor:
                # 쿼리중 오류가 나더라도, 커넥션은 정상적으로 닫아야 하므로 예외처리 추가
                try:
                    sql = '''
                        select a.*,b.userimage from commentdata a , userdata b where a.a_idx=%s and a.id=b.id;
                    '''
                    cursor.execute(sql,(idx))
                    result = cursor.fetchall()
                    #print(result)
                except Exception as e1:
                    print(e1)
    except Exception as e:
        print(e)
    return result

# 좋아요!
def likey(id,idx):
    result = None
    try:
        connection = con()
        with connection:
            with connection.cursor() as cursor:
                # 쿼리중 오류가 나더라도, 커넥션은 정상적으로 닫아야 하므로 예외처리 추가
                try:
                    sql = '''
                        select * from likes where a_idx=%s and userid=%s;
                    '''
                    cursor.execute(sql,(idx,id))
                    result = cursor.fetchall()
                    if result: # 이미 좋아요를 눌렀다면, 삭제
                        sql = '''
                            delete from likes where a_idx=%s and userid=%s;
                        '''
                        cursor.execute(sql,(idx,id))
                        connection.commit() # insert, update ,delete후 커밋이 필수
                        result="off"
                        pass
                    else:# 좋아요를 누른적이 없다면,
                        sql = '''
                            insert into likes(a_idx,userid) values (%s,%s);
                        '''
                        cursor.execute(sql,(idx,id))
                        connection.commit() # insert, update ,delete후 커밋이 필수
                        result = "on"
                except Exception as e1:
                    print(e1)
                    print("@@#@#!@#!@#@!#")
                    result=None
    except Exception as e:
        print(e)
        result=None
    return result
# 게시판 수정(미완성 수정.)
def modify_community(idx,title,content,filename):
    result = None
    try:
        connection = con()
        with connection:
            with connection.cursor() as cursor:
                # 쿼리중 오류가 나더라도, 커넥션은 정상적으로 닫아야 하므로 예외처리 추가
                try:
                    if filename[-1]=="_" or filename=="None":
                        sql = '''
                            update communitydata set title=%s,content=%s,filename=null where idx=%s;
                        '''
                        cursor.execute(sql,(title+("" if "(수정)" in title else "(수정)") ,content,idx))
                    else:
                        sql = '''
                            update communitydata set title=%s,content=%s,filename=%s where idx=%s;
                        '''
                        cursor.execute(sql,(title+("" if "(수정)" in title else "(수정)"),content,filename,idx))
                    # print("%s %s %s %s %s @@@@"%(idx,id,title,content,filename))
                    print("수정완료@@@@@@@@@@@@@@@@@@@@@")
                    connection.commit() # insert, update ,delete후 커밋이 필수
                    result = "성공"
                    print(result)
                except Exception as e1:
                    print(e1)
                    result=None
    except Exception as e:
        print(e)
        result=None
    return result

def modify_userprofile(userid,username,pwd,filename):
    result = None
    try:
        connection = con()
        with connection:
            with connection.cursor() as cursor:
                # 쿼리중 오류가 나더라도, 커넥션은 정상적으로 닫아야 하므로 예외처리 추가
                print("1234")
                print(filename)
                try:
                    if filename is None or filename=="None": # 바꿀이미지 없는 경우
                        print("바꿀이미지없음")
                        sql = '''
                            update userdata set username=%s,pwd=%s,userimage=null where id=%s;
                        '''
                        cursor.execute(sql,(username,pwd,userid))
                    else: # 이미지 있는 경우
                        print('바꿀이미지있음')
                        sql = '''
                            update userdata set username=%s,pwd=%s,userimage=%s where id=%s;
                        '''
                        cursor.execute(sql,(username,pwd,filename,userid))
                    # print("%s %s %s %s %s @@@@"%(idx,id,title,content,filename))
                    print("수정완료@@@@@@@@@@@@@@@@@@@@@")
                    connection.commit() # insert, update ,delete후 커밋이 필수
                    result = "성공"
                    print(result)
                except Exception as e1:
                    print(e1)
                    result=None
    except Exception as e:
        print(e)
        result=None
    return result

# 좋아요 적용
def get_likes(idx):
    result = None
    try:
        connection = con()
        with connection:
            with connection.cursor() as cursor:
                # 쿼리중 오류가 나더라도, 커넥션은 정상적으로 닫아야 하므로 예외처리 추가
                try:
                    sql = '''
                        select count(*) as num from likes where a_idx=%s;
                    '''
                    cursor.execute(sql,(idx))
                    result = cursor.fetchone()
                    sql = '''
                        update communitydata set likes=%s where idx=%s;
                    '''
                    cursor.execute(sql,(result['num'],idx))
                    connection.commit()
                except Exception as e1:
                    print(e1)
    except Exception as e:
        print(e)
    return result

#3일 베스트 게시물
def most_like_community():
    result = None
    try:
        connection = con()
        with connection:
            with connection.cursor() as cursor:
                # 쿼리중 오류가 나더라도, 커넥션은 정상적으로 닫아야 하므로 예외처리 추가
                try:
                    sql = '''
                        select * from communitydata WHERE uploaddate BETWEEN DATE_ADD(NOW(), INTERVAL -3 DAY ) AND NOW() order by likes desc, looks desc limit 10;
                    '''
                    cursor.execute(sql)
                    result = cursor.fetchall()
                except Exception as e1:
                    print(e1)
    except Exception as e:
        print(e)
    return result



if __name__=='__main__':
    select_login('guest','1')
else:
    print("다른사람이 사용시 호출")
    pass
