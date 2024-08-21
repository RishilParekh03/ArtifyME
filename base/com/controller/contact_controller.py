from base import app
from flask import render_template, request, jsonify, redirect, url_for, flash
from base.com.controller.login_controller import get_sess
from base.com.vo.contact_vo import ContactVO
from base.com.dao.contact_dao import ContactDAO


@app.route("/contact_us_page")
def contact_us_page():
    try:
        user_field = get_sess()
        if user_field['curr_user'] is not None:
            return redirect(url_for('user_contact_us_page', username=user_field['curr_user']))
        else:
            flash("You must be signed in to submit a feedback.")
            return render_template("admin/contact_us_page.html", user_field=user_field)
    except Exception as error:
        print("\nError: feedback page unavailable.\n")
        return render_template("admin/error_page.html", error=error)


@app.route("/contact_us_page/<username>")
def user_contact_us_page(username):
    try:
        user_field = get_sess()
        if user_field["curr_user"] == username:
            return render_template("admin/contact_us_page.html", user_field=user_field)
    except Exception as error:
        print("\nError: feedback page unavailable.\n")
        return render_template("admin/error_page.html", error=error)


@app.route("/submit_feedback/<user_id>", methods=['get'])
def submit_feedback(user_id):
    try:
        user_field = get_sess()

        if user_field['curr_user_id'] == int(user_id):
            name = request.args.get('name')
            email = request.args.get('email')
            feedback = request.args.get('feedback')

            insert_inquiry_vo = ContactVO()
            insert_inquiry_dao = ContactDAO()

            insert_inquiry_vo.inquiry_user_id = user_field['curr_user_id']
            insert_inquiry_vo.inquiry_user_email = email
            insert_inquiry_vo.feedback = feedback

            insert_inquiry_dao.insert_inquiry(insert_inquiry_vo)

            return jsonify({'status': 'success', 'name': name})
        else:
            return jsonify({'status': 'error', 'message': 'You must be signed in to submit feedback.'})
    except Exception as error:
        print("\nError: Failed to submit feedback.\n")
        return render_template("admin/error_page.html", error=error)
