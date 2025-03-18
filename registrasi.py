import json
import hashlib
import tkinter as tk
from tkinter import messagebox

# Konstanta
USER_DATA_FILE = "users.json"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# Warna-warna
PURPLE_COLOR = "#4C0086"  # Warna ungu untuk background
GREEN_COLOR = "#00FF11"   # Warna hijau untuk input field
WHITE_COLOR = "#FFFFFF"   # Warna putih untuk text

# Variabel global untuk entry fields
entry_name = None
entry_username = None
entry_password = None
entry_login_username = None
entry_login_password = None

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

def create_rounded_frame(parent, color):
    frame = tk.Frame(parent, bg=color, bd=5)
    frame.configure()
    return frame

def create_rounded_button(parent, text, command, width=10, height=1, font=("Arial", 12)):
    button = tk.Button(
        parent,
        text=text,
        font=font,
        bg=PURPLE_COLOR,
        fg="white",
        relief="raised",
        command=command,
        width=width,
        height=height,
        bd=5,
        cursor="hand2"
    )
    return button

def create_entry(parent, placeholder):
    entry = tk.Entry(parent, font=("Arial", 16), bg=GREEN_COLOR, fg="black", insertbackground="black", width=40, justify="center")
    entry.insert(0, placeholder)
    entry.placeholder_active = True  # Inisialisasi placeholder_active
    entry.bind("<FocusIn>", lambda e: on_entry_click(e, entry, placeholder))
    entry.bind("<FocusOut>", lambda e: on_entry_leave(e, entry, placeholder))
    return entry

def on_entry_click(event, entry, placeholder):
    if entry.get() == placeholder:
        entry.delete(0, tk.END)
        if placeholder == "password":
            entry.config(show="*")  # Tampilkan karakter * untuk password
        entry.config(fg="black")  # Ubah warna teks menjadi hitam saat diklik
        entry.placeholder_active = False  # Tandai bahwa placeholder tidak aktif

def on_entry_leave(event, entry, placeholder):
    if entry.get() == "":
        entry.insert(0, placeholder)
        if placeholder == "password":
            entry.config(show="")  # Kembalikan tampilan normal untuk placeholder password
        entry.config(fg="gray")  # Ubah warna teks menjadi abu-abu untuk placeholder
        entry.placeholder_active = True  # Tandai bahwa placeholder aktif
    elif entry.get() != placeholder:
        if placeholder == "password":
            entry.config(show="*")  # Tampilkan karakter * untuk input password
        entry.config(fg="black")  # Pastikan teks input tetap hitam
        entry.placeholder_active = False  # Tandai bahwa placeholder tidak aktif

def show_login_page():
    signup_frame.pack_forget()
    login_frame.pack(expand=True, pady=50)

def show_sign_up_page():
    login_frame.pack_forget()
    signup_frame.pack(expand=True, pady=50)

def sign_up():
    name = entry_name.get().strip()
    username = entry_username.get().strip()
    password = entry_password.get().strip()
    
    # Cek apakah masih menggunakan placeholder
    if (entry_name.placeholder_active or 
        entry_username.placeholder_active or 
        entry_password.placeholder_active):
        messagebox.showerror("Error", "Nama, Username, dan Password tidak boleh kosong!")
        return
    
    # Cek apakah ada field yang kosong
    if not name or not username or not password:
        messagebox.showerror("Error", "Nama, Username, dan Password tidak boleh kosong!")
        return
    
    # Cek panjang password minimal 8 karakter
    if len(password) < 8:
        messagebox.showerror("Error", "Password harus minimal 8 karakter!")
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
    
    # Cek apakah masih menggunakan placeholder
    if entry_login_username.placeholder_active or entry_login_password.placeholder_active:
        messagebox.showerror("Error", "Silakan masukkan username dan password!")
        return
    
    if username in users and users[username]["password"] == hash_password(password):
        messagebox.showinfo("Sukses", f"Login berhasil! Selamat datang, {users[username]['name']}")
        if username == ADMIN_USERNAME:
            open_admin_panel(users[username]["name"])
        else:
            open_user_panel(users[username]["name"])
    else:
        messagebox.showerror("Error", "Username atau password salah!")

def open_admin_panel(name):
    admin_window = tk.Toplevel(root)
    admin_window.title("Admin Panel")
    admin_window.geometry("300x200")
    tk.Label(admin_window, text=f"Admin Panel - Selamat Datang, {name}").pack()
    tk.Button(admin_window, text="Tambah Pengguna", command=show_sign_up_page).pack()
    tk.Button(admin_window, text="Keluar", command=admin_window.destroy).pack()

def open_user_panel(name):
    user_window = tk.Toplevel(root)
    user_window.title("User Panel")
    user_window.geometry("300x200")
    tk.Label(user_window, text=f"User Panel - Selamat Datang, {name}").pack()
    tk.Button(user_window, text="Keluar", command=user_window.destroy).pack()

def close_app():
    root.destroy()

# ================ GUI SETUP ================
# Inisialisasi admin
initialize_admin()

# Setup window utama
root = tk.Tk()
root.title("BOOK-KU!")
root.attributes('-fullscreen', True)
root.configure()

# Frame utama
main_frame = tk.Frame(root)
main_frame.pack(expand=True, pady=50)

# Frame untuk login dan signup
login_frame = tk.Frame(main_frame)
signup_frame = tk.Frame(main_frame)

# ================ LOGIN PAGE SETUP ================
# Logo dan Judul
title_frame = tk.Frame(login_frame, bg=PURPLE_COLOR)
title_frame.pack(pady=20)

title_label = tk.Label(title_frame, text="📖BOOK-KU!", font=("Arial Black", 48, "bold"), fg="black")
title_label.pack()

# Login Frame
login_form_frame = tk.Frame(login_frame, bg=PURPLE_COLOR, padx=20, pady=20)
login_form_frame.pack(expand=True)

# Entry fields dengan background hijau
entry_login_username = create_entry(login_form_frame, "your @gmail.com")
entry_login_username.pack(fill="x", padx=10, pady=10, ipady=10)

entry_login_password = create_entry(login_form_frame, "password")
entry_login_password.pack(fill="x", padx=10, pady=10, ipady=10)

# Login button dengan styling
login_button = create_rounded_button(
    login_frame,
    "LOGIN",
    log_in,
    width=10,
    height=1,
    font=("Arial", 16, "bold")
)
login_button.pack(pady=20)

# Tombol untuk pindah ke halaman sign up
signup_link_button = create_rounded_button(
    login_frame,
    "Belum punya akun? Daftar",
    show_sign_up_page,
    width=20,
    height=1
)
signup_link_button.pack()

# Tombol keluar untuk login page
login_exit_button = create_rounded_button(
    login_frame,
    "Keluar",
    close_app,
    width=10,
    height=1
)
login_exit_button.pack(pady=10)

# ================ SIGNUP PAGE SETUP ================
# Logo dan Judul untuk Sign Up
sign_up_title_frame = tk.Frame(signup_frame, bg=PURPLE_COLOR)
sign_up_title_frame.pack(pady=20)

sign_up_title_label = tk.Label(sign_up_title_frame, text="📖BOOK-KU!", font=("Arial Black", 48, "bold"), fg="black")
sign_up_title_label.pack()

# Frame untuk form sign up
sign_up_form_frame = tk.Frame(signup_frame, bg=PURPLE_COLOR, padx=20, pady=20)
sign_up_form_frame.pack(expand=True)

# Entry fields dengan background hijau untuk sign up
entry_name = create_entry(sign_up_form_frame, "your name")
entry_name.pack(fill="x", padx=20, pady=10, ipady=10)

entry_username = create_entry(sign_up_form_frame, "your @gmail.com")
entry_username.pack(fill="x", padx=20, pady=10, ipady=10)

entry_password = create_entry(sign_up_form_frame, "password")
entry_password.pack(fill="x", padx=20, pady=10, ipady=10)

# Sign Up button dengan styling
sign_up_button = create_rounded_button(
    signup_frame,
    "SIGN UP",
    sign_up,
    width=10,
    height=1,
    font=("Arial", 16, "bold")
)
sign_up_button.pack(pady=20)

# Tombol untuk kembali ke halaman login
login_link_button = create_rounded_button(
    signup_frame,
    "Sudah punya akun? Login",
    show_login_page,
    width=20,
    height=1
)
login_link_button.pack()

# Tombol keluar
exit_button = create_rounded_button(
    signup_frame,
    "Keluar",
    close_app,
    width=10,
    height=1
)
exit_button.pack(pady=10)

# Tampilkan login page pertama
show_login_page()

# ================ MAIN LOOP ================
root.mainloop()
