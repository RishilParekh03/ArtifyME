from base import app
from base.com.controller.login_controller import get_sess
from base.com.vo.login_vo import LoginVO
from base.com.dao.login_dao import LoginDAO
from flask import render_template, request, redirect, url_for, flash, session
import bcrypt


@app.route('/profile')
def profile():
    try:
        user_field = get_sess()
        if user_field['curr_user'] is not None:
            return redirect(url_for('user_profile', username=user_field['curr_user']))
        else:
            flash("You must be signed in to view your profile.")
            return render_template("admin/profile_page.html", user_field=user_field)
    except Exception as error:
        print("\nError: Unable to load the profile page.\n")
        return render_template("admin/error_page.html", error=error)


@app.route('/profile/<username>')
def user_profile(username):
    try:
        user_field = get_sess()
        if user_field["curr_user"] == username:
            search_profile_vo = LoginVO()
            search_profile_dao = LoginDAO()
            search_profile_vo.username = user_field['curr_user']
            fetch_profile = search_profile_dao.search_user(search_profile_vo)
            print(f"Found a Profile: {fetch_profile.as_dict()}")
            return render_template("admin/profile_page.html", user_field=fetch_profile)
    except Exception as error:
        print("\nError: Unable to load the profile page.\n")
        return render_template("admin/error_page.html", error=error)


@app.route('/profile/edit/<user_id>', methods=['GET', 'POST'])
def edit_profile(user_id):
    try:
        user_field = get_sess()
        search_profile_vo = LoginVO()
        search_profile_dao = LoginDAO()

        if request.method == 'GET':
            if user_field["curr_user_id"] == int(user_id):
                search_profile_vo.user_id = user_field['curr_user_id']
                fetch_profile = search_profile_dao.edit_user(search_profile_vo)
                return render_template('admin/edit_profile.html', user_field=fetch_profile)

        elif request.method == "POST":
            edit_name = request.form['edit-name']
            edit_email = request.form['edit-email']
            edit_pwd = request.form['edit-password']

            if edit_pwd:
                hashed_edit_pwd = bcrypt.hashpw(edit_pwd.encode('utf-8'), bcrypt.gensalt())
                search_profile_vo.password = hashed_edit_pwd
            else:
                search_profile_vo.username = user_field['curr_user']
                existing_profile = search_profile_dao.search_user(search_profile_vo)
                search_profile_vo.password = existing_profile.password

            search_profile_vo.user_id = user_field['curr_user_id']
            search_profile_vo.name = edit_name
            search_profile_vo.username = edit_email

            search_profile_dao.update_user(search_profile_vo)

            session.pop('curr_user', None)
            session['curr_user'] = edit_email

            flash('Profile updated.')
            return redirect(url_for('user_profile', username=edit_email))

    except Exception as error:
        print("\nError: Unable to load the edit page.\n")
        return render_template("admin/error_page.html", error=error)


@app.route('/profile/delete/<user_id>', methods=["POST"])
def delete_profile(user_id):
    try:
        user_field = get_sess()
        if user_field["curr_user_id"] == int(user_id):
            password_popup = request.form['verifyPassword']
            delete_profile_vo = LoginVO()
            delete_profile_dao = LoginDAO()

            delete_profile_vo.user_id = user_field['curr_user_id']
            fetch_profile = delete_profile_dao.edit_user(delete_profile_vo)
            stored_hashed = fetch_profile.password

            if bcrypt.checkpw(password_popup.encode('utf-8'), stored_hashed.encode('utf-8')):
                delete_profile_dao.delete_user(delete_profile_vo)
                print('Profile deleted.')
                return redirect('/signout')
            else:
                flash("Incorrect password.")
                return redirect(url_for('user_profile', username=user_field['curr_user']))

    except Exception as error:
        print("\nError: Unable to delete profile.\n")
        return render_template("admin/error_page.html", error=error)
