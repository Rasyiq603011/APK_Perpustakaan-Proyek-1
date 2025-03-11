import json
import hashlib
import tkinter as tk
from tkinter import messagebox
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

USER_DATA_FILE = "users.json"
CLIENT_SECRET_FILE = "client_secret.json"
SCOPES = ["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"]
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

def load_users():
    try:
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_users(users):
    with open(USER_DATA_FILE, "w") as file:
        json.dump(users, file, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def initialize_admin():
    users = load_users()
    if ADMIN_USERNAME not in users:
        users[ADMIN_USERNAME] = {"name": "Administrator", "password": hash_password(ADMIN_PASSWORD)}
        save_users(users)
initialize_admin()

def show_login_page():
    sign_up_frame.pack_forget()
    login_frame.pack(expand=True)

def show_sign_up_page():
    login_frame.pack_forget()
    sign_up_frame.pack(expand=True)

def sign_up():
    name = entry_name.get().strip()
    username = entry_username.get().strip()
    password = entry_password.get().strip()
    
    if not name or not username or not password:
        messagebox.showerror("Error", "Nama, Username, dan Password tidak boleh kosong!")
        return
    
    users = load_users()
    if username in users:
        messagebox.showerror("Error", "Username sudah terdaftar!")
        return
    users[username] = {"name": name, "password": hash_password(password)}
    save_users(users)
    messagebox.showinfo("Sukses", "Registrasi berhasil! Silakan login.")
    show_login_page()

def log_in():
    users = load_users()
    username = entry_login_username.get().strip()
    password = entry_login_password.get().strip()
    
    if username in users and users[username]["password"] == hash_password(password):
        messagebox.showinfo("Sukses", f"Login berhasil! Selamat datang, {users[username]['name']}")
        root.withdraw()
        if username == ADMIN_USERNAME:
            open_admin_panel(users[username]["name"])
        else:
            open_user_panel(users[username]["name"])
    else:
        messagebox.showerror("Error", "Username atau password salah!")

def google_login():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    
    service = build("oauth2", "v2", credentials=creds)
    user_info = service.userinfo().get().execute()
    
    email = user_info["email"]
    name = user_info.get("name", email)
    users = load_users()
    
    if email not in users:
        users[email] = {"name": name, "password": hash_password(email)}
        save_users(users)
    
    messagebox.showinfo("Sukses", f"Login berhasil! Selamat datang, {name}")
    root.withdraw()
    open_user_panel(name)

def open_admin_panel(name):
    admin_window = tk.Toplevel(root)
    admin_window.title("Admin Panel")
    admin_window.geometry("300x200")
    tk.Label(admin_window, text=f"Admin Panel - Selamat Datang, {name}").pack()
    tk.Button(admin_window, text="Tambah Pengguna", command=sign_up).pack()
    tk.Button(admin_window, text="Keluar", command=admin_window.destroy).pack()

def open_user_panel(name):
    user_window = tk.Toplevel(root)
    user_window.title("User Panel")
    user_window.geometry("300x200")
    tk.Label(user_window, text=f"User Panel - Selamat Datang, {name}").pack()
    tk.Button(user_window, text="Keluar", command=user_window.destroy).pack()

def close_app():
    root.destroy()

# GUI Setup
root = tk.Tk()
root.title("Login System")
root.attributes('-fullscreen', True)

sign_up_frame = tk.Frame(root)
login_frame = tk.Frame(root)

# Sign Up Page
tk.Label(sign_up_frame, text="Nama:", font=("Arial", 16)).pack()
entry_name = tk.Entry(sign_up_frame, font=("Arial", 16))
entry_name.pack()

tk.Label(sign_up_frame, text="Username:", font=("Arial", 16)).pack()
entry_username = tk.Entry(sign_up_frame, font=("Arial", 16))
entry_username.pack()

tk.Label(sign_up_frame, text="Password:", font=("Arial", 16)).pack()
entry_password = tk.Entry(sign_up_frame, show="*", font=("Arial", 16))
entry_password.pack()

tk.Button(sign_up_frame, text="Sign Up", command=sign_up, font=("Arial", 16)).pack()
tk.Button(sign_up_frame, text="Sudah punya akun? Login", command=show_login_page, font=("Arial", 16)).pack()

tk.Button(sign_up_frame, text="Keluar", command=close_app, font=("Arial", 16)).pack()

# Login Page
tk.Label(login_frame, text="Username:", font=("Arial", 16)).pack()
entry_login_username = tk.Entry(login_frame, font=("Arial", 16))
entry_login_username.pack()

tk.Label(login_frame, text="Password:", font=("Arial", 16)).pack()
entry_login_password = tk.Entry(login_frame, show="*", font=("Arial", 16))
entry_login_password.pack()

tk.Button(login_frame, text="Log In", command=log_in, font=("Arial", 16)).pack()
tk.Button(login_frame, text="Login dengan Google", command=google_login, font=("Arial", 16)).pack()
tk.Button(login_frame, text="Belum punya akun? Daftar", command=show_sign_up_page, font=("Arial", 16)).pack()
tk.Button(login_frame, text="Keluar", command=close_app, font=("Arial", 16)).pack()

# Tampilkan halaman sign-up pertama kali
show_sign_up_page()
root.mainloop()