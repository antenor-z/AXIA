import subprocess
from flask import Flask, render_template, send_from_directory, redirect, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix
import os
import shutil
from datetime import datetime

from blueprints.login import login, is_logged
from dotenv import dotenv_values

config = dotenv_values(".env")

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[],
    storage_uri="memory://",
)
limiter.limit("4 per minute")(login)

app.config['MAX_CONTENT_LENGTH'] = float(config["max_upload_size_mb"]) * 1024 * 1024 

app.register_blueprint(login)
app.secret_key = config["secret_key"]
DIR = "cloud"

@app.before_request
def check_logged():
    return is_logged()

def get_path_type(int_path):
    ttype = ""
    if os.path.isdir(int_path): ttype = "folder"
    else:
        extension = int_path.split(".")[-1].lower()
        ddict = {
            "doc": "document",
            "docx": "document",
            "jpg": "image",
            "jpeg": "image",
            "png": "image",
            "pdf": "document2",
            "mp4": "video",
            "mov": "video",
            "txt": "document",
            "ppt": "presentation",
            "pptx": "presentation",
            "xls": "spreadsheet",
            "xlsx": "spreadsheet",
            "zip": "compressed",
            "rar": "compressed",
            "mp3": "audio",
            "wav": "audio",
            "html": "web",
            "css": "web",
            "js": "web",
            "json": "data",
            "csv": "data",
            "exe": "executable",
            "gif": "image",
        }
        ttype = ddict.get(extension, "other")
    return ttype

@app.get("/")
@app.get("/p")
@app.get("/p/<path:path>")
def ls(path = ""):
    res = []
    if path != "":
        parent_dir = os.path.split(path)[0]
        res.append(
            {
                "name": "..",
                "created_at": "",
                "path": "/p/" + parent_dir,
                "type": "up"
            }
        )
        if res[0]["path"].endswith("/"):
            res[0]["path"] = res[0]["path"][:-1]
    for file in sorted(os.listdir(os.path.join(DIR, path)), key=lambda x: (not os.path.isdir(os.path.join(DIR, path, x)), x)):
        ext_path = os.path.join(path, file)
        int_path = os.path.join(DIR, path, file)
        file_or_dir = "/p/" if os.path.isdir(int_path) else "/f/"
        if not os.path.isdir(int_path):
            size = os.path.getsize(int_path)
        else:
            size = get_directory_size(int_path)

        size = format_file_size(size)
        edit_path : str | None = get_edit_path(ext_path)
         
        res.append({
            "name": file,
            "created_at": datetime.fromtimestamp(os.path.getctime(int_path)).strftime('%Y-%m-%d %H:%M'),
            "path": file_or_dir + ext_path,
            "size": size,
            "type": get_path_type(int_path=int_path),
            "rm_path": "/rm/" + ext_path,
            "edit_path": edit_path,
            "rename_path": "/rename/" + ext_path
        })

    return render_template("directory.html", res=res, upload="/upload/" + path, current_path="/" + path)

@app.get("/f/<path:path>")
def op(path):
    return send_from_directory(DIR, path)

@app.get("/rm/<path:path>")
def rm(path):
    try:
        os.remove(os.path.join(DIR, path))
    except IsADirectoryError:
        shutil.rmtree(os.path.join(DIR, path))

    parent_dir = os.path.split(path)[0]
    return redirect("/p/" + parent_dir)

@app.get("/at/<path:path>")
def op_as_attachment(path):
    return send_from_directory(DIR, path, as_attachment=True)

@app.post("/upload")
def upload_post():
    path = request.form["path"]
    if path.startswith("/"): path = path[1:]

    if 'file' not in request.files:
        return "no file"
    
    files = request.files.getlist('file')

    for file in files:
        if file.filename == '':
            return "no file", 500
            
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(DIR, path, filename))

    return redirect("/p/" + path)

@app.post("/mkdir")
def mkdir():
    folder_name = request.form["folder_name"]
    path = request.form["path"]
    if path.startswith("/"): path = path[1:]
    int_path = os.path.join(DIR, path, secure_filename(folder_name))
    os.mkdir(int_path)
    return redirect("/p/" + path)

@app.post("/create")
def create():
    folder_name = request.form["file_name"]
    path = request.form["path"]
    if path.startswith("/"): path = path[1:]
    int_path = os.path.join(DIR, path, secure_filename(folder_name))
    with open(int_path, "w"):
        pass
    return redirect("/p/" + path)

@app.post("/rename/<path:path>")
def rename(path):
    parent_path = os.path.split(path)[0]
    new_name = request.form["name"]
    int_path = os.path.join(DIR, path)
    parent_dir = os.path.split(int_path)[0]
    int_path_new = os.path.join(parent_dir, new_name)
    os.rename(int_path, int_path_new)
    return redirect("/p/" + parent_path)

@app.get("/edit/<path:path>")
def edit(path):
    int_path = os.path.join(DIR, path)
    if not is_plain_text_file(int_path):
        return "The file is not plain text"
    a = ""
    with open(int_path) as fp:
        a = fp.read()
    return render_template("edit.html", contents=a, path=path)

@app.post("/edit/<path:path>")
def update(path):
    new_contents = request.form["new_contents"]
    parent_dir = os.path.split(path)[0]
    with open(os.path.join(DIR, path), "w") as fp:
        fp.write(new_contents)

    return redirect("/p/" + parent_dir)

# @app.errorhandler(404)
# def not_found(e):
#     return render_template("error.html", error="404 | Página não encontrada."), 404

def format_file_size(size):
    GiB = 1024 * 1024 * 1024
    MiB = 1024 * 1024
    KiB = 1024
    if size >= GiB:
        return str(round(size / GiB, 2)) + " GiB"
    elif size >= MiB:
        return str(round(size / MiB, 2)) + " MiB"
    elif size >= KiB:
        return str(round(size / KiB, 2)) + " KiB"
    elif size == 1:
        return str(size) + " byte"
    else:
        return str(size) + " bytes"
    
def get_directory_size(directory):
    r = subprocess.run(["du", "-bs", directory], capture_output=True)
    res = r.stdout.decode("utf-8")
    if r.returncode != 0:
        return 0
    return int(res.split("\t")[0])

def is_plain_text_file(int_path):
    try:
        with open(int_path) as fp:
            fp.read(128)
    except IsADirectoryError: return False
    except UnicodeDecodeError: return False
    return True

def get_edit_path(ext_path):
    int_path = os.path.join(DIR, ext_path)
    if is_plain_text_file(int_path):
        return f"/edit/{ext_path}"
    return None


if __name__ == '__main__':
    app.run(debug=True, port=5000)
