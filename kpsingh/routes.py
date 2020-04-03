import os
import secrets
from kpsingh import app
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, Flask
from kpsingh.forms import UploadImageForm

app.config["MAX_IMAGE_FILESIZE"] = 0.1 * 1024 * 1024


# Saving the accepted image

def SaveImage(form_picture):

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/uploaded_images', picture_fn)
    i = Image.open(form_picture)
    i.save(picture_path)

    return picture_fn  

# Accepting the image

def allowed_image_filesize(filesize):

    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False 

# API to save the accepted image

@app.route("/", methods=['GET', 'POST'])
def UploadImage():
    
    form = UploadImageForm()

    if form.validate_on_submit():

        if form.picture.data:
            
            if "filesize" in request.cookies:

                if not allowed_image_filesize(request.cookies["filesize"]):                   
                    flash('401 :   Upload Error! File too large.', 'danger')
                    return redirect(request.url)
                else:
                    SaveImage(form.picture.data)
                    flash('201  :   Image uploaded to local drive successfully!', 'success')
                    return redirect(request.url)                        
        else:
            flash('No file selected for uploading', 'warning')
            return redirect(request.url)
               
    image_file = url_for('static', filename='uploaded_images/default.jpg')
    return render_template('home.html', image_file=image_file, form=form)



