from flask import Flask, request, render_template, redirect, session, flash
import DBModule
app = Flask(__name__)
app.secret_key = b'aaa!111/'

@app.route('/') 
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST']) 
def login():
    if request.method == "GET": 
        return render_template('pages/login.html')
    else:
        userid = request.form["userid"]
        pwd = request.form["pwd"] 
        result = DBModule.loginUser(userid, pwd)
   
        #result == None : 아이디, 비밀번호 중 틀려서 검색 안 됨
        if result != None:        
            session["userid"] = result[0]
            session["uName"] = result[2]
            session["email"] = result[3]           
            return redirect('/') 
        else:
            #로그인 실패 판업창 띄우기 
            return redirect('/') 

#get : 회원 가입 페이지, post : 회원 가입
@app.route('/join', methods=['GET', 'POST']) 
def join():
    if request.method == "GET":
        return render_template('pages/join.html')
    else:
        userid = request.form["id"]
        pwd = request.form["pwd"] 
        uName = request.form["uName"] 
        email = request.form["email"] 

        joinInfo = [userid, pwd, uName, email]

        result = DBModule.joinUser(joinInfo) 

        if result == 1:
            return render_template('index.html')
        else :
            return render_template('pages/join.html')

#아이디 중복 체크
@app.route('/idCheck', methods=['GET', 'POST']) 
def idCheck():
    if request.method == "GET":
        userid = request.args.get("userid")  #request.form["userid"] -> 쿼리 스트링 값 이걸로 받으려니 에러 발생
        # 1 : 중복, 0 : 사용 가능
        result = DBModule.confirmId(userid)
        return render_template('/pages/idCheck.html', id=userid, resu=result)

#로그아웃
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


#"diagnosisReq, boardList, 대시 보드, 대화 기록" 인형 등록 유무 확인하기
#진단 요청
@app.route('/diagnosisReq', methods=['GET', 'POST']) 
def diagnosisReq():
    requestState = None
    if request.method == "GET":
        regState = DBModule.checkDollRegState(session["userid"])    
        if regState == 1:
            userid = session["userid"]
            requestState = DBModule.diaState(userid)
            return render_template('pages/diagnosisReq.html', reqState=requestState)
        else:           
            flash("인형이 등록되지 않았습니다.")        
            return redirect('/')
    else:
        userid = session["userid"]
        requestState = DBModule.diaRequest(userid)
        return render_template('pages/diagnosisReq.html', reqState=requestState)

#진단 게시판. get : 진단 게시판으로 이동
@app.route('/boardList')
def boardList():
    regState = DBModule.checkDollRegState(session["userid"])    
    if regState == 1:
        blists = ""
        userid = session["userid"]
        boardList = DBModule.boardList(userid)
        return render_template('/pages/board.html', blists = boardList)
    else:
        flash("인형이 등록되지 않았습니다.")        
        return redirect('/')


#진단 게시글 보기
@app.route('/boardView')
def boardView():
    blists = ""
    boardNum = request.args.get("boardNum")   
    board = DBModule.getBoard(boardNum)

    return render_template('/pages/boardView.html', boardEnt=board)

#완료된 진단 요청 삭제
@app.route('/reqDelete', methods=['GET', 'POST']) 
def reqDelete():
    if request.method == "GET":
        userid = session["userid"]
        DBModule.reqDelete(userid)

        return redirect('boardList')

#회원 정보 수정
@app.route('/modifyMember', methods=['GET', 'POST'])
def modifyMember():
    if request.method == "GET":   
        regState = DBModule.checkDollRegState(session["userid"])
        return render_template('/pages/mypageModify.html', rgd=regState)
    else:
        uName = request.form["uName"] 
        email = request.form["email"] 
        userid = request.form["userid"]
        modifyInfo = [uName, email, userid]
        
        result = DBModule.modifyMember(modifyInfo)
        session["uName"] = result[2]
        session["email"] = result[3]           
        
        return redirect("modifyMember") 
    
#인형 등록 
@app.route('/doolReg', methods=['GET', 'POST'])
def doolReg():
    message = ""
    dollNumber = request.form['dollNumber']
    result = DBModule.regDoll(session["userid"], dollNumber)
    
    if result == 1: 
        message = "인형 등록 완료"
    elif result == 2:
        message = "사용 불가능한 인형"
    else: 
        message = "인형 등록 실패"

    flash(message)        
    return redirect("modifyMember")


#관리자 페이지 및 기능
@app.route('/adminPage') 
def adminPage():
    return render_template('admin/adminPage.html')

#로그인
@app.route('/adminlogin', methods=['GET', 'POST']) 
def adminlogin():
    adminid = request.form["adminid"]
    pwd = request.form["pwd"] 
    result = DBModule.loginAdmin(adminid, pwd)
   
    if result != None:        
        session["adminId"] = result[0]
        return render_template('admin/adminPage.html')
    else:
        return render_template('admin/adminPage.html')

#요청 목록 확인
@app.route('/reqList', methods=['GET', 'POST']) 
def reqList():
    if request.method == "GET":
        reqList = DBModule.reqList()
        return render_template('admin/reqList.html', requestList = reqList)

#요청에 대한 진단글 쓰기
@app.route('/resWrite', methods=['GET', 'POST']) 
def resWrite():
    if request.method == "GET":
        user = request.args.get("user")   
        return render_template('admin/resWrite.html', userid=user)
    else:
        userid = request.form["userid"] 
        resContent = request.form["resContent"] 

        DBModule.resWrite(userid, resContent)

        reqList = DBModule.reqList()
        return render_template('admin/reqList.html', requestList = reqList)



#회원 기능, 진단 요청, 인형 등록, 등록 시 사이트 기능 이용하도록 등등 구현 완료
# 라즈베리파이단에서 기능 구현해서 DB에 값 넘겨주면 다음 아래 체크리스트 구현
# 5.1. 대시보드 구현하기. (부트스트랩 템플릿)
# 6.1. 대화 기록 구현하기.(??)
# 6.2. 다이얼로그 플로우. (안 해도 된다고 함)

# 기타 
#진단 요청 AJAX 사용하기.
#pwd 보안 적용하기
#단순 CRUD에서 업그레이드, 회원 탈퇴 기능



