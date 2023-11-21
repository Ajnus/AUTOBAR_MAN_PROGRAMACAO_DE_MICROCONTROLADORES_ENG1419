import tkinter as tk
from tkinter import messagebox
import ast


window = tk.Tk()
window.title("Auto Barman")
window.geometry('925x500+300+200')
# print(window.keys)
window.configure(bg='#333333')
window.resizable(False, False)

img = tk.PhotoImage(file='assets/images/izac.png')
tk.Label(window, image=img, bg='white').place(x=50, y=50)


#def login():
    #username = "bino"
    #password = "cmonboy"

    #if username_entry.get() == username and password_entry.get() == password:
    #    messagebox.showinfo(
    #        title="IT IS ON!", message=f"Bem-vindo ao Bar dos Brothers, {username}.")
    #else:
    #    messagebox.showinfo(title="Erro", message="Login inválido.")


def login():
    username = username_entry.get()
    password = password_entry.get()

    if username=='bino' and password=='cmonboy':
        messagebox.showinfo(
            title="IT IS ON!", message=f"Bem-vindo ao Bar dos Brothers, {username}.")
        
        screen = tk.Toplevel(window)
        screen.title = "Cadastro"
        screen.geometry('925x500+300+200')
        screen.config(bg='#333333')
        screen.resizable(False, False)

        tk.Label(screen, text="Entremo!", bg = '#00FF41', font=("Inconsolata", 50,'bold')).pack(expand=True)

        screen.mainloop()

    elif username!='bino' and password!='cmonboy':
        messagebox.showinfo(title="Inválido", message="Cliente e Senha inválidos.")

    elif username!='bino' and password!='cmonboy':
        messagebox.showinfo(title="Inválido", message="Senha inválida.")

    elif username!='bino':
        messagebox.showinfo(title="Inválido", message="Cliente inválido.")

def on_enterU(e):
    username_entry.delete(0, 'end')

def on_leaveU(e):
    name = username_entry.get()
    if name=='':
        username_entry.insert(0,'Cliente')

def on_enterP(e):
    password_entry.delete(0, 'end')

def on_leaveP(e):
    name = password_entry.get()
    if name=='':
        password_entry.insert(0,'Senha')



frame = tk.Frame(window, width='350', height='350', bg='#333333')
frame.place(x=480, y=70)

# Creating widgets
login_label = tk.Label(frame, text="Hello There", bg='#333333',
                       fg='#00FF41', font=("Inconsolata", 23))
# username_label = tk.Label(frame, text="Cliente", bg = '#333333', fg = '#FFFFFF', font=("Arial", 16))
username_entry = tk.Entry(frame, width=25, fg='black', border=0, bg='white', font=("Inconsolata", 11))
password_entry = tk.Entry(frame, width=25, fg='black', border=0, bg='white', show="*", font=("Inconsolata", 11))
# password_label = tk.Label(frame, text="Senha", bg = '#333333', fg = '#FFFFFF', font=("Arial", 16))
login_button = tk.Button(frame, text="Login", bg='#FF3399',
                         fg='#FFFFFF', font=("Inconsolata", 16), command=login)
register_button = tk.Button(frame, text="Cadastro", bg='#FF3399', fg='#FFFFFF', font=(
    "Inconsolata", 16))

# Placing widgets on the screen
login_label.place(x=50, y=5)
# username_label.grid(row=1, column=0)
username_entry.place(x=30, y=80)
username_entry.insert(0, 'Cliente')
password_entry.place(x=30, y=140)
password_entry.insert(0, 'Senha')
login_button.place(x=35, y=204)
register_button.place(x=190, y=204)

# frame.pack()

#tk.Frame(frame, width=295, height=2, bg = 'black').place(x=25, y=107)

username_entry.bind('<FocusIn>', on_enterU)
username_entry.bind('<FocusOut>', on_leaveU)
password_entry.bind('<FocusIn>', on_enterP)
password_entry.bind('<FocusOut>', on_leaveP)

window.mainloop()
