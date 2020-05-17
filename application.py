import os
import requests
from flask import Flask, session,render_template,request,redirect,url_for,flash,jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine("postgres://boaqtdatmuhusp:568946665bde49b4c20c29ab15259a2c9029462c4d92a29fe9aa37c44dcfe580@ec2-50-17-90-177.compute-1.amazonaws.com:5432/dd4t41ubcfugk1")
db = scoped_session(sessionmaker(bind=engine))

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/aboutUs")
def aboutUs():
    return render_template("aboutUs.html")

@app.route("/signUp",methods=["GET","POST"])
def signUp():
    if request.method == "GET":
        return render_template("signUp.html")
    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        ifemail = db.execute("SELECT email FROM users WHERE email = :email ;",{"email":email}).fetchone()
        ifusername = db.execute("SELECT username FROM login WHERE username = :username ;",{"username":username}).fetchone()
        if(ifemail is not None):
            flash("Email already exists,Try another!")
            return render_template("signUp.html")
        if(ifusername is not None):
            flash("Username already exists,Try another!")
            return render_template("signUp.html")
        if(email is None or name is None or username is None or password is None):
            flash("Fill all the details")
            return render_template("signUp.html")
        db.execute("INSERT INTO login(username,password) VALUES( :username , :password ) ;",{"username":username,"password":password})
        db.commit()
        results = (db.execute("SELECT id FROM login WHERE username = :username ;",{"username":username}).fetchone())
        if(results):
            login_id = results[0]
        db.execute("INSERT INTO users(login_id,email,name) VALUES(:login_id , :email , :name );",{"login_id":login_id,"email":email,"name":name})
        db.commit()
        return redirect(url_for("logIn"))
    
    
@app.route("/logIn",methods = ["GET","POST"])
def logIn():
    if request.method=="GET":
        if(session.get("username") is not None):
            flash(f"Already Logged In as {session.get('username')}")
            return redirect(url_for("dashboard"))
        return render_template("logIn.html")
    if request.method=="POST":
        if(session.get("username") is not None):
            flash("Already logged in!")
            return render_template("logIn.html")
        else:
            username = request.form.get("username")
            password = request.form.get("password")
            passcheck = db.execute("SELECT password FROM login WHERE username = :username ;",{"username":username}).fetchone()
            if passcheck is None:
                flash("Wrong Password or Username!")
                return render_template("logIn.html")
            if(passcheck[0] != password):
                flash("Wrong Password or Username!")
                return render_template("logIn.html")
            else:
                session["username"] = username
                return redirect(url_for("dashboard"))
            
        

@app.route("/dashboard",methods = ["POST","GET"])
def dashboard():
    if session.get("username") is None:
        return redirect(url_for("logIn"))
    else:
        return render_template("dashboard.html",username = session["username"])
    
@app.route("/logout")
def logOut():
    session.clear()
    return redirect(url_for("logIn"))

@app.route("/search",methods=["POST"])
def search():
    try:
        searchstring = request.form.get("string")
    except:
        return "Error!!"
    if searchstring is None:
        return redirect(url_for("dashboard"))
    if searchstring == "":
        return redirect(url_for("dashboard"))
    try:
        results = db.execute("SELECT title FROM books where isbn LIKE :search OR title LIKE :search OR author LIKE :search",{"search":f"%{searchstring}%"}).fetchall()
    except:
        return "Error!!"
    if results is None:
        return render_template("nosearch.html",username = session["username"])
    resultsearch = []
    for result in results:
        resultsearch.append(result[0])
    if len(resultsearch)==0 :
        return render_template("nosearch.html",username = session["username"])
    return render_template("search.html",username=session["username"],results = resultsearch)


@app.route("/topbooks")
def topbooks():
    if session.get("username") is None:
        return redirect(url_for("logIn"))
    try: 
        results = db.execute("SELECT A.title FROM books A JOIN book_score B ON A.isbn = B.isbn  order by B.score ASC LIMIT 100;").fetchall()
    except:
        return "Error!!"
    resultsearch = []
    for result in results:
        resultsearch.append(result[0])
    if len(resultsearch)==0 :
        results = db.execute("SELECT title FROM books LIMIT 100").fetchall()
        
    for result in results:
        resultsearch.append(result[0])
    return render_template("topbooks.html",username=session["username"],results = resultsearch)

@app.route("/topauthors")
def topauthors():
    if session.get("username") is None:
        return redirect(url_for("logIn"))
    try:
        results = db.execute("SELECT B.name FROM  author_score B  order by B.score ASC LIMIT 100").fetchall()
    except:
        return "Error!!"
    resultsearch = []
    if results is None:
        return render_template("nosearch.html")
    for result in results:
        resultsearch.append(result[0])
    if len(resultsearch)==0 :
        return render_template("nosearch.html",username = session["username"])
    return render_template("topauthors.html",results = resultsearch,username=session["username"])
 
@app.route("/my-favourite-books")
def favbooks():
    if session.get("username") is None:
        return redirect(url_for("logIn"))
    try:
        results = db.execute("SELECT A.title FROM books A JOIN collection B ON A.isbn = B.isbn where B.catagory = 'fav' AND B.username = :username ",{"username":session["username"]}).fetchall()
    except:
        return "Error!!"
    resultsearch = []
    if results is None:
        return render_template("nosearch.html")
    for result in results:
        resultsearch.append(result[0])
    if len(resultsearch)==0 :
        return render_template("nosearch.html",username = session["username"])    
    return render_template("favbooks.html",results = resultsearch,username=session["username"])

@app.route("/books-to-read")
def books2read():
    if session.get("username") is None:
        return redirect(url_for("logIn"))
    try:
        results = db.execute("SELECT A.title FROM books A JOIN collection B ON A.isbn = B.isbn where B.catagory = 'books2read' AND B.username = :username ",{"username":session["username"]}).fetchall()
    except:
        return "Error!!"
    resultsearch = []
    if results is None:
        return render_template("nosearch.html")
    for result in results:
        resultsearch.append(result[0])
    if len(resultsearch)==0 :
        return render_template("nosearch.html",username = session["username"])
    return render_template("books2read.html",results = resultsearch,username=session["username"])

@app.route("/books-i-have-read")
def booksread():
    if session.get("username") is None:
        return redirect(url_for("logIn"))
    try:
        results = db.execute("SELECT A.title FROM books A JOIN collection B ON A.isbn = B.isbn where B.catagory = 'booksread' AND B.username = :username ",{"username":session["username"]}).fetchall()
    except:
        return "Error!!"
    resultsearch = []
    if results is None:
        return render_template("nosearch.html")
    for result in results:
        resultsearch.append(result[0])
    if len(resultsearch)==0 :
        return render_template("nosearch.html",username = session["username"])
    return render_template("booksread.html",results = resultsearch,username=session["username"])

@app.route("/<string:title>",methods = ["GET","POST"])
def bookish(title):
    if session.get("username") is None:
        return redirect(url_for("logIn"))
    
    try:
        results = db.execute("SELECT author,isbn,year FROM books where title = :title",{"title":title}).fetchone()
    except:
        return "Error!!"
    if results is None:
        return render_template("nosearch.html")
    if len(results)==0 :
        return render_template("nosearch.html",username = session["username"])
    author = results[0]
    isbn = results[1]
    year = results[2]
    print(title)
    try:
        users = db.execute("SELECT A.id FROM users A,login B WHERE A.login_id = B.id AND B.username = :username",{"username":session["username"]}).fetchone()
    except:
        return "Error!!"
    user_id = users[0]
    print(user_id)
    if request.method=="POST":
        rating = (int)(request.form.get("rating"))
        comment = request.form.get("comment")
        catagory = request.form.get("catagory")
        if (catagory is None) or (catagory=="none") :
            pass
        else:
            result = db.execute("SELECT id FROM collection WHERE isbn = :isbn AND catagory = :catagory AND username = :username",{"isbn":isbn,"catagory":catagory,"username":session["username"]}).fetchone()
            if result is None:
                db.execute("INSERT INTO collection(isbn,catagory,username) VALUES(:isbn,:catagory,:username)",{"isbn":isbn,"catagory":catagory,"username":session["username"]})
                db.commit()
        if rating is None:
            pass
        else:
            result = db.execute("SELECT id FROM reviews WHERE user_id = :user_id AND isbn = :isbn",{"user_id":user_id,"isbn":isbn}).fetchone()
            if result is None:
                db.execute("INSERT INTO reviews(isbn,comment,user_id,rating) VALUES(:isbn,:comment,:user_id,:rating)",{"isbn":isbn,"comment":comment,"user_id":user_id,"rating":rating})
                db.commit()
            else:
                db.execute("UPDATE reviews SET rating = :rating,comment = :comment WHERE isbn = :isbn AND user_id = :user_id",{"isbn":isbn,"comment":comment,"user_id":user_id,"rating":rating})
                db.commit()
                avg = db.execute("SELECT AVG(A.rating) FROM reviews A,books B WHERE A.isbn = B.isbn AND B.author = :author",{"author":author}).fetchone()
                db.execute("UPDATE author_score SET score = :avg WHERE name = :author",{"avg":avg[0],"author":author})
                db.commit()
    avg = db.execute("SELECT AVG(rating) FROM reviews WHERE isbn = :isbn",{"isbn":isbn}).fetchone()
    if avg[0] is None:
        avg_score = 0
    else:
        avg_score = avg[0]
    avg_score = "{:.2f}".format(avg_score)
    print(avg_score)
    user_review = db.execute("SELECT rating,comment FROM reviews WHERE user_id = :id AND isbn = :isbn",{"id":user_id,"isbn":isbn}).fetchone()
    if user_review is None:
        user_review = {0,None}
    print(user_review)
    all_review = db.execute("SELECT rating,comment FROM reviews WHERE isbn = :isbn",{"isbn":isbn}).fetchall()
    
    if len(all_review)==0:
        all_review = [user_review]
    print(all_review)
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "Z1joHriwnnDlpMVx7ztLA", "isbns": isbn})
    data = res.json()
    print(data)
    goodread_score = data["books"][0]['average_rating']
    goodread_count = data["books"][0]['work_ratings_count']
    print(goodread_score)
    print(goodread_count)
    
    return render_template("books.html",title = title,isbn = isbn,author = author,year = year,avg_score = avg_score,user_review = user_review,all_reviews = all_review,goodread_score = goodread_score,goodread_count = goodread_count,username=session["username"])
    
@app.route("/api/<string:isbn>")
def apis(isbn):
    if session.get("username") is None:
        return redirect(url_for("logIn"))
    else:
         try:
            results = db.execute("SELECT author,title,year FROM books where isbn = :isbn",{"isbn":isbn}).fetchone()
         except:
            return jsonify({"error": "isbn Not Found"}), 422
         if results is None:
            return jsonify({"error": "isbn Not Found"}), 422
         if len(results)==0 :
            return jsonify({"error": "isbn Not Found"}), 422
         author = results[0]
         title = results[1]
         year = results[2]
         avg = db.execute("SELECT AVG(rating) FROM reviews WHERE isbn = :isbn",{"isbn":isbn}).fetchone()
         if avg[0] is None:
            avg_score = 0
         else:
            avg_score = avg[0]
         count = db.execute("SELECT COUNT(*) FROM reviews WHERE isbn = :isbn",{"isbn":isbn}).fetchone()
         review_count = count[0]
         return jsonify({"title": title,"author": author,"year": year,"isbn": isbn,"review_count": review_count,"average_score": avg_score})
         
if __name__ == "__main__":
    app.run()
