import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import ast

tamanho_fonte = 7


root = tk.Tk()
root.title("Auto Barman")
root.geometry("1080x720")
root.configure(bg='#333333')
root.resizable(False, False)

storeName = "AutoBar, man"
table1 = "DRINKS"
table2 = "INGREDIENTS"

img = tk.PhotoImage(file='assets/images/izac_resized.png')

frame1 = tk.Frame(root, width='350', height='1850', bg='#333333')
frame1.place(x=80, y=280)
my_tree1 = ttk.Treeview(frame1, height=6)

frame2 = tk.Frame(root, width='350', height='1850', bg='#333333')
frame2.place(x=45, y=510)
my_tree2 = ttk.Treeview(frame2, height=6)

# Creating widgets
title_label = tk.Label(root, text=storeName, bg='#333333', fg='#00FF41', font=("Inconsolata", 30), bd=2)
table_title_label1 = tk.Label(root, text=table1, bg='#333333', fg='#00FF41', font=("Inconsolata", 20), bd=2)
table_title_label2= tk.Label(root, text=table2, bg='#333333', fg='#F803F8', font=("Inconsolata", 20), bd=2)

id_label1 = tk.Label(frame1, text="Nome", font=("Inconsolata", tamanho_fonte), bd=2, relief="solid", bg='#FFFFFF')
name_label1 = tk.Label(frame1, text="Preço", font=("Inconsolata", tamanho_fonte), bd=2, relief="solid", bg='#FFFFFF')
price_label1 = tk.Label(frame1, text="Ingredientes", font=("Inconsolata", tamanho_fonte), bd=2, relief="solid", bg='#FFFFFF')
quantity_label1 = tk.Label(frame1, text="Quantidades (ml)", font=("Inconsolata", tamanho_fonte), bd=2, relief="solid", bg='#FFFFFF')

id_label2 = tk.Label(frame2, text="Nome", font=("Inconsolata", tamanho_fonte), bd=2, relief="solid", bg='#FFFFFF')
name_label2 = tk.Label(frame2, text="Volume Disponível (ml)", font=("Inconsolata", tamanho_fonte), bd=2, relief="solid", bg='#FFFFFF')
price_label2 = tk.Label(frame2, text="Data de Validade", font=("Inconsolata", tamanho_fonte), bd=2, relief="solid", bg='#FFFFFF')

entry_id1 = tk.Entry(frame1, width=25, bd=5, font=("Inconsolata", tamanho_fonte))
entry_name1 = tk.Entry(frame1, width=25, bd=5, font=("Inconsolata", tamanho_fonte))
entry_price1 = tk.Entry(frame1, width=25, bd=5, font=("Inconsolata", tamanho_fonte))
entry_quantity1= tk.Entry(frame1, width=25, bd=5, font=("Inconsolata", tamanho_fonte))

entry_id2 = tk.Entry(frame2, width=25, bd=5, font=("Inconsolata", tamanho_fonte))
entry_name2 = tk.Entry(frame2, width=25, bd=5, font=("Inconsolata", tamanho_fonte))
entry_price2 = tk.Entry(frame2, width=25, bd=5, font=("Inconsolata", tamanho_fonte))

#mock
quantidades_label = tk.Label(root, text="selecionados: 200 ml de Vodka; 100 ml de Lemon", font=("Inconsolata", tamanho_fonte), bg="#333333", fg="#00FF41")

button_enter1=tk.Button(
    root, text="Inserir", padx=5, pady=5, width=7,bd=3,
    font=('Inconsolata', tamanho_fonte), bg="#0099FF"
    )
button_enter2=tk.Button(
    root, text="Inserir", padx=5, pady=5, width=7,bd=3,
    font=('Inconsolata', tamanho_fonte), bg="#0099FF"
    )
button_update1=tk.Button(
    root, text="Alterar", padx=5, pady=5, width=7,bd=3,
    font=('Inconsolata', tamanho_fonte), bg="#FFFF08"
    )
button_update2=tk.Button(
    root, text="Alterar", padx=5, pady=5, width=7,bd=3,
    font=('Inconsolata', tamanho_fonte), bg="#FFFF08"
    )
button_delete1=tk.Button(
    root, text="Remover", padx=5, pady=5, width=7,bd=3,
    font=('Inconsolata', tamanho_fonte), bg="#E62E00"
    )
button_delete2=tk.Button(
    root, text="Remover", padx=5, pady=5, width=7,bd=3,
    font=('Inconsolata', tamanho_fonte), bg="#E62E00"
    )
button_add1=tk.Button(
    root, text="adicionar", padx=4, pady=3, width=10,bd=3,
    font=('Inconsolata', tamanho_fonte-1), bg="#00FF41"
    )
button_clear1=tk.Button(
    root, text="limpar tudo", padx=3, pady=3, width=10,bd=3,
    font=('Inconsolata', tamanho_fonte-1), bg="#FF9900"
    )
button_add2=tk.Button(
    root, text="adicionar", padx=4, pady=3, width=10,bd=3,
    font=('Inconsolata', tamanho_fonte-1), bg="#00FF41"
    )
button_clear2=tk.Button(
    root, text="limpar tudo", padx=3, pady=3, width=10,bd=3,
    font=('Inconsolata', tamanho_fonte-1), bg="#FF9900"
    )



# Placing widgets on the screen
title_label.place(x=390, y=10)
table_title_label1.place(x=490, y=244)
table_title_label2.place(x=445, y=470)

tk.Label(root, image=img, bg='white').place(x=440, y=70)

id_label1.grid(row=0, column=0, padx=1, pady=1)
name_label1.grid(row=1, column=0, padx=10, pady=10)
price_label1.grid(row=2, column=0, padx=10, pady=10)
quantity_label1.grid(row=3, column=0, padx=10, pady=10)

id_label2.grid(row=0, column=0, padx=10, pady=10)
name_label2.grid(row=1, column=0, padx=10, pady=10)
price_label2.grid(row=2, column=0, padx=10, pady=10)

entry_id1.grid(row=0, column=1, columnspan=3, padx=5, pady=5)
entry_name1.grid(row=1, column=1, columnspan=3, padx=5, pady=5)
entry_price1.grid(row=2, column=1, columnspan=3, padx=5, pady=5)
entry_quantity1.grid(row=3, column=1, columnspan=3, padx=5, pady=5)

entry_id2.grid(row=0, column=1, columnspan=3, padx=5, pady=5)
entry_name2.grid(row=1, column=1, columnspan=3, padx=5, pady=5)
entry_price2.grid(row=2, column=1, columnspan=3, padx=5, pady=5)

button_enter1.place(x=386, y=433)
button_update1.place(x=386+245+30, y=433)
button_delete1.place(x=386+490+30, y=433)

button_enter2.place(x=386, y=660)
button_update2.place(x=386+245+30, y=660)
button_delete2.place(x=386+490+30, y=660)

button_add1.place(x=384-178,y=427)
button_clear1.place(x=384-79,y=427)
button_add2.place(x=384-177,y=635)
button_clear2.place(x=384-78,y=635)

quantidades_label.place(x=80,y=473)


style = ttk.Style()
style.configure("Treeview.Heading", font=('Inconsolata', 10))

my_tree1['columns']=("ID", "Name", "Price", "Composition")
my_tree1.column("#0", width=0, stretch=False)
my_tree1.column("ID", anchor="w", width=100)
my_tree1.column("Name", anchor="w", width=150)
my_tree1.column("Price", anchor="w", width=180)
my_tree1.column("Composition", anchor="w", width=150)
my_tree1.heading("ID", text = "ID", anchor="center")
my_tree1.heading("Name", text = "Nome", anchor="center")
my_tree1.heading("Price", text = "Preço", anchor="center")
my_tree1.heading("Composition", text = "Composição", anchor="center")

my_tree1.tag_configure('orow', background = "#EEEEEE", font=('Inconsolata', tamanho_fonte))
my_tree1.grid(row=0, column=5, columnspan=4, rowspan=5, padx=10, pady=1)

my_tree2['columns']=("ID", "Name", "Volume", "Data de Validade")
my_tree2.column("#0", width=0, stretch=False)
my_tree2.column("ID", anchor="w", width=100)
my_tree2.column("Name", anchor="w", width=150)
my_tree2.column("Volume", anchor="w", width=180)
my_tree2.column("Data de Validade", anchor="w", width=150)
my_tree2.heading("ID", text = "ID", anchor="center")
my_tree2.heading("Name", text = "Nome", anchor="center")
my_tree2.heading("Volume", text = "Volume disponível (ml)", anchor="center")
my_tree2.heading("Data de Validade", text = "Data de Validade", anchor="center")

my_tree2.tag_configure('orow', background = "#EEEEEE", font=('Inconsolata', tamanho_fonte))
my_tree2.grid(row=0, column=5, columnspan=4, rowspan=5, padx=10, pady=1)

root.mainloop()


# OLD CODE:
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
