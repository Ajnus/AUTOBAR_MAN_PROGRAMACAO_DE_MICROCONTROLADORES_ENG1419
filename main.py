import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import ast


root = tk.Tk()
root.title("Auto Barman")
root.geometry("1080x720")
root.configure(bg='#333333')
root.resizable(False, False)
my_tree = ttk.Treeview(root)
storeName = "AutoBar, man"

img = tk.PhotoImage(file='izac.png')
tk.Label(root, image=img, bg='white').place(x=341, y=330)

frame = tk.Frame(root, width='350', height='1850', bg='#333333')
frame.place(x=400, y=240)

# Creating widgets
title_label = tk.Label(frame, text=storeName, bg='#333333', fg='#00FF41', font=("Inconsolata", 30), bd=2)
title_label.grid(row=0, column=0, columnspan=8, padx=20, pady=20)

id_label = tk.Label(root, text="ID", font=("Inconsolata", 15))
name_label = tk.Label(root, text="Nome", font=("Inconsolata", 15))
price_label = tk.Label(root, text="Preço", font=("Inconsolata", 15))
quantity_label = tk.Label(root, text="Quantidade", font=("Inconsolata", 15))

entry_id = tk.Entry(root, width=25, bd=5, font=("Inconsolata", 15))
entry_name = tk.Entry(root, width=25, bd=5, font=("Inconsolata", 15))
entry_price = tk.Entry(root, width=25, bd=5, font=("Inconsolata", 15))
entry_quantity = tk.Entry(root, width=25, bd=5, font=("Inconsolata", 15))

button_enter=tk.Button(
    root, text="Inserir", padx=5, pady=5, width=7,bd=3,
    font=('Inconsolata', 15), bg="#0099FF"
    )
button_update=tk.Button(
    root, text="Alterar", padx=5, pady=5, width=7,bd=3,
    font=('Inconsolata', 15), bg="#FFFF08"
    )
button_delete=tk.Button(
    root, text="Remover", padx=5, pady=5, width=7,bd=3,
    font=('Inconsolata', 15), bg="#E62E00"
    )


# Placing widgets on the screen
id_label.grid(row=1, column=0, padx=10, pady=10)
name_label.grid(row=2, column=0, padx=10, pady=10)
price_label.grid(row=3, column=0, padx=10, pady=10)
quantity_label.grid(row=4, column=0, padx=10, pady=10)

entry_id.grid(row=1, column=1, columnspan=3, padx=5, pady=5)
entry_name.grid(row=2, column=1, columnspan=3, padx=5, pady=5)
entry_price.grid(row=3, column=1, columnspan=3, padx=5, pady=5)
entry_quantity.grid(row=4, column=1, columnspan=3, padx=5, pady=5)

button_enter.grid(row=5, column=1, columnspan=1)
button_update.grid(row=5, column=2, columnspan=1)
button_delete.grid(row=5, column=3, columnspan=1)

style = ttk.Style()
style.configure("Treeview.Heading", font=('Inconsolata', 15))

my_tree['columns']=("ID", "Name", "Price", "Quantity")
my_tree.column("#0", width=0, stretch=False)
my_tree.column("ID", anchor="w", width=100)
my_tree.column("Name", anchor="w", width=200)
my_tree.column("Price", anchor="w", width=150)
my_tree.column("Quantity", anchor="w", width=150)
my_tree.heading("ID", text = "ID", anchor="w")
my_tree.heading("Name", text = "Nome", anchor="w")
my_tree.heading("Price", text = "Preço", anchor="w")
my_tree.heading("Quantity", text = "Quantidade", anchor="w")

my_tree.tag_configure('orow', background = "#EEEEEE", font=('Inconsolata', 15))
my_tree.grid(row=1, column=5, columnspan=4, rowspan=5, padx=10, pady=10)







root.mainloop()

















# def login():
# username = "bino"
# password = "cmonboy"

# if username_entry.get() == username and password_entry.get() == password:
#    messagebox.showinfo(
#        title="IT IS ON!", message=f"Bem-vindo ao Bar dos Brothers, {username}.")
# else:
#    messagebox.showinfo(title="Erro", message="Login inválido.")

"""
def login():
    username = username_entry.get()
    password = password_entry.get()

    if username == 'bino' and password == 'cmonboy':
        messagebox.showinfo(
            title="IT IS ON!", message=f"Bem-vindo ao Bar dos Brothers, {username}.")

        screen1 = tk.Toplevel(window)
        screen1.title = "O Chamado do Bar"
        screen1.geometry('925x500+300+200')
        screen1.config(bg='#333333')
        screen1.resizable(False, False)

        tk.Label(screen1, text="Entremo!", bg='#00FF41', font=(
            "Inconsolata", 50, 'bold')).pack(expand=True)

        screen1.mainloop()

    elif username != 'bino' and password != 'cmonboy':
        messagebox.showinfo(
            title="Inválido", message="Cliente e Senha inválidos.")

    elif username != 'bino' and password != 'cmonboy':
        messagebox.showinfo(title="Inválido", message="Senha inválida.")

    elif username != 'bino':
        messagebox.showinfo(title="Inválido", message="Cliente inválido.")


def on_enterU(e):
    username_entry.delete(0, 'end')


def on_leaveU(e):
    name = username_entry.get()
    if name == '':
        username_entry.insert(0, 'Cliente')


def on_enterP(e):
    password_entry.delete(0, 'end')


def on_leaveP(e):
    name = password_entry.get()
    if name == '':
        password_entry.insert(0, 'Senha')


def register():
    screen2 = tk.Toplevel(window)
    screen2.title = "Cadastro"
    screen2.geometry('925x500+300+200')
    screen2.config(bg='#333333')
    screen2.resizable(False, False)

    img2 = tk.PhotoImage(file='persuadable_bouncer_1.png')
    tk.Label(screen2, image=img2).place(x=50, y=50)

    frame2 = tk.Frame(screen2, width='350', height='350', bg='#333333')
    frame2.place(x=480, y=70)


    login_label = tk.Label(frame2, text="Hello There", bg='#333333',
                       fg='#00FF41', font=("Inconsolata", 23))
    username_entry = tk.Entry(frame2, width=25, fg='black',
                          border=0, bg='white', font=("Inconsolata", 11))
    password_entry = tk.Entry(frame2, width=25, fg='black',
                          border=0, bg='white', show="*", font=("Inconsolata", 11))

    register_button = tk.Button(frame2, text="Cadastro", bg='#FF3399', fg='#FFFFFF', font=(
    "Inconsolata", 16), command=register)


    login_label.place(x=50, y=5)

    username_entry.place(x=30, y=80)
    username_entry.insert(0, 'Cliente')
    password_entry.place(x=30, y=140)
    password_entry.insert(0, 'Senha')
    login_button.place(x=35, y=204)
    register_button.place(x=190, y=204)

    username_entry.bind('<FocusIn>', on_enterU)
    username_entry.bind('<FocusOut>', on_leaveU)
    password_entry.bind('<FocusIn>', on_enterP)
    password_entry.bind('<FocusOut>', on_leaveP)
    --------
    
    # username_label = tk.Label(frame, text="Cliente", bg = '#333333', fg = '#FFFFFF', font=("Arial", 16))
#username_entry = tk.Entry(frame, width=25, fg='black',
                          #border=0, bg='white', font=("Inconsolata", 11))
#password_entry = tk.Entry(frame, width=25, fg='black',
                          #border=0, bg='white', show="*", font=("Inconsolata", 11))
# password_label = tk.Label(frame, text="Senha", bg = '#333333', fg = '#FFFFFF', font=("Arial", 16))
#login_button = tk.Button(frame, text="Login", bg='#FF3399',
                         #fg='#FFFFFF', font=("Inconsolata", 16), command=login)
#register_button = tk.Button(frame, text="Cadastro", bg='#FF3399', fg='#FFFFFF', font=(
    #"Inconsolata", 16), command=register)
    
    # username_label.grid(row=1, column=0)
#username_entry.place(x=30, y=80)
#username_entry.insert(0, 'Cliente')
#password_entry.place(x=30, y=140)
#password_entry.insert(0, 'Senha')
#login_button.place(x=35, y=204)
#register_button.place(x=190, y=204)

# frame.pack()

# tk.Frame(frame, width=295, height=2, bg = 'black').place(x=25, y=107)

#username_entry.bind('<FocusIn>', on_enterU)
#username_entry.bind('<FocusOut>', on_leaveU)
#password_entry.bind('<FocusIn>', on_enterP)
#password_entry.bind('<FocusOut>', on_leaveP)


"""
