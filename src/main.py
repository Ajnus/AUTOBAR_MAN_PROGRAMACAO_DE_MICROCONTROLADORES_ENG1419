import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from datetime import datetime
from PIL import Image, ImageTk
from unidecode import unidecode
from integracao import serial_load
from integracao import serial_send


tamanho_fonte = 7


root = tk.Tk()
root.title("AutoBar, man")
root.geometry("1080x720")
root.configure(bg='#333333')
root.resizable(False, False)

storeName = "AutoBar, man"
table1 = "DRINKS"
table2 = "INGREDIENTS"

img = tk.PhotoImage(file='assets/images/izac_resized.png')
with Image.open("assets/images/sort.png") as sort:
    sort_image = ImageTk.PhotoImage(sort)

frame1 = tk.Frame(root, width='350', height='1850', bg='#333333')
frame1.place(x=20, y=280)
my_tree1 = ttk.Treeview(frame1, height=6)

frame2 = tk.Frame(root, width='350', height='1850', bg='#333333')
frame2.place(x=2, y=510)
my_tree2 = ttk.Treeview(frame2, height=6)


# INSERÇÃO DE DADOS

def reverse(tuples):
    new_tup = tuples[::-1]
    return new_tup


def insert(table, id, name, attr3, attr4):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    if table == "ingredients":
        column3 = "itemVolume"
        config3 = "INTEGER"
        column4 = "itemExpirationDate"
        config4 = "DATETIME"
    elif table == "drinks":
        column3 = "itemPrice"
        config3 = "FLOAT"
        column4 = "itemComposition"
        config4 = "TEXT"

    cursor.execute(f"""CREATE TABLE IF NOT EXISTS
                   {table}(itemId INTEGER, itemName TEXT, {column3} {config3}, {column4} {config4})""")
    cursor.execute(f"INSERT INTO {table} VALUES(?, ?, ?, ?)",
                   (id, name, attr3, attr4))
    conn.commit()


def delete(table, data):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    if table == "ingredients":
        column3 = "itemVolume"
        config3 = "INTEGER"
        column4 = "itemExpirationDate"
        config4 = "DATETIME"
    elif table == "drinks":
        column3 = "itemPrice"
        config3 = "FLOAT"
        column4 = "itemComposition"
        config4 = "TEXT"

    cursor.execute(f"""CREATE TABLE IF NOT EXISTS
                   {table}(itemId INTEGER, itemName TEXT, {column3} {config3}, {column4} {config4})""")
    cursor.execute(f"DELETE FROM {table} WHERE itemId = ?", (int(data),))
    conn.commit()


def update(table, id, name, attr3, attr4, idName):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    if table == "ingredients":
        column3 = "itemVolume"
        config3 = "INTEGER"
        column4 = "itemExpirationDate"
        config4 = "DATETIME"
    elif table == "drinks":
        column3 = "itemPrice"
        config3 = "FLOAT"
        column4 = "itemComposition"
        config4 = "TEXT"

    cursor.execute(f"""CREATE TABLE IF NOT EXISTS
                   {table}(itemId INTEGER, itemName TEXT, {column3} {config3}, {column4} {config4})""")
    cursor.execute(f"UPDATE {table} SET itemId = ?, itemName = ?, {column3} = ?, {column4} = ? WHERE itemId = ?",
                   (int(id), name, attr3, attr4, int(idName)))

    conn.commit()


def read(table):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    if table == "ingredients":
        column3 = "itemVolume"
        config3 = "INTEGER"
        column4 = "itemExpirationDate"
        config4 = "DATETIME"
    elif table == "drinks":
        column3 = "itemPrice"
        config3 = "FLOAT"
        column4 = "itemComposition"
        config4 = "TEXT"

    cursor.execute(f"""CREATE TABLE IF NOT EXISTS
                   {table}(itemId INTEGER, itemName TEXT, {column3} {config3}, {column4} {config4})""")
    cursor.execute(f"SELECT * FROM {table}")

    results = cursor.fetchall()
    # print(results)
    conn.commit()
    return results


def update_combobox(combo, table):
    # Atualizar a lista de opções para a combobox
    global options
    options = [my_tree2.item(item, 'values')[1]
               for item in my_tree2.get_children()] if table == "ingredients" else [my_tree1.item(item, 'values')[1]
                                                                                    for item in my_tree1.get_children()]
    combo["values"] = options
    # print(f"UPDATE_COMBOBOX, OPTIONS: {options}")


def insert_data(table, combo):
    global composition

    if table == "ingredients":
        tree = my_tree2
        entrada1 = entry_ingredient_name
        entrada2 = entry_volume
        texto_2 = "Volume disponível"
        entrada3 = entry_expiration_date.get()
        texto_3 = "Data de Validade"
        nome_local = "ingrediente"

    if table == "drinks":
        tree = my_tree1
        entrada1 = entry_drink_name
        entrada2 = entry_price
        texto_2 = "Preço"
        entrada3 = composition
        texto_3 = "Composição"
        nome_local = "drink"

    if str(entrada1.get()) != "":
        var_local1 = str(entrada1.get())
    else:
        messagebox.showinfo(
            "Erro", f"Nome de {nome_local} não inserido.\nPor favor tente outra vez.")
        return

    if str(entrada2.get()) != "":
        var_local2 = str(entrada2.get())
    else:
        messagebox.showinfo(
            "Erro", f"{texto_2} de {nome_local} não inserido.\nPor favor tente outra vez.")
        return

    print(f"COMPOSITION: {str(entrada3)}")
    if str(entrada3) != "":
        var_local3 = str(entrada3)
    else:
        messagebox.showinfo(
            "Erro", f"{texto_3} de {nome_local} não inserida.\nPor favor tente outra vez.")
        return

    existing_data = read(f"{table}")
    if existing_data:
        max_id = max(int(item[0]) for item in existing_data)
    else:
        max_id = 0

    # Generate a new ID for the item
    new_id = max_id + 1
    insert(table, new_id, str(var_local1),
           str(var_local2), str(var_local3))

    for data in tree.get_children():
        # print("insert_data: pre-delete")
        tree.delete(data)
        # print("insert_data: pos-delete")

    # counter2 = 0  # Initialize a counter variable
    for result in reverse(read(f"{table}")):
        tree.insert(parent='', index='end', iid=result[0],
                    text="", values=(result), tag='orow')
        # counter2 += 1  # Increment the counter for the next iteration

    tree.tag_configure('orow', background="#EEEEEE",
                       font=('Inconsolata', tamanho_fonte))
    tree.grid(row=0, column=5, columnspan=4, rowspan=5, padx=10, pady=1)

    # Limpar campos após a inserção de dados
    entrada1.delete(0, 'end')
    entrada2.delete(0, 'end')

    if table == "ingredients":
        entry_expiration_date.delete(0, 'end')
        update_combobox(combo, table)

    if table == "drinks":
        clear_all()

    composition.clear()


def delete_data(table, combo):

    # print(f"DELETE_DATA: {options}")
    if table == "ingredients":
        tree = my_tree2
        update_combobox(combo, table)
    if table == "drinks":
        tree = my_tree1

    if tree.selection():
        # print(tree)

        # print("removeu?")
        # if my_tree2.selection():
        # print(f"PRE-SELECTED ITEM: {tree.selection()[0]}")
        selected_item = tree.selection()[0]
        # else:
        #    None

        if table == "ingredients":
            update_combobox(combo, table)
            # Remover o item selecionado da Combobox
            ingredient_name = tree.item(selected_item)['values'][1]
            # print(f"INGREDIENT NAME: {ingredient_name}")
            global options
            # print(options)
            options.remove(ingredient_name)
            combo["values"] = options

        # if selected_item:
        # Obtenha o índice da linha selecionada
        # selected_index = tree.index(selected_item)
        # Exclua os dados do banco de dados
        delete_data = str(tree.item(selected_item)['values'][0])
        # print(f" actual selected item: {tree.item(selected_item)}")
        # print(f"delete_data: {delete_data}" )
        delete(table, delete_data)

        for data in tree.get_children():
            # print("pre-delete tree")
            tree.delete(data)
            # print("pos-delete tree")

        # Selecione automaticamente a próxima linha (se existir)
        """
            if selected_index < len(tree.get_children()):
                next_item = tree.get_children()[selected_index]
                tree.selection_set(next_item)
            elif selected_index > 0:
                # Se não houver uma próxima linha, selecione a linha anterior
                prev_item = tree.get_children()[selected_index - 1]
                tree.selection_set(prev_item)
            # else:
            # messagebox.showinfo(
            # "Erro", "Nenhuma linha selecionada para exclusão.")
            """

        # counter2 = 0  # Initialize a counter variable
        for result in reverse(read(f"{table}")):
            tree.insert(parent='', index='end', iid=result[0],
                        text="", values=(result), tag='orow')
            # counter2 += 1  # Increment the counter for the next iteration

        tree.tag_configure('orow', background="#EEEEEE",
                           font=('Inconsolata', tamanho_fonte))
        tree.grid(row=0, column=5, columnspan=4, rowspan=5, padx=10, pady=1)

    else:
        messagebox.showinfo(
            "Erro", "Nenhum ingrediente selecionado.\nPor favor tente outra vez.")


def update_data(table):
    if table == "ingredients":
        tree = my_tree2
        entrada1 = entry_ingredient_name
        entrada2 = entry_volume
        entrada3 = entry_expiration_date.get()
    if table == "drinks":
        tree = my_tree1
        entrada1 = entry_drink_name
        entrada2 = entry_price
        entrada3 = composition

    # print(tree.selection())
    # print(tree.selection()[0])
    selected_item = tree.selection()[0]
    # print(selected_item)

    update_name = str(tree.item(selected_item)['values'][0])
    update(table, update_name, entrada1.get(), entrada2.get(),
           entrada3, update_name)

    for data in tree.get_children():
        tree.delete(data)

    # counter2 = 0  # Initialize a counter variable
    for result in reverse(read(f"{table}")):
        tree.insert(parent='', index='end', iid=result[0],
                    text="", values=(result), tag='orow')
        # counter2 += 1  # Increment the counter for the next iteration

    tree.tag_configure('orow', background="#EEEEEE",
                       font=('Inconsolata', tamanho_fonte))
    tree.grid(row=0, column=5, columnspan=4, rowspan=5, padx=10, pady=1)

# reordena coluna


def sort_treeview_column(tv, col, col_type, reverse):
    data = [(tv.set(child, col), child) for child in tv.get_children('')]

    # Define uma chave de ordenação personalizada com base no tipo de dados na coluna
    def key_func(item):
        # print(f"item: {item}")
        value, _ = item
        if col_type == 'int':
            # print(f"col_type == 'int'? {col_type}")
            return int(value)
        elif col_type == 'float':
            # print(f"col_type == 'float'? {col_type}")
            return float(value)
        elif col_type == 'datetime':
            return datetime.strptime(value, '%d-%m-%Y')
        elif col_type == 'str':
            # Remove a acentuação antes de comparar strings
            return unidecode(value.lower())
        else:
            # print(f"col_type 'else'? {col_type}")
            return value

    data.sort(key=lambda x: key_func(x), reverse=reverse)

    for index, item in enumerate(data):
        tv.move(item[1], '', index)

    tv.heading(col, command=lambda: sort_treeview_column(
        tv, col, col_type, not reverse))

    """
    data = [(treeview.set(child, col), child)
            for child in treeview.get_children('')]

    # Define uma chave de ordenação personalizada com base no tipo de dados na coluna
    def key_func(item):
        value, _ = item
        try:
            # Tentativa de conversão para número
            return float(value)
        except ValueError:
            try:
                # Tentativa de conversão para data
                return datetime.strptime(value, '%d-%m-%Y')
            except ValueError:
                # Se falhar, manter como string
                return value

    data.sort(key=key_func, reverse=reverse)

    for index, (value, child) in enumerate(data):
        treeview.move(child, '', index)
"""


composition = {}


def add_composition():
    print("CHAMOU ADD_COMPOSITION")
    global composition
    print(f"COMPOSIÇÃO: {composition}")
    selected_ingredient = combo.get()
    selected_quantity = entry_quantities.get()

    if selected_ingredient and selected_quantity:
        current_text = combinacoes_label.cget("text")
        updated_text = f"{current_text} {selected_quantity} ml de {selected_ingredient};"
        combinacoes_label.config(text=updated_text)
        composition[selected_ingredient] = selected_quantity
        print("COMPOSIÇÃO: {composition}")

    else:
        messagebox.showinfo(
            "Erro", "Nenhum ingrediente ou quantidade selecionado(s).\nPor favor tente outra vez.")


def clear_all():
    combo.set("")
    entry_quantities.delete(0, 'end')
    combinacoes_label.config(text="Selecionados:")


# Creating widgets
title_label = tk.Label(root, text=storeName, bg='#333333',
                       fg='#00FF41', font=("Inconsolata", 30), bd=2)
table_title_label1 = tk.Label(
    root, text=table1, bg='#333333', fg='#00FF41', font=("Inconsolata", 20), bd=2)
table_title_label2 = tk.Label(
    root, text=table2, bg='#333333', fg='#F803F8', font=("Inconsolata", 20), bd=2)

drink_name_label = tk.Label(frame1, text="Nome", font=(
    "Inconsolata", tamanho_fonte), bd=2, relief="solid", bg='#FFFFFF')
price_label = tk.Label(frame1, text="Preço", font=(
    "Inconsolata", tamanho_fonte), bd=2, relief="solid", bg='#FFFFFF')
ingredients_label = tk.Label(frame1, text="Ingredientes", font=(
    "Inconsolata", tamanho_fonte), bd=2, relief="solid", bg='#FFFFFF')
quantities_label = tk.Label(frame1, text="Quantidades (ml)", font=(
    "Inconsolata", tamanho_fonte), bd=2, relief="solid", bg='#FFFFFF')

ingredient_name_label = tk.Label(frame2, text="Nome", font=(
    "Inconsolata", tamanho_fonte), bd=2, relief="solid", bg='#FFFFFF')
volume_label = tk.Label(frame2, text="Vol Disponível (ml)", font=(
    "Inconsolata", tamanho_fonte), bd=2, relief="solid", bg='#FFFFFF')
expiration_date_label = tk.Label(frame2, text="Data de Validade", font=(
    "Inconsolata", tamanho_fonte), bd=2, relief="solid", bg='#FFFFFF')

entry_drink_name = tk.Entry(frame1, width=22, bd=5,
                            font=("Inconsolata", tamanho_fonte))
entry_price = tk.Entry(frame1, width=22, bd=5,
                       font=("Inconsolata", tamanho_fonte))
entry_ingredients = tk.Entry(frame1, width=22, bd=5,
                             font=("Inconsolata", tamanho_fonte))
entry_quantities = tk.Entry(frame1, width=22, bd=5,
                            font=("Inconsolata", tamanho_fonte))

entry_ingredient_name = tk.Entry(frame2, width=22, bd=5,
                                 font=("Inconsolata", tamanho_fonte))
entry_volume = tk.Entry(frame2, width=22, bd=5,
                        font=("Inconsolata", tamanho_fonte))
entry_expiration_date = tk.Entry(frame2, width=22, bd=5,
                                 font=("Inconsolata", tamanho_fonte))

# mock
combinacoes_label = tk.Label(root, text="selecionados:", font=(
    "Inconsolata", tamanho_fonte), bg="#333333", fg="#00FF41")

button_enter1 = tk.Button(
    root, text="Inserir", padx=5, pady=5, width=7, bd=3,
    font=('Inconsolata', tamanho_fonte), bg="#0099FF", command=lambda: insert_data("drinks", combo)
)
button_enter2 = tk.Button(
    root, text="Inserir", padx=5, pady=5, width=7, bd=3,
    font=('Inconsolata', tamanho_fonte), bg="#0099FF", command=lambda: insert_data("ingredients", combo)
)
button_update1 = tk.Button(
    root, text="Alterar", padx=5, pady=5, width=7, bd=3,
    font=('Inconsolata', tamanho_fonte), bg="#FFFF08", command=lambda: update_data("drinks")
)
button_update2 = tk.Button(
    root, text="Alterar", padx=5, pady=5, width=7, bd=3,
    font=('Inconsolata', tamanho_fonte), bg="#FFFF08", command=lambda: update_data("ingredients")
)
button_delete1 = tk.Button(
    root, text="Remover", padx=5, pady=5, width=7, bd=3,
    font=('Inconsolata', tamanho_fonte), bg="#E62E00", command=lambda: delete_data("drinks", combo)
)
button_delete2 = tk.Button(
    root, text="Remover", padx=5, pady=5, width=7, bd=3,
    font=('Inconsolata', tamanho_fonte), bg="#E62E00", command=lambda: delete_data("ingredients", combo)
)
button_add = tk.Button(
    root, text="adicionar", padx=3, pady=3, width=10, bd=3,
    font=('Inconsolata', tamanho_fonte-2), bg="#00FF41", command=add_composition
)
button_clear = tk.Button(
    root, text="limpar tudo", padx=3, pady=3, width=10, bd=3,
    font=('Inconsolata', tamanho_fonte-2), bg="#FF9900", command=clear_all

)

button_download = tk.Button(
    root, text="Desce uma!🍺", padx=20, pady=15, width=7, bd=3,
    # command=lambda: insert_data("drinks", combo)
    font=('Inconsolata', tamanho_fonte, 'bold'),
    bg="#AE4EAF",
    fg="white", command=lambda: serial_send(resultado+"\n")
)


# Antes de criar a lista options, certifique-se de preencher a tabela my_tree2 com dados
for data in my_tree2.get_children():
    my_tree2.delete(data)

# counter = 0  # Initialize a counter variable
for result in reverse(read("ingredients")):
    my_tree2.insert(parent='', index='end', iid=result[0],
                    text="", values=(result), tag='orow')
    # counter += 1  # Increment the counter for the next iteration

# Agora, crie a lista de opções para a combobox
options = [my_tree2.item(item, 'values')[1]
           for item in my_tree2.get_children()]
# print(f"OPTIONS: {options}")

# Variável para armazenar a opção selecionada
selected_option = tk.StringVar()

# Criar a combobox
combo = ttk.Combobox(frame1, textvariable=selected_option,
                     values=options, width=16, state="readonly")
# combo.pack(pady=10)
# combo.set("Escolha um ingrediente")  # Valor padrão exibido na combobox


def on_select(event=None):
    print("selecionou")
    combo.set(combo.get())

# TO DO: não Funciona


def on_focus_out(event=None):
    print("ON_FOCUS_EVENT")
    combo.selection_clear()


# Adicionar um evento para quando uma opção é selecionada
combo.bind("<<ComboboxSelected>>", lambda event=None: on_select())

# Adiciona o evento <FocusOut> para deselecionar a combobox ao clicar fora dela
combo.bind("<FocusOut>", lambda event=None: on_focus_out())

# Label para exibir a opção selecionada
label_result = tk.Label(root, text="Selecionado: Nenhum",
                        font=("Arial", tamanho_fonte))
# label_result.pack(pady=10)


# Placing widgets on the screen
title_label.place(x=390, y=10)
table_title_label1.place(x=490, y=244)
table_title_label2.place(x=445, y=470)

tk.Label(root, image=img, bg='white').place(x=440, y=70)

drink_name_label.grid(row=0, column=0, padx=1, pady=1)
price_label.grid(row=1, column=0, padx=10, pady=10)
ingredients_label.grid(row=2, column=0, padx=10, pady=10)
quantities_label.grid(row=3, column=0, padx=10, pady=10)

ingredient_name_label.grid(row=0, column=0, padx=10, pady=10)
volume_label.grid(row=1, column=0, padx=10, pady=10)
expiration_date_label.grid(row=2, column=0, padx=10, pady=10)

entry_drink_name.grid(row=0, column=1, columnspan=3, padx=5, pady=5)
entry_price.grid(row=1, column=1, columnspan=3, padx=5, pady=5)
combo.grid(row=2, column=1, columnspan=3, padx=5, pady=5)
entry_quantities.grid(row=3, column=1, columnspan=3, padx=5, pady=5)

entry_ingredient_name.grid(row=0, column=1, columnspan=3, padx=5, pady=5)
entry_volume.grid(row=1, column=1, columnspan=3, padx=5, pady=5)
entry_expiration_date.grid(row=2, column=1, columnspan=3, padx=5, pady=5)

button_enter1.place(x=386-78, y=433)
button_update1.place(x=645, y=433)
button_delete1.place(x=386+610+30-38, y=433)

button_enter2.place(x=386-78, y=660)
button_update2.place(x=645, y=660)
button_delete2.place(x=386+610+30-38, y=660)

button_add.place(x=384-178-59, y=427)
button_clear.place(x=384-79-68, y=427)
button_download.place(x=958, y=225)


combinacoes_label.place(x=80, y=473)


style = ttk.Style()
style.configure("Treeview.Heading", font=('Inconsolata', 10))

# Criar um ícone de seta
# arrow_icon = create_arrow_icon()

my_tree1['columns'] = ("ID", "Nome", "Preco", "Composicao")
my_tree1.column("#0", width=0, stretch=False)
my_tree1.column("ID", anchor="w", width=40)
my_tree1.column("Nome", anchor="w", width=200)
my_tree1.column("Preco", anchor="w", width=60)
my_tree1.column("Composicao", anchor="w", width=440)
my_tree1.heading("ID", text="ID", image=sort_image, anchor="center")
my_tree1.heading("Nome", text="Nome", anchor="center")
my_tree1.heading("Preco", text="Preço", anchor="center")
my_tree1.heading(
    "Composicao", text="Composição (dose de 100 ml)", anchor="center")

# Configurar cabeçalhos clicáveis
col_types = {'ID': 'int', 'Nome': 'str',
             'Preço': 'float', 'Data de Validade': 'datetime'}
for col in my_tree1['columns']:
    text = my_tree1.heading(col, "text")
    my_tree1.heading(col, text=text, command=lambda c=col: sort_treeview_column(
        my_tree1, c, col_types.get(c, 'str'), False))

"""
for col in my_tree1['columns']:
    text = my_tree1.heading(col, "text")
    my_tree1.heading(
        col, text=text, command=lambda c=col: sort_treeview_column(my_tree1, c, False))
"""

# print("1")
# print(my_tree1.get_children())
for data in my_tree1.get_children():
    # print("2")
    my_tree1.delete(data)
    # print("apagou")

# counter = 0  # Initialize a counter variable
for result in reverse(read("drinks")):
    my_tree1.insert(parent='', index='end', iid=result[0],
                    text="", values=(result), tag='orow')
    # counter += 1  # Increment the counter for the next iteration

my_tree1.tag_configure('orow', background="#EEEEEE",
                       font=('Inconsolata', tamanho_fonte))
my_tree1.grid(row=0, column=5, columnspan=4, rowspan=5, padx=10, pady=1)


my_tree2['columns'] = ("ID", "Nome", "Volume", "Data de Validade")
my_tree2.column("#0", width=0, stretch=False)
my_tree2.column("ID", anchor="w", width=40)
my_tree2.column("Nome", anchor="w", width=200)
my_tree2.column("Volume", anchor="w", width=200)
my_tree2.column("Data de Validade", anchor="w", width=300)
# my_tree2.heading('#0', text="ID", image = sort_image, anchor="center")
my_tree2.heading("ID", text="ID", image=sort_image, anchor="center",
                 command=lambda: sort_treeview_column(my_tree2, '#0', 'ID', False))
my_tree2.heading("Nome", text="Nome", anchor="center")
my_tree2.heading("Volume", text="Volume disponível (ml)", anchor="center")
my_tree2.heading("Data de Validade", text="Data de Validade", anchor="center")

# Configurar cabeçalhos clicáveis
col_types = {'ID': 'int', 'Nome': 'str',
             'Volume': 'float', 'Data de Validade': 'datetime'}
for col in my_tree2['columns']:
    text = my_tree2.heading(col, "text")
    my_tree2.heading(col, text=text, command=lambda c=col: sort_treeview_column(
        my_tree2, c, col_types.get(c, 'str'), False))

"""
for col in my_tree2['columns']:
    text = my_tree2.heading(col, "text")
    my_tree2.heading(
        col, text=text, command=lambda c=col: sort_treeview_column(my_tree2, c, False))
"""

# print("1")
# print(my_tree2.get_children())
for data in my_tree2.get_children():
    # print("2")
    my_tree2.delete(data)
    # print("apagou")

# counter = 0  # Initialize a counter variable
for result in reverse(read("ingredients")):
    my_tree2.insert(parent='', index='end', iid=result[0],
                    text="", values=(result), tag='orow')
    # counter += 1  # Increment the counter for the next iteration

my_tree2.tag_configure('orow', background="#EEEEEE",
                       font=('Inconsolata', tamanho_fonte))
my_tree2.grid(row=0, column=5, columnspan=4, rowspan=5, padx=10, pady=1)

serial_load()

# print(read("drinks"))
drinks = read("drinks")

# Inicializa a variável de texto
resultado = ""

# Percorre a lista de drinks
for drink in drinks:
    # Extrai as informações relevantes
    drink_id, nome, preco, composicao_str = drink

    # Converte a string de composição para um dicionário
    composicao = eval(composicao_str)

    # Extrai os valores das chaves específicas ou usa 0 se a chave não existir
    valor_campari = composicao.get('Campari', 0)
    valor_limonada = composicao.get('Limonada', 0)
    valor_pinga_azul = composicao.get('Pinga Azul', 0)
    valor_cachaca = composicao.get('Cachaça', 0)

    # Formata a string e adiciona ao resultado
    resultado += f"{drink_id} {preco} {valor_campari} {valor_limonada} {valor_pinga_azul} {valor_cachaca} {unidecode(nome)}\n"

# Exibe o resultado
# print(resultado)

# texto = "ID PREÇO PP1 PP2 PP3 PP4 NOME)"

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
