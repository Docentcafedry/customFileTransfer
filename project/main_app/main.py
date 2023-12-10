import shutil
import os
from .. import  config
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, flash, redirect, url_for, send_from_directory
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def validate_file(filename: str) -> bool:
    return '.' in filename and filename.split('.')[1].lower() in ALLOWED_EXTENSIONS

@main.route('/')
def index():
    return  render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    disk_usage = shutil.disk_usage("/")
    total = f"Всего: {disk_usage.total / (2 ** 30):.2f} GB"
    used = f"Использовано: {disk_usage.used / (2 ** 30):.2f} GB"
    free = f"Свободно: {disk_usage.free / (2 ** 30):.2f} GB"

    filenames = os.listdir(config.UPLOAD_DIR)
    return render_template(
        'profile.html',
        name=current_user.name,
        filenames=filenames,
        total=total,
        used=used,
        free=free
    )

@main.route('/upload', methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        flash("Cant read file")
        return redirect(url_for("main.profile"))

    file = request.files["file"]
    if file.filename == "":
        flash("File doesn't choosen")
        return redirect(url_for("main.profile"))
    if file.filename and validate_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(config.UPLOAD_DIR, filename))
        return redirect(url_for('main.profile'))


@main.route('/uploads/<filename>')
@login_required
def download_file(filename):
    return send_from_directory(config.UPLOAD_DIR, filename)


@main.route('/delete/<filename>', methods=["DELETE"])
def delete_file(filename):
    try:
        os.remove(os.path.join(config.UPLOAD_DIR, filename))
        flash('File successfully deleted')
        return redirect(url_for('main.profile'))
    except Exception as ex:
        return str(ex)
