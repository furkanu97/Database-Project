from flask import *
from datetime import datetime
from product import Product
from forms import ProductEditForm, LoginForm, UserEditForm
from settings import *
from user import *
from flask_login import login_user, logout_user, login_required, current_user

def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day=day_name)

def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.data["email"]
        user = get_user(email)
        if user is not None:
            password = form.data["password"]
            if hasher.verify(password, user.password):
                login_user(user)
                flash("You have logged in.")
                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)
        flash("Invalid credentials.")
    return render_template("login.html", form=form)


def logout_page():
    logout_user()
    flash("You have logged out.")
    return redirect(url_for("home_page"))

def products_page():
    db = current_app.config["db"]
    if request.method == "GET":
        products = []
        products = db.get_products()
        return render_template("products.html", products = products)
    else:
        if not current_user.is_admin:
            abort(401)
        form_product_keys = request.form.getlist("product_keys")
        for form_product_key in form_product_keys:
            db.delete_product(int(form_product_key))
        flash("%(num)d products deleted." % {"num": len(form_product_keys)})
        return redirect(url_for("products_page"))

def product_page(product_key):
    db = current_app.config["db"]
    product = db.get_product(product_key)
    return render_template("product.html", product=product)

@login_required
def product_add_page():
    form = ProductEditForm()
    if form.validate_on_submit():
        name = form.data["name"]
        price = form.data["price"]
        imported = form.data["imported"]
        category = form.data["category"]
        info = form.data["info"]
        db = current_app.config["db"]
        product_key = db.add_product(name, price, imported, category, info)
        return redirect(url_for("product_page", product_key=product_key))
    return render_template("product_add.html", form = form)

def validate_product_form(form):
    form.data = {}
    form.errors = {}

    form_name = form.get("name", "").strip()
    if len(form_name) == 0:
        form.errors["name"] = "Name can not be blank."
    else:
        form.data["name"] = form_name
    
    form_price = form.get("price", "").strip()
    if form_price == 0:
        form.errors["price"] = "Price can not be 0."
    elif not form_price.isdigit():
        form.errors["price"] = "Price must consist of digits only."
    else:
        form.data["price"] = form_price
    
    form_imported = form.get("imported", "").strip()
    if len(form_imported) == 0:
        form.errors["imported"] = "Import status can only be True or False."
    else:
        form.data["imported"] = form_imported
    
    form_category = form.get("category")   
    if len(form_category) == 0:       
        form.errors["category"] = "Category can not be blank." 
    else:
        form.data["category"] = form_category

    form_info = form.get("info", "").strip()
    if len(form_info) == 0:
        form.data["info"] = None
    else:
        form.data["info"] = form_info

@login_required
def product_edit_page(product_key):
    db = current_app.config["db"]
    product = db.get_product(product_key)
    form = ProductEditForm()
    if form.validate_on_submit():
        name = form.data["name"]
        price = form.data["price"]
        imported = form.data["imported"]
        category = form.data["category"]
        info = form.data["info"]
        db.update_product(product_key, name, price, imported, category, info)
        return redirect(url_for("product_page", product_key=product_key))
    form.name.data = product.name
    form.price.data = product.price
    form.imported.data = product.imported
    form.category.data = product.category
    form.info.data = product.info if product.info else ""
    return render_template("product_edit.html", form=form)

def users_page():
    db = current_app.config["db"]
    if request.method == "GET":
        users = db.get_users()
        return render_template("users.html", users=sorted(users))
    else:
        if not current_user.is_admin:
            abort(401)
        form_user_keys = request.form.getlist("user_keys")
        for form_user_key in form_user_keys:
            db.delete_user(int(form_user_key))
        flash("%(num)d users deleted." % {"num": len(form_user_keys)})
        return redirect(url_for("users_page"))

def user_page(user_key):
    db = current_app.config["db"]
    user = db.get_user(user_key)
    return render_template("user.html", user=user)

def sign_in_page():
    form = UserEditForm()
    if form.validate_on_submit():
        name = form.data["name"]
        surname = form.data["surname"]
        email = form.data["email"]
        password = form.data["password"]
        phone_number = form.data["phone_number"]
        user = User(name, surname, email, password, phone_number)
        db = current_app.config["db"]
        user_key = db.add_user(name, surname, email, password, phone_number)
        login_user(user)
        flash("You have logged in.")
        next_page = request.args.get("next", url_for("user_page", user_key=user_key))
        return redirect(next_page)
    return render_template("sign_in.html", form = form)

def validate_user_form(form):
    form.data = {}
    form.errors = {}

    form_name = form.get("name", "").strip()
    if len(form_name) == 0:
        form.errors["name"] = "Name can not be blank."
    else:
        form.data["name"] = form_name
    
    form_surname = form.get("surname", "").strip()
    if len(form_surname) == 0:
        form.errors["surname"] = "Surname can not be blank."
    else:
        form.data["surname"] = form_surname
    
    form_email = form.get("email", "").strip()
    if len(form_email) == 0:
        form.errors["email"] = "E-mail can not be blank."
    else:
        form.data["email"] = form_email
    
    form_password = form.get("password")   
    if len(form_password) < 8 | len(form_password) > 16:       
        form.errors["password"] = "Password must be between 8-16 characters." 
    else:
        form.data["password"] = form_password

    form_phone_number = form.get("phone_number", "").strip()
    if form_phone_number < 5300000000 | form_phone_number > 5599999999:
        form.data["phone_number"] = "Phone number is invalid."
    else:
        form.data["phone_number"] = form_phone_number

@login_required
def user_edit_page(user_key):
    db = current_app.config["db"]
    user = db.get_user(user_key)
    form = UserEditForm()
    if form.validate_on_submit():
        name = form.data["name"]
        surname = form.data["surname"]
        email = form.data["email"]
        password = form.data["password"]
        phone_number = form.data["phone_number"]
        db.update_user(user_key, name, surname, email, password, phone_number)
        return redirect(url_for("user_page", user_key=user_key))
    form.name.data = user.name
    form.surname.data = user.surname
    form.email.data = user.email
    form.password.data = user.password
    form.phone_number.data = user.phone_number
    return render_template("user_edit.html", form=form)