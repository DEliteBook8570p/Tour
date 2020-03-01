from flask import Flask, render_template, redirect, flash, request, session
from mysqlconn import connectToMySQL
from flask_bcrypt import Bcrypt        
import re   # the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
app = Flask(__name__)
bcrypt = Bcrypt(app)     # creating an object called bcrypt 
                         

app.secret_key = "pass2311"
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=['POST'])
def register_user():
    is_valid = True
    if len(request.form['fn']) < 1:
        is_valid = False
        flash("First name is a required field")
    if len(request.form['fn']) < 2:
        is_valid = False
        flash("First name should be at least 2 characters long")
    if len(request.form['ln']) < 1:
        is_valid = False
        flash("Last name is a required field")
    if len(request.form['ln']) < 2:
        is_valid = False
        flash("Last name should be at least 2 characters long")
    if len(request.form['email']) < 1:
        is_valid = False
        flash("email is a required field")
    if len(request.form['password']) < 8:
        is_valid = False
        flash("Password must be at least 8 characters long")
    if request.form['c_password'] != request.form['password']:
        is_valid = False
        flash("Passwords must match")
    if not request.form['fn'].isalpha():
        is_valid = False
        flash("First name can only contain alphabetic characters")
    if not request.form['ln'].isalpha():
        is_valid = False
        flash("First name can only contain alphabetic characters")
    if not EMAIL_REGEX.match(request.form['email']):    # test whether a field matches the pattern
        is_valid = False
        flash("Invalid email address!")
    if not is_valid:
        return redirect("/")
    if is_valid:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])  
        print(pw_hash)
        query = "INSERT INTO users (first_name, last_name, email,password) VALUES (%(fn)s, %(ln)s,%(email)s, %(pw)s)"
        data = {
            'fn': request.form['fn'],
            'ln': request.form['ln'],
            'email': request.form['email'],
            'pw': pw_hash

        }
         
        mysql = connectToMySQL('tour')
        results = mysql.query_db(query, data)
        if results:
            session['id_user'] = results

      
    
    return redirect("/register")  #should change this one.


if __name__ == "__main__":
    app.run(debug=True)
