import tkinter as tk
from tkinter import messagebox


window = tk.Tk()
window.title("Auto Barman")
window.geometry('340x440')
print(window.keys)
window.configure(bg = '#333333')

def login():
    username = "bino"
    password = "cmonboy"

    if username_entry.get() == username and password_entry.get() == password:
        messagebox.showinfo(title="IT IS ON!", message=f"Bem-vindo ao Bar dos Brothers, {username}.")
    else:
        messagebox.showinfo(title="Erro", message="Login inválido.")

frame = tk.Frame(bg = '#333333')

#Creating widgets
login_label = tk.Label(frame, text="Login", bg = '#333333', fg = '#FFFFFF', font=("Arial", 30))
username_label = tk.Label(frame, text="Cliente", bg = '#333333', fg = '#FFFFFF', font=("Arial", 16))
username_entry = tk.Entry(frame, font=("Arial", 16))
password_entry = tk.Entry(frame, show="*", font=("Arial", 16))
password_label = tk.Label(frame, text="Senha", bg = '#333333', fg = '#FFFFFF', font=("Arial", 16))
login_button = tk.Button(frame, text="Login", bg = '#FF3399', fg = '#FFFFFF', font=("Arial", 16), command=login)

#Placing widgets on the screen
login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
username_label.grid(row=1, column=0)
username_entry.grid(row=1, column=1, pady=20)
password_label.grid(row=2, column=0)
password_entry.grid(row=2, column=1, pady=20)
login_button.grid(row=3, column=0, columnspan=2, pady=30)

frame.pack()

window.mainloop()

