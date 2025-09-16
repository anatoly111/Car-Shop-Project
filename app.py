from flask import Flask, render_template,url_for,session,redirect,g,request,flash
from flask_session import Session
from database import get_db, close_db
from forms import registrationForm, loginForm, profileForm, passForm, checkoutForm,filterForm,infoForm,contactForm
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps


app = Flask(__name__)
app.teardown_appcontext(close_db)
app.config["SECRET_KEY"] = "secret_key"
app.config["SESSION_PERMANENT"] = False 
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



@app.before_request
def load_logged_in_user():
    g.user = session.get("user_id",None)



def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("login",next = request.url))
        return view(*args, **kwargs)
    return wrapped_view


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cars",methods = ["GET","POST"])
def cars():
    form = filterForm()
    db = get_db()
    cars = db.execute(""" SELECT * FROM cars; """).fetchall()
    if request.method == "POST": 
        price = form.price.data
        make = form.make.data
        if make is not None and price == "lowest-highest": 
            cars = db.execute(""" SELECT * FROM cars
                                    WHERE make = ?
                                    ORDER BY price;""", (make, )).fetchall()
        
        elif make is not None and price == "highest-lowest":    
            cars = db.execute(""" SELECT * FROM cars 
                                WHERE make = ?
                                ORDER BY price DESC;""",(make, )).fetchall()
        
        elif make is None and price == "highest-lowest":    
            cars = db.execute(""" SELECT * FROM cars 
                              ORDER BY price DESC;""").fetchall()
            print(cars)
            
            
        elif make is None and price == "lowest-highest":
            cars = db.execute(""" SELECT * FROM cars 
                              ORDER BY price ;""").fetchall()
        else:
            cars = db.execute(""" SELECT * FROM cars
                                    WHERE make = ?""",(make, )).fetchall()
    
    return render_template("cars.html",form = form, cars = cars)

   

@app.route("/car/<int:car_id>")
def car(car_id):
    db = get_db() 
    car = db.execute("""SELECT * FROM cars
                        WHERE car_id = ?;""", (car_id,)).fetchone()
    return render_template("car.html",car=car)

@app.route("/register", methods = ["GET","POST"])
def register():
    form = registrationForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data
        password2 = form.password2.data
        db = get_db()
        conflict_user = db.execute( """ Select * FROM users
                                        WHERE user_id = ?;""", (user_id, )).fetchone()
        if conflict_user is not None:
            form.user_id.errors.append("Username already taken")
        else:
            db.execute(""" 
                        INSERT INTO users(user_id, password)
                        VALUES(?,?);""",
                        (user_id, generate_password_hash(password), ))
            db.commit()
            return redirect(url_for("login"))
    return(render_template("register.html",form = form))

@app.route("/login", methods = ["GET","POST"])
def login():
    form = loginForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data
        db = get_db()
        user = db.execute(""" SELECT * FROM users
                            WHERE user_id = ?;""", (user_id,)).fetchone()
        if user is None:
            form.user_id.errors.append("No such user name")
        elif not check_password_hash(user["password"],password):
            form.password.errors.append("Incorrect password")
        else:
            session.clear()
            session["user_id"] = user_id
            next_page = request.args.get("next")
            if not next_page:
                next_page = url_for("index")
            return redirect(next_page)
    return render_template("login.html",form = form)


@app.route("/logout")
def logout():
    session.clear()
    return redirect( url_for("index"))

@app.route("/cart")
@login_required
def cart():
    if "cart" not in session:
        session["cart"] = {}
    names = {}
    total = 0
    db = get_db()
    for car_id in session["cart"]:
        motor_car = db.execute("""SELECT * FROM cars 
                         WHERE car_id = ?;""", (car_id, )).fetchone()
        name = motor_car["name"]
        names[car_id] = name
        total += motor_car["price"] * session["cart"][car_id]
        print(session["cart"])
    return render_template("cart.html",cart = session["cart"],names = names, total = total)

@app.route("/add_to_cart/<int:car_id>")
@login_required
def add_to_cart(car_id):
    if "cart" not in session:
        session["cart"] = {}
    if car_id not in session["cart"]:
        session["cart"][car_id] = 1
    else:
        session["cart"][car_id] = session["cart"][car_id]+1
    session.modified = True
    return redirect( url_for("cart") )

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")

@app.route("/edit", methods = ["GET","POST"])
def edit():
    form = profileForm()
    if form.validate_on_submit():
        new_name = form.name.data
        oldname = form.oldname.data
        db = get_db()
        update = db.execute(""" SELECT * FROM users
                                WHERE user_id = ?;""",(new_name, )).fetchone()
        if update is not None:
            form.name.errors.append("username already taken")
        else:
            session.pop("user_id",None)
            db.execute(""" UPDATE users
                         SET user_id = ?
                         WHERE user_id = ?;""",(new_name, oldname))
            db.commit()
            return redirect("profile")
    return render_template("edit.html",form = form)

@app.route("/edit_password", methods = ["GET","POST"])
def edit_pass():
    form = passForm()
    if form.validate_on_submit():
        name = form.name.data
        new = form.new_pass.data
        db = get_db()
        edit_pass = db.execute(""" SELECT * FROM users
                                    WHERE user_id = ?;""",(name, )).fetchone()
        if edit_pass is None:
            form.name.error.append("user name does not exist")
        else:
            session.pop("password",None)
            db.execute(""" UPDATE users
                            SET password = ?
                            WHERE user_id = ?;""",(generate_password_hash(new), name))
            db.commit()
            return redirect("profile")
    return render_template("edit_pass.html",form = form)

@app.route("/remove_from_cart/<int:car_id>")
@login_required
def remove_cart(car_id):
    if "cart" not in session:
        session["cart"] = {}
    if "cart" in session:
        if car_id in session["cart"]:
            if session["cart"][car_id] > 1:
                session["cart"][car_id] -= 1
            else:
                del session["cart"][car_id]
        session.modified = True
        return redirect(url_for("cart"))

@app.route("/checkout",methods = ["POST","GET"])
@login_required
def checkout():
    form = checkoutForm()
    if form.validate_on_submit():
        message = "thank you for shopping at Thrifty wheels"
        return render_template("post.html",message = message)

    return render_template("checkout.html",form = form)


@app.route("/person_info",methods = ["GET","POST"])
@login_required
def info():
    form = infoForm()
    if form.validate_on_submit():
        name =form.name.data
        age = form.age.data
        email = form.email.data
        db = get_db()
        db.execute(""" INSERT INTO info(Name,AGE,email)
                        VALUES(?,?,?);""",(name, age, email))
        db.commit()
        return redirect("profile")
    return render_template("info.html",form = form)

@app.route("/Contact",methods = ["POST","GET"])
def contact():
    form  = contactForm()
    if form.validate_on_submit():
        message = form.message.data
        email = form.email.data
        name = form.name.data
        db = get_db()
        db.execute(""" INSERT INTO contact(Name,email,message)
                        VALUES(?,?,?);""",(name,email,message),)
        db.commit()
        return redirect("Contact")
    return render_template("Contact.html",form = form)
