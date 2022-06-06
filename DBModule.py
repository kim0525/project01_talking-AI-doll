import pymysql

def connection():
    return pymysql.connect(host='localhost',
                        user='root', password='1234',
                        db='tori', charset='utf8')


def loginUser(userid, pwd):
        ret = ()    
        try:
            db = connection()
            conn = db.cursor()
            # DB CONNECTION
            setdata = (userid, pwd)
            conn.execute('SELECT * FROM memberTBL WHERE userid = %s AND pwd = %s', setdata) # 쿼리 실행
            ret = conn.fetchone() # SELECT 결과 받음

            print(ret)
        except Exception as e:
            print('db error:', e)
        finally:
            conn.close()
            return ret 


#회원가입
def joinUser(joinInfo):
    ret = ()
    result = 0
    
    try:
        db = connection()
        conn = db.cursor()
        # DB CONNECTION

        setdata = (joinInfo[0], joinInfo[1], joinInfo[2], joinInfo[3])
        conn.execute('INSERT INTO memberTBL (userid, pwd, uName, email) VALUES (%s, %s, %s, %s)', setdata) # 튜플 안 쓰니 execute() takes from 2 to 3 positional arguments but 6 were given라고 에러 발생함
        db.commit() #파이썬은 AUTO COMMIT 기본 제공 안 함
        
        conn.execute('SELECT * FROM memberTBL WHERE userid = %s', joinInfo[0]) # 쿼리 실행 
        ret = conn.fetchone() # SELECT 결과 받음

        # 1:회원가입 성공, 0:회원가입 실패
        if ret:
            result = 1 # !!비밀번호 암호화 하기
        else:
            result = 0

        print(str(result) + " (1 가입 성공, 0 가입 실패)")    
    except Exception as e:
        print('db error:', e)
    finally:
        conn.close()
        return result         


#아이디 확인
def confirmId(userid):
        ret = ()    
        result = 0
        try:
            db = connection()
            conn = db.cursor()
            # DB CONNECTION

            conn.execute('SELECT * FROM memberTBL WHERE userid = %s', userid) # 쿼리 실행 
            ret = conn.fetchone() # SELECT 결과 받음

            if ret:
                result = 1
            else:
                result = 0

            print(str(result) + " (1 중복 걸림, 0 중복 통과)")    
        except Exception as e:
            print('db error:', e)
        finally:
            conn.close()
            return result


#회원 수정
def modifyMember(modifyInfo):
    ret = ()
    try:
        db = connection()
        conn = db.cursor()
        # DB CONNECTION

        setdata = (modifyInfo[0], modifyInfo[1], modifyInfo[2])
        conn.execute('UPDATE memberTBL SET uName = %s, email= %s WHERE userid = %s', setdata) 
        db.commit()

        conn.execute('SELECT * FROM memberTBL WHERE uName = %s', modifyInfo[0]) # 쿼리 실행 
        ret = conn.fetchone() # SELECT 결과 받음
        
        print(ret)
    except Exception as e:
        print('db error:', e)
    finally:
        conn.close()
        return ret    
    

#인형 등록 상태 확인
def checkDollRegState(userid):
    ret = ()    
    result = 0
    try:
        db = connection()
        conn = db.cursor()
        # DB CONNECTION
        conn.execute('SELECT * FROM dollNumberTBL WHERE dollRegUser = %s', userid) # 쿼리 실행 
        ret = conn.fetchone() # SELECT 결과 받음

        #등록 O : 1, 등록 X : 0
        if ret: 
            result = 1
        else:
            result = 0
    except Exception as e:
        print('db error:', e)
    finally:
        print(result)
        conn.close()
        return result

#인형 등록
def regDoll(userid, dollNumber):
    ret = ()
    result = 0
    
    try:
        db = connection()
        conn = db.cursor()
        # DB CONNECTION

        conn.execute('SELECT * FROM dollNumberTBL WHERE dollNumber = %s', dollNumber) # 쿼리 실행 
        ret = conn.fetchone() # SELECT 결과 받음
        print(ret[1])

        #등록된 인형 : 2, 등록 성공 : 1, 등록 실패 : 0
        if ret[1] is None:
            setdata = (userid, dollNumber)                  
            if ret:
                conn.execute('UPDATE dollNumberTBL SET dollRegUser = %s, isReg=1 WHERE dollNumber = %s', setdata) 
                db.commit()
                result = 1
        else:
            result = 2 
             
    except Exception as e:
        print('db error:', e)
    finally:
        print(result)
        conn.close()
        return result 


#진단 상태
def diaState(userid):
        ret = 0
        try:
            db = connection()
            conn = db.cursor()
            # DB CONNECTION

            conn.execute('SELECT * FROM requestTBL WHERE reqUser = %s', userid) # 쿼리 실행 
            ret = conn.fetchone()
        except Exception as e:
            print('db error:', e)
        finally:
            conn.close()
            return ret

#진단 요청
def diaRequest(userid):
    ret = 0
    try:
        db = connection()
        conn = db.cursor()
        # DB CONNECTION
        conn.execute('INSERT INTO requestTBL (reqUser) VALUES (%s)', userid) 
        db.commit() 
            
        conn.execute('SELECT * FROM requestTBL WHERE reqUser = %s', userid) # 쿼리 실행 
        ret = conn.fetchone()

    except Exception as e:
        print('db error:', e)
    finally:
        conn.close()
        return ret


#완료된 진단 요청 삭제
def reqDelete(userid):
    try:
        db = connection()
        conn = db.cursor()
        # DB CONNECTION

        conn.execute('DELETE FROM requestTBL WHERE reqUser = %s', userid) 
        db.commit()

    except Exception as e:
        print('db error:', e)
    finally:
        conn.close()
        return ""


#진단 게시글 목록 조회
def boardList(userid):
    ret = ()
    result = 0   
    try:
        db = connection()
        conn = db.cursor()
        # DB CONNECTION

        conn.execute('SELECT * FROM boardTBL WHERE reqUser=%s ORDER BY boardNum DESC', userid)
        ret = conn.fetchall() 

        #for i in ret:
        #    print(i)

    except Exception as e:
        print('db error:', e)
    finally:
        conn.close()
        return ret     


#진단 상세보기
def getBoard(boardNum):
    ret = ()
    result = 0   
    try:
        db = connection()
        conn = db.cursor()
        # DB CONNECTION

        conn.execute('SELECT * FROM boardTBL WHERE boardNum=%s', boardNum)
        ret = conn.fetchone() 

    except Exception as e:
        print('db error:', e)
    finally:
        conn.close()
        return ret     

#
#관리자 로그인
def loginAdmin(adminid, pwd):
        ret = ()    
        try:
            db = connection()
            conn = db.cursor()
            # DB CONNECTION
            setdata = (adminid, pwd)
            conn.execute('SELECT * FROM adminTBL WHERE adminId = %s AND pwd = %s', setdata) # 쿼리 실행
            ret = conn.fetchone() # SELECT 결과 받음

            print(ret)
        except Exception as e:
            print('db error:', e)
        finally:
            conn.close()
            return ret 


#들어온 요청 목록 리스트
def reqList():
    ret = ()
    result = 0   
    try:
        db = connection()
        conn = db.cursor()
        # DB CONNECTION

        conn.execute('SELECT * FROM requestTBL ORDER BY requestNum DESC')
        ret = conn.fetchall()
        
        for i in ret:
            print(i)

    except Exception as e:
        print('db error:', e)
    finally:
        conn.close()
        return ret     


#진단 작성
def resWrite(userid, resContent):
    ret = ()
    result = 0   
    try:
        db = connection()
        conn = db.cursor()
        # DB CONNECTION

        setdata = (resContent, userid)
        conn.execute('INSERT INTO boardTBL (content, reqUser) VALUES (%s, %s)', setdata) 
        conn.execute("UPDATE requestTBL SET reqState='1' WHERE reqUser = %s", userid) 
        db.commit()

    except Exception as e:
        print('db error:', e)
    finally:
        conn.close()
        return ""    
    