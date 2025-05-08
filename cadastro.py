import tkinter as tk
from tkinter import messagebox, simpledialog
import threading

from flask import Flask, request, jsonify

# --- FLASK API ---
app = Flask(__name__)
mercados = []
produtos = []

@app.route('/mercado', methods=['POST'])
def cadastrar_mercado():
    data = request.json
    mercados.append(data)
    return jsonify({'mensagem': 'Mercado cadastrado com sucesso'}), 201

@app.route('/produto', methods=['POST'])
def cadastrar_produto():
    data = request.json
    produtos.append(data)
    return jsonify({'mensagem': 'Produto cadastrado com sucesso'}), 201

@app.route('/produtos/<localizacao>', methods=['GET'])
def listar_descontos(localizacao):
    mercados_local = [m['nome'] for m in mercados if m['localizacao'] == localizacao]
    resultado = [p for p in produtos if p['mercado'] in mercados_local and p['desconto']]
    return jsonify(resultado), 200

# Rodar o Flask em uma thread separada
def iniciar_flask():
    app.run(port=5000)

threading.Thread(target=iniciar_flask, daemon=True).start()

# --- INTERFACE TKINTER ---
import requests

def cadastrar_mercado():
    nome = simpledialog.askstring("Mercado", "Nome do mercado:")
    localizacao = simpledialog.askstring("Mercado", "Localização:")

    if nome and localizacao:
        r = requests.post("http://localhost:5000/mercado", json={
            "nome": nome,
            "localizacao": localizacao
        })
        messagebox.showinfo("Cadastro", r.json()["mensagem"])

def cadastrar_produto():
    mercado = simpledialog.askstring("Produto", "Nome do mercado:")
    nome = simpledialog.askstring("Produto", "Nome do produto:")
    preco = simpledialog.askfloat("Produto", "Preço:")
    desconto = messagebox.askyesno("Desconto", "Produto está com desconto?")

    if mercado and nome and preco is not None:
        r = requests.post("http://localhost:5000/produto", json={
            "mercado": mercado,
            "nome": nome,
            "preco": preco,
            "desconto": desconto
        })
        messagebox.showinfo("Cadastro", r.json()["mensagem"])

def listar_produtos():
    localizacao = simpledialog.askstring("Consulta", "Digite a localização:")
    r = requests.get(f"http://localhost:5000/produtos/{localizacao}")
    resultado = r.json()

    texto = "\n".join(
        [f"{p['nome']} - R${p['preco']} ({p['mercado']})" for p in resultado]
    ) if resultado else "Nenhum produto com desconto encontrado."
    
    messagebox.showinfo("Resultados", texto)

# Construir janela
janela = tk.Tk()
janela.title("Sistema de Descontos")

tk.Button(janela, text="Cadastrar Mercado", command=cadastrar_mercado, width=30).pack(pady=10)
tk.Button(janela, text="Cadastrar Produto", command=cadastrar_produto, width=30).pack(pady=10)
tk.Button(janela, text="Listar Produtos com Desconto", command=listar_produtos, width=30).pack(pady=10)

janela.mainloop()