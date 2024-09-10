from flask import Flask, render_template, send_from_directory, redirect, request, Blueprint, session, current_app
import secrets
import os
from dotenv import dotenv_values
import pyotp

config = dotenv_values(".env")

login = Blueprint('login', __name__)
__password = config["password"]

if __password is None:
    raise SystemError("No password set in .env")

active_sessions = []

def is_logged():
    print(active_sessions)
    if "/static/" in request.url:
        return None
    
    if request.endpoint in ["login.show_login", "login.try_login"]:
        return None
    
    if session.get("session") not in active_sessions:
        return redirect("/login")
    
    

@login.get("/login")
def show_login():
    return render_template('login.html')

@login.get("/logout")
def logout():
    old_token = session.pop("session")
    active_sessions.remove(old_token)
    return redirect("/")


@login.post("/login")
def try_login():
    if request.form['password'] == __password:
        totp = pyotp.TOTP(config["TOTP_secret"])
        #if request.form['password2'] == totp.now():
        token = secrets.token_hex(32)
        session["session"] = token
        active_sessions.append(token)

    return redirect("/")
