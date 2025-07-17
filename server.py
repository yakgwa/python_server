from flask import Flask
from flask import render_template # html 문서를 로드!!
from flask import request # 요청 받은 값을 담고 있는 라이브러리
from flask import redirect, make_response
# from aws import detect_labels_local_file as label
from aws import compare_faces
from werkzeug.utils import secure_filename
# 단, templates 폴더에 있는 html만 바라볼 수 있다
# 터미널에서 mkdir templates

app = Flask(__name__) # private한 변수이고 class로 받았으므로 변수로 받을 수 있음

# 서버 주소 / -> 하나당 함수 하나 매핑
# return html문서
@app.route("/")
def index():
    return render_template("home.html")

@app.route("/compare", methods=["POST"])

def compare():

    try:

        if request.method == "POST":
            f1 = request.files["file1"]
            f2 = request.files["file2"]
            f1_filename = secure_filename(f1.filename)
            f2_filename = secure_filename(f2.filename)

            f1.save("static/" + f1_filename)
            f2.save("static/" + f2_filename)

            r = compare_faces("static/" + f1_filename, "static/" + f2_filename)
            return r

    except:

        return "얼굴 비교 실패"

    return "얼굴 비교 페이지"

@app.route("/detect", methods=["POST"])
def detect():
    try:
        if request.method == "POST":
            f = request.files["file"]

            filename = secure_filename(f.filename)
            # 외부에서 온 이미지, 파일 등을
            # 마음대로 저장할 수 없음
            # 서버에 클라이언트가 보낸 이미지를 저장!!
            f.save("static/" + filename)
            r = label("static/" + filename)
            return r
    except:
        return "감지 실패"

@app.route("/mbti", methods=["POST"])
def mbti():
    try:
        if request.method == "POST":
            mbti = request.form["mbti"]

            return f"당신의 MBTI는 {mbti}입니다"
    except:
        return "데이터 수신 실패"


# html 폴더 내 exam04.html을
# templates 폴더로 복사!!
@app.route("/login", methods=["GET"]) # methods=["GET","POST"]
def login():
    try:
        if request.method == "GET":
            # get -> request.args로 받을 수 있음
            login_id = request.args["login_id"]
            login_pw = request.args["login_pw"]
            # 로그인 성공 ->
            # 로그인 실패 -> 
            if login_id == "admin" and login_pw == "1234":

                response = make_response(redirect("/login/success")) # 응답객체를 담고
                response.set_cookie("user", login_id) # 그걸 꺼내서 쿠키에 얹음

                return response
            else:
                return redirect("/")

    except:
        return "로그인 실패"

@app.route("/login/success")
def login_success():

    login_id = request.cookies.get("user")
    return f"{login_id}님 환영합니다"

if __name__=="__main__":
    # 1. host
    # 2. port
    app.run(host="0.0.0.0") # localhost=127.0.0.1(내 Flask server IP)
                                # 0.0.0.0 = 10.10.15.28(내 IP)
# Ctrl + L하면 터미널 클리어

# 얼굴 비교
# 1. day13.py에 /compare라는 경로 만들기
# 2. home.html에 입력태그(form) 하나 추가
# 이미지 2개를 compare로 전송
# compare에서 받은 이미지 2개를 static폴더에 잘 저장!!
# aws.py 안에 compare_faces 그 결과를 문자열로
# "동일 인물일 확률은 15.24%"입니다 리턴
# 5. compare에서 리턴된 문자열을 받아서 웹 상에 출력(return)