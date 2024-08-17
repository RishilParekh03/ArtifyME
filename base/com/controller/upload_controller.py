from base import app
from base.com.controller.login_controller import get_sess
from base.com.vo.upload_vo import UploadVO
from base.com.dao.upload_dao import UploadDAO
from base.com.model.portrait_model import PortraitModel
from flask import render_template, request, redirect, url_for, flash, jsonify
import os
from werkzeug.utils import secure_filename


@app.route('/upload_image')
def upload_page():
    try:
        user_field = get_sess()
        if user_field['curr_user'] is not None:
            return redirect(url_for('user_upload_image', username=user_field['curr_user']))
        else:
            flash("You must be signed in to upload image.")
            return render_template('admin/upload_page.html', user_field=user_field)
    except Exception as error:
        print("\nError: Failed to load the upload page.\n")
        return render_template("admin/error_page.html", error=error)


@app.route('/upload_image/<username>')
def user_upload_image(username):
    try:
        user_field = get_sess()
        if user_field['curr_user'] == username:
            return render_template('admin/upload_page.html', user_field=user_field)
    except Exception as error:
        print("\nError: Failed to load the upload page.\n")
        return render_template("admin/error_page.html", error=error)


@app.route('/converting_image', methods=["post"])
def converting_image():
    try:
        user_field = get_sess()
        print(f"Current user ID: {user_field['curr_user_id']}")

        if user_field['curr_user_id'] is not None:
            input_file = request.files['inputImage']
            print(f"User Selected Image: {input_file}\n")  # remove this once done
            if input_file:
                input_filename = input_file.filename
                print(f"Filename: {input_filename}\n")

                file_extension = os.path.splitext(input_filename)[1].lower()
                allowed_ext = ['.jpg', '.jpeg', '.png']
                if file_extension not in allowed_ext:
                    return jsonify({"error": f"Invalid file extension: {file_extension}."}), 400

                input_filename = secure_filename(input_filename)
                input_file_path = os.path.join(app.config['INPUT_FILES'], input_filename)
                input_file.save(input_file_path)

                print(f"File Path: {input_file_path}\n")

                model = PortraitModel(input_file_path)
                image_saved, img_path = model.final_result(input_filename)
                print(f"Image processed successfully: {image_saved}\n")
                print(f"Image saved: {img_path}\n")

                if img_path:
                    stored_filename = f'portrait_{input_filename}'
                    upload_vo = UploadVO()
                    upload_dao = UploadDAO()

                    upload_vo.upload_user_id = user_field['curr_user_id']
                    upload_vo.original_filename = input_filename
                    upload_vo.original_path = input_file_path
                    upload_vo.stored_filename = stored_filename
                    upload_vo.stored_path = img_path

                    upload_dao.insert_image(upload_vo)

                    processed_image_url = url_for('static', filename=f'output_images/portrait_{input_filename}')
                    return jsonify({'processed_image': processed_image_url})
            else:
                return redirect(url_for('user_upload_image', username=user_field['curr_user']))
        else:
            return redirect(url_for('upload_page'))
    except Exception as error:
        print("\nError: Image conversion failed.\n")
        return render_template("admin/error_page.html", error=error)
