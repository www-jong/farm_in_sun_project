# 패키지를 의미하는 파일
# 파이썬 3.3 이하에서는 2.x버전에 하위호환용
# 3.3 이상에ㅓ는 없어도 된다
# 여기에 최종적인 디비연동코드가 들어간다

# 1. 모듈가져오기
import pymysql

host='121.175.81.240'
user='dbmanager'
password='1234'
database='farm_in_sun'

def select_login(id,pwd):
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
def create_myplant(master_name,master_id,plant_name,imagepath,memo):
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
                        insert into plantdata(master_name,master_id,plant_name,imagepath,memo) values (%s,%s,%s,%s,%s);
                    '''

                    cursor.execute(sql,(master_name,master_id,plant_name,imagepath,memo))
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

# 게시판 리스트 DB 연동
def rend_communuty(idx="None"):
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
                    if idx=="None":
                        sql = '''
                            select * from communitydata order by uploaddate desc;
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

# 게시판 글 작성 BD 연동
def create_community(id,title,content,filename):
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
                    result = "성공"
                    print(result)
                except Exception as e1:
                    print(e1)
                    result=None
    except Exception as e:
        print(e)
        result=None
    return result

# 닉네임 가져오기
def getnickname(idx):
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
                        select * from commentdata where a_idx=%s;
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
def modify_community(id,title,content,filename):
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
                    if filename[-1]=="_":
                        sql = '''
                            update communitydata(id,title,content) values (%s,%s,%s);
                        '''
                        cursor.execute(sql,(id,title+"(수정)",content))
                    else:
                        sql = '''
                            insert into communitydata(id,title,content,filename) values (%s,%s,%s,%s);
                        '''
                        cursor.execute(sql,(id,title+"(수정)",content,filename))
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

# 코멘트가져오기
def get_likes(idx):
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

if __name__=='__main__':
    select_login('guest','1')
else:
    print("다른사람이 사용시 호출")
    pass
