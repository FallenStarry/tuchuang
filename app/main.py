from flask import *
import config as c
import uuid
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = "123456"

def login_check(f):
    @wraps(f) 
    def decorated(*args, **kwargs):
        if "logged_in" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs) 
    return decorated

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("password") == config.key:
            session["logged_in"] = True   # 写入 session，浏览器 cookie 里存一个签名标记
            return redirect(url_for("index"))
        flash("账号或密码错误")
    return render_template("login.html")  # GET 请求或登录失败，显示登录页面

@app.route("/", methods=["GET", "POST"])
@login_required                    # 必须登录才能访问
def index():
    if request.method == "POST":
        file = request.files.get("file")   # 从表单中取上传的文件对象
        if not file or file.filename == "":
            flash("请先选择文件")
        else:
            ext = file.filename.rsplit(".", 1)[1].lower()
            new_name = uuid.uuid4().hex + "." + ext        # 32位随机文件名
            file.save(config.UPLOAD_DIR + "/" + new_name)  # 保存到 uploads 目录
            flash("上传成功：" + new_name)
        return redirect(url_for("index"))  # 上传后重定向，防止刷新重复提交
    
    files = sorted(
        [f for f in os.listdir(config.up) if os.path.isfile(config.up + "/" + f)],
        reverse=True,                # 倒序，新文件排前面
    )
    return render_template("index.html", files=files)

if __name__ == "__main__":
    app.run(host=config.host, port=config.port, debug=True)  # 启动开发服务器，debug=True 开启自动重载