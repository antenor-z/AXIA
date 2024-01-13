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
        }
        ttype = ddict.get(extension, "document")
    return ttype

@app.get("/")
@app.get("/p/")
@app.get("/p/<path:path>/")
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
    for file in os.listdir(os.path.join(DIR, path)):
        ext_path = os.path.join(path, file)
        int_path = os.path.join(DIR, path, file)
        file_or_dir = "/p/" if os.path.isdir(int_path) else "/f/"
         
        res.append({
            "name": file,
            "created_at": datetime.fromtimestamp(os.path.getctime(int_path)).strftime('%Y-%m-%d %H:%M'),
            "path": file_or_dir + ext_path,
            "type": get_path_type(int_path=int_path),
            "rm_path": "/rm/" + ext_path
        })

        res.sort(key=lambda x: x['name'].split(".")[-1])

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
    
    file = request.files['file']

    if file.filename == '':
        return "no file"
        
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(DIR, path, filename))

    return redirect("/p/" + path)

@app.post("/mkdir/")
def mkdir():
    folder_name = request.form["folder_name"]
    path = request.form["path"]
    if path.startswith("/"): path = path[1:]
    if "/" in folder_name or "$" in folder_name:
        return "invalid folder name"
    int_path = os.path.join(DIR, path, folder_name)
    os.mkdir(int_path)
    return redirect("/p/" + path)

# @app.errorhandler(404)
# def not_found(e):
#     return render_template("error.html", error="404 | Página não encontrada."), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
