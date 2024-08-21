from base import app
from base.com.controller.login_controller import get_sess
from base.com.vo.login_vo import LoginVO
from base.com.dao.login_dao import LoginDAO
from flask import render_template, request, redirect, url_for, flash, jsonify


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


@app.route('/edit_profile/<user_id>')
def edit_profile(user_id):
    try:
        user_field = get_sess()
        if user_field["curr_user_id"] == int(user_id):
            search_profile_vo = LoginVO()
            search_profile_dao = LoginDAO()
            print(user_field['curr_user_id'])
            search_profile_vo.user_id = user_field['curr_user_id']
            fetch_profile = search_profile_dao.edit_user(search_profile_vo)
            print(f"Found a Profile: {fetch_profile.as_dict()}")
            return render_template('admin/edit_profile.html', user_field=fetch_profile)
    except Exception as error:
        print("\nError: Unable to load the edit page.\n")
        return render_template("admin/error_page.html", error=error)
