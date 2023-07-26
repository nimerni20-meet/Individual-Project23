from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
import json
import requests 


config = {
  "apiKey": "AIzaSyAvEeJXjtPejmnIphkox18ts4kDAIvQpQ4",
 "authDomain": "lab-c4556.firebaseapp.com",
  "projectId": "lab-c4556",
  "storageBucket": "lab-c4556.appspot.com",
  "messagingSenderId": "980248028540",
  "appId": "1:980248028540:web:197a93e8e7e72f00f670f9",
  "measurementId": "G-KR93543B28",
  "databaseURL":"https://lab-c4556-default-rtdb.europe-west1.firebasedatabase.app/"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()




app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here



parameters = {"camera": "NAVCAM"} # Shows Navigation Camera photos only.

response = requests.get("https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&api_key=faRn6vfvjvAmibI3UeuCfdYb3S4BFBP7rAPSfsu2", params = parameters)

print(response.content)





@app.route('/', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        bio = request.form['bio']
        locaion = request.form['locaion']
        name = request.form['name']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user={"email":email,"password":password,"bio":bio,"locaion":locaion,"name":name, "UID":UID}
            db.child("user").child(UID).set(user)
            return redirect(url_for('signin'))
        except:
            error = "Authentication failed"
    return render_template("singup.html")





@app.route('/home',methods=['GET','POST'])
def home():
    return render_template("index.html")






@app.route('/singin', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']
        try:
            # print("test")
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('home'))
        except:
            error = "Authentication failed"
    return render_template("singin.html",error=error)







@app.route('/profile')
def profile():
    try:
        UID = login_session['user']['localId']
        info = db.child("user").child(UID).get().val()
        print(info)
        return render_template('profile.html',info=info)
    except:
        error = "Authentication failed"
    return render_template("profile.html")


@app.route('/users')
def users():
    try:
        info = db.child("user").get().val()
        return render_template('users.html',info=info)
    except:
        error = "Authentication failed"
    return render_template("users.html")

@app.route('/user/<string:fid>', methods=['GET','POST'])
def add_friend(fid):
    try:
        UID = login_session['user']['localId']
        if friend_exists(fid) == False:
            exp_1 = db.child("user").child(UID).child("friends").push({'UID':fid})
            # exp_2 = db.child("user").child(UID).update(updated)
        return redirect(url_for('users'))
    except:
        return "Authentication failed"


def friend_exists(fUID):
    friends = db.child("user").child(UID).child("friends").get().val()
    for ID in friends:
        if ID == fUID:
            return True
    return False



@app.route('/add_posts', methods=['GET', 'POST'])
def add_posts():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        try:
            print('1')
            UID = login_session['user']['localId']
            print('1')
            posts={"title":title,"text":text}
            print('1')
            db.child("posts").push(posts)
            print('1')
            return redirect(url_for('all_posts'))
             
        except:
            error = "Authentication failed"
    return render_template("index.html")

@app.route('/all_posts')
def all_posts():
    posts=db.child('posts').get().val()
    return render_template("posts.html",posts=posts)


@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))
























#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)
# @app.route('/profile')
# def profile():
#     if 'email' in session:
#         user = users.get(session['email'])
#         return render_template('profile.html', user=user)
#     return redirect(url_for('login'))