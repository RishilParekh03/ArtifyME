from base import app
from flask import render_template, request, redirect, url_for, flash, session
from base.com.vo.login_vo import LoginVO
from base.com.dao.login_dao import LoginDAO
import bcrypt


def get_sess():
    current_user_id = session.get('curr_user_id')
    current_user = session.get('curr_user')

    user_field = {
        "curr_user_id": current_user_id,
        "curr_user": current_user
    }

    return user_field


@app.route('/')
def index():
    try:
        user_field = get_sess()
        if user_field['curr_user'] is not None:
            return redirect(url_for('home', username=user_field['curr_user']))
        else:
            return render_template("admin/index.html", user_field=user_field)
    except Exception as error:
        print("\nError: Unable to load the home page.\n")
        return render_template("admin/error_page.html", error=error)


@app.route('/home/<username>')
def home(username):
    try:
        user_field = get_sess()
        if user_field["curr_user"] == username:
            return render_template("admin/index.html", user_field=user_field)
    except Exception as error:
        print("\nError: Unable to load the home page.\n")
        return render_template("admin/error_page.html", error=error)


@app.route('/signin')
def signin():
    try:
        return render_template("admin/sign-in_page.html")
    except Exception as error:
        print("\nError: Unable to load the sign-in page.\n")
        return render_template("admin/error_page.html", error=error)


@app.route('/user_signin_details', methods=['POST'])
def user_signin_details():
    try:
        signin_email = request.form.get('signIn-email')
        signin_password = request.form.get('signIn-password')

        search_profile_vo = LoginVO()
        search_profile_dao = LoginDAO()
        search_profile_vo.username = signin_email
        search_profile_vo.password = signin_password
        search_profile = search_profile_dao.search_user(search_profile_vo)

        if search_profile:
            print(f"Profile Found: {search_profile.as_dict()}")
            stored_hash = search_profile.password
            if bcrypt.checkpw(signin_password.encode('utf-8'), stored_hash.encode('utf-8')):
                print("Password match successful")
                session['curr_user_id'] = search_profile.user_id
                session['curr_user'] = search_profile.username
                return redirect(url_for('home', username=search_profile.username))
            else:
                flash("Invalid email or password")
                return redirect(url_for('signin'))
        else:
            flash("Profile not found!")
            return redirect(url_for('signin'))
    except Exception as error:
        print("\nError: Unable to sign In.\n")
        return render_template('admin/error_page.html', error=error)


@app.route('/signout')
def signout():
    try:
        session.pop('curr_user_id', None)
        session.pop('curr_user', None)
        return redirect(url_for('index'))
    except Exception as error:
        print("\nError: Unable to sign out.\n")
        return render_template("admin/error_page.html", error=error)


@app.route('/signup')
def signup():
    try:
        return render_template("admin/sign-up_page.html")
    except Exception as error:
        print("\nError: Unable to load the sign-up page.\n")
        return render_template("admin/error_page.html", error=error)


@app.route('/user_signup_details', methods=['POST'])
def user_signup_details():
    try:
        signup_name = request.form.get('signUp-name')
        signup_email = request.form.get('signUp-email')
        signup_password = request.form.get('signUp-password')
        signup_con_password = request.form.get('signUp-con-password')

        if signup_password != signup_con_password:
            flash("Password do not match.")
            return redirect(url_for('signup'))

        byte = signup_password.encode('utf-8')
        hash_pw = bcrypt.hashpw(byte, bcrypt.gensalt())

        insert_new_user_vo = LoginVO()
        insert_new_user_dao = LoginDAO()

        insert_new_user_vo.name = signup_name
        insert_new_user_vo.username = signup_email
        insert_new_user_vo.password = hash_pw

        insert_new_user_dao.insert_user(insert_new_user_vo)

        return redirect(url_for('signin'))
    except Exception as error:
        print("\nError: Unable to sign Up.\n")
        return render_template('admin/error_page.html', error=error)
