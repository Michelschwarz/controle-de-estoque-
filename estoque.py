import sqlite3
from tkinter import *
from tkinter import messagebox, Scrollbar
from PIL import Image, ImageTk  # Certifique-se de instalar Pillow usando 'pip install pillow'

def create_table():
    with sqlite3.connect('estoque.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco REAL NOT NULL
        )
        ''')
        conn.commit()

def add_product(nome, quantidade, preco):
    with sqlite3.connect('estoque.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO produtos (nome, quantidade, preco)
        VALUES (?, ?, ?)
        ''', (nome, quantidade, preco))
        conn.commit()

def list_products():
    with sqlite3.connect('estoque.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM produtos')
        rows = cursor.fetchall()
        return rows

def update_quantity(id, nova_quantidade):
    with sqlite3.connect('estoque.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        UPDATE produtos
        SET quantidade = ?
        WHERE id = ?
        ''', (nova_quantidade, id))
        conn.commit()

def delete_product(id):
    with sqlite3.connect('estoque.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        DELETE FROM produtos
        WHERE id = ?
        ''', (id,))
        conn.commit()

def add_product_gui():
    nome = nome_entry.get()
    quantidade = quantidade_entry.get()
    preco = preco_entry.get()
    if nome and quantidade.isdigit() and preco.replace('.', '', 1).isdigit():
        add_product(nome, int(quantidade), float(preco))
        messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")
        clear_entries()
    else:
        messagebox.showwarning("Erro", "Por favor, preencha todos os campos corretamente.")

def list_products_gui():
    products = list_products()
    list_frame = Toplevel(root)  # Cria uma nova janela para a lista de produtos
    list_frame.title("Lista de Produtos")
    list_frame.geometry("600x400")

    # Configura o widget Text com barra de rolagem
    text = Text(list_frame, wrap=NONE, width=70, height=20)
    scrollbar = Scrollbar(list_frame, orient=VERTICAL, command=text.yview)
    text.configure(yscrollcommand=scrollbar.set)

    # Adiciona cabeçalho
    text.insert(END, f"{'ID':<5} {'Nome':<20} {'Quantidade':<10} {'Preço':<10}\n")
    text.insert(END, '-'*50 + '\n')

    # Adiciona produtos
    for row in products:
        text.insert(END, f"{row[0]:<5} {row[1]:<20} {row[2]:<10} {row[3]:<10.2f}\n")
    
    text.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

def update_quantity_gui():
    id = id_entry.get()
    nova_quantidade = nova_quantidade_entry.get()
    if id.isdigit() and nova_quantidade.isdigit():
        update_quantity(int(id), int(nova_quantidade))
        messagebox.showinfo("Sucesso", "Quantidade atualizada com sucesso!")
        clear_entries()
    else:
        messagebox.showwarning("Erro", "ID ou quantidade inválidos.")

def delete_product_gui():
    id = id_entry.get()
    if id.isdigit():
        delete_product(int(id))
        messagebox.showinfo("Sucesso", "Produto deletado com sucesso!")
        clear_entries()
    else:
        messagebox.showwarning("Erro", "ID inválido.")

def clear_entries():
    nome_entry.delete(0, END)
    quantidade_entry.delete(0, END)
    preco_entry.delete(0, END)
    id_entry.delete(0, END)
    nova_quantidade_entry.delete(0, END)

def resize_image(image, width, height):
    """Redimensiona a imagem para o tamanho especificado."""
    return image.resize((width, height), Image.LANCZOS)

def main_gui():
    global root, nome_entry, quantidade_entry, preco_entry, id_entry, nova_quantidade_entry, bg_photo

    create_table()

    root = Tk()
    root.title("Controle de Estoque")
    root.geometry("800x600")

    # Definir o ícone da janela
    try:
        root.iconbitmap('C:/Users/Rudimar/Desktop/estoque/logoico.ico')  
    except Exception as e:
        print(f"Erro ao carregar o ícone: {e}")

    # Carregar a imagem de fundo
    try:
        bg_image = Image.open('C:/Users/Rudimar/Desktop/estoque/design.png')  
        bg_image = resize_image(bg_image, root.winfo_screenwidth(), root.winfo_screenheight())
        bg_photo = ImageTk.PhotoImage(bg_image)
    except Exception as e:
        print(f"Erro ao carregar a imagem de fundo: {e}")
        bg_photo = None

    # Configura o Canvas para a imagem de fundo
    canvas = Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
    canvas.pack(fill=BOTH, expand=True)
    if bg_photo:
        canvas.create_image(0, 0, anchor=NW, image=bg_photo)
        # Para garantir que a imagem não seja removida pelo garbage collector
        canvas.image = bg_photo

    # Redimensiona a imagem de fundo quando a janela é redimensionada
    def on_resize(event):
        new_width = event.width
        new_height = event.height
        resized_image = resize_image(bg_image, new_width, new_height)
        bg_photo = ImageTk.PhotoImage(resized_image)
        canvas.create_image(0, 0, anchor=NW, image=bg_photo)
        canvas.image = bg_photo

    root.bind("<Configure>", on_resize)

    # Frame para adicionar produtos
    add_frame = Frame(root, bg='#ffffff', padx=20, pady=20, bd=2, relief=SOLID)
    add_frame.place(relx=0.5, rely=0.3, anchor=CENTER)

    Label(add_frame, text="Nome do Produto:", bg='#ffffff', font=('Helvetica', 12)).grid(row=0, column=0, sticky=W, pady=5)
    nome_entry = Entry(add_frame, width=40, font=('Helvetica', 12))
    nome_entry.grid(row=0, column=1, pady=5)

    Label(add_frame, text="Quantidade:", bg='#ffffff', font=('Helvetica', 12)).grid(row=1, column=0, sticky=W, pady=5)
    quantidade_entry = Entry(add_frame, width=40, font=('Helvetica', 12))
    quantidade_entry.grid(row=1, column=1, pady=5)

    Label(add_frame, text="Preço:", bg='#ffffff', font=('Helvetica', 12)).grid(row=2, column=0, sticky=W, pady=5)
    preco_entry = Entry(add_frame, width=40, font=('Helvetica', 12))
    preco_entry.grid(row=2, column=1, pady=5)

    Button(add_frame, text="Adicionar Produto", command=add_product_gui,
            bg='#4CAF50', fg='white', font=('Helvetica', 12), relief=RAISED).grid(row=3, column=0, columnspan=2, pady=10)

    # Frame para atualizar e deletar produtos
    update_delete_frame = Frame(root, bg='#ffffff', padx=20, pady=20, bd=2, relief=SOLID)
    update_delete_frame.place(relx=0.5, rely=0.7, anchor=CENTER)

    Label(update_delete_frame, text="ID do Produto:",
           bg='#ffffff', font=('Helvetica', 12)).grid(row=0, column=0, sticky=W, pady=5)
    id_entry = Entry(update_delete_frame, width=40, font=('Helvetica', 12))
    id_entry.grid(row=0, column=1, pady=5)

    Label(update_delete_frame, text="Nova Quantidade:",
           bg='#ffffff', font=('Helvetica', 12)).grid(row=1, column=0, sticky=W, pady=5)
    nova_quantidade_entry = Entry(update_delete_frame, width=40, font=('Helvetica', 12))
    nova_quantidade_entry.grid(row=1, column=1, pady=5)

    Button(update_delete_frame, text="Atualizar a Quantidade", command=update_quantity_gui,
            bg='#2196F3', fg='white', font=('Helvetica', 12), relief=RAISED).grid(row=2, column=0, columnspan=2, pady=5)
    Button(update_delete_frame, text="Deletar Produto", command=delete_product_gui,
            bg='#f44336', fg='white', font=('Helvetica', 12), relief=RAISED).grid(row=3, column=0, columnspan=2, pady=5)

    Button(update_delete_frame, text="Listar Produtos", command=list_products_gui,
            bg='#FFC107', fg='black', font=('Helvetica', 12), relief=RAISED).grid(row=4, column=0, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main_gui()
