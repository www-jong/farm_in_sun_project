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
                    print("%s %s %s @@@@"%(username,id,pwd))
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

if __name__=='__main__':
    select_login('guest','1')
else:
    print("다른사람이 사용시 호출")
    pass