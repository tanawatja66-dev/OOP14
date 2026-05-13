from flask import Flask, render_template, request, redirect, session
from auth import AuthManager
from datetime import datetime

app = Flask(__name__)

# สำคัญสำหรับ session
app.secret_key = "123456"

auth_manager = AuthManager()


# =========================
# HOME
# =========================

@app.route("/")
def home():

    # ยังไม่ login
    if not auth_manager.is_logged_in():
        return redirect("/login")

    # ดึง user จาก session
    user = session.get("user")

    return render_template(
        "index.html",
        user=user
    )


# =========================
# REGISTER
# =========================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form["fullName"]
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        

        auth_manager.register(
            full_name,
            email,
            username,
            password
        )

        # เก็บข้อมูลลง session
        session["user"] = {
            "fullName": full_name,
            "email": email,
            "username": username,
            "registerDate": datetime.now().strftime("%d/%m/%Y"),
        }

        return redirect("/login")

    return render_template("register.html")


# =========================
# LOGIN
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if auth_manager.login(username, password):

            # ดึง user
            user = auth_manager.get_user()

            # เก็บ session
            session["user"] = user

            return redirect("/")

    return render_template("login.html")


# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    auth_manager.logout()

    session.clear()

    return redirect("/login")


# =========================
# RUN
# =========================

if __name__ == "__main__":
    app.run(debug=True)